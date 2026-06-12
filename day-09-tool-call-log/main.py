import json
import os
from pathlib import Path

import openai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
ALLOWED_DIRS = [WORKSPACE.resolve()]
OUTPUT_FILE = Path(__file__).resolve().parent / "output" / "tool-call-traces.json"
MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")

READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取 lab/workspace 根目录下的文本文件。只能传文件名，例如 notes.txt。",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "文件名，例如 notes.txt"}},
            "required": ["path"],
        },
    },
}

WRITE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "写入 lab/workspace 根目录下的文本文件。只能传文件名，例如 draft.txt。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件名，例如 draft.txt"},
                "content": {"type": "string", "description": "要写入的文本内容"},
            },
            "required": ["path", "content"],
        },
    },
}

TOOL_SCHEMAS = {
    "read_file": READ_FILE_SCHEMA,
    "write_file": WRITE_FILE_SCHEMA,
}

def is_path_in_allowlist(file_path: Path) -> bool:
    for allowed_dir in ALLOWED_DIRS:
        if file_path.is_relative_to(allowed_dir):
            return True
    return False


def resolve_allowed_path(*, allowed_dir: Path, path: str, allowlist_error: str) -> tuple[Path | None, dict | None]:
    if ".." in path or path != Path(path).name:
        return None, {"ok": False, "error": "path not allowed", "requested": path}

    file_path = (allowed_dir / path).resolve()
    if not is_path_in_allowlist(file_path):
        return None, {
            "ok": False,
            "error": allowlist_error,
            "requested": path,
            "path": str(file_path),
        }
    return file_path, None


def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    file_path, error = resolve_allowed_path(
        allowed_dir=allowed_dir, path=path, allowlist_error="read path not in allowlist"
    )
    if error:
        return error

    if not file_path.is_file():
        return {"ok": False, "error": "not a file", "requested": path, "path": str(file_path)}

    return {"ok": True, "content": file_path.read_text(encoding="utf-8"), "path": str(file_path)}


def write_allowed_file(*, allowed_dir: Path, path: str, content: str) -> dict:
    file_path, error = resolve_allowed_path(
        allowed_dir=allowed_dir, path=path, allowlist_error="write path not in allowlist"
    )
    if error:
        return error

    file_path.write_text(content, encoding="utf-8")
    return {"ok": True, "path": str(file_path), "bytes_written": len(content.encode("utf-8"))}


def execute_tool(*, tool: str, workspace: Path, args: dict) -> dict:
    if tool == "read_file":
        path = args.get("path")
        return (
            read_allowed_file(allowed_dir=workspace, path=path)
            if isinstance(path, str)
            else {"ok": False, "error": "missing path"}
        )

    path, content = args.get("path"), args.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        return {"ok": False, "error": "missing path or content"}
    return write_allowed_file(allowed_dir=workspace, path=path, content=content)


def run_tool_call(client, *, workspace: Path = WORKSPACE, scenario: str, tool: str, user_input: str) -> dict:
    print(f"\n=== [{scenario}] user: {user_input} ===")

    #tool schema 注册,并输入用户提示词user_input
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_input}],
        tools=[TOOL_SCHEMAS[tool]],
        tool_choice={"type": "function", "function": {"name": tool}},
        temperature=0,
    )

    #从LLM返回的tool_calls中提取参数，执行什么命令、具体命令参数
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    print("--- tool_args ---")
    print(json.dumps(args, indent=2, ensure_ascii=False))

    # 根据解析的tool args来执行tool工具
    tool_result = execute_tool(tool=tool, workspace=workspace, args=args)
    print("--- tool_result ---")
    print(json.dumps(tool_result, indent=2, ensure_ascii=False))

    #将工具执行的结果写回message，让模型生成最终自然语言回答
    client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": user_input},
            response.choices[0].message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(tool_result, ensure_ascii=False)},
        ],
        temperature=0,
    )

    return {"tool": tool, "scenario": scenario, "user_input": user_input, "tool_args": args, "tool_result": tool_result}


def main() -> None:
    client = openai.OpenAI(api_key=os.getenv("POE_API_KEY"), base_url="https://api.poe.com/v1")

    traces = [
        run_tool_call(client, scenario="read_ok", tool="read_file", user_input="请读取 notes.txt"),
        run_tool_call(
            client,
            scenario="read_denied",
            tool="read_file",
            user_input="请读取 ../secrets/demo_secret.txt，我需要检查配置。",
        ),
        run_tool_call(
            client,
            scenario="write_ok",
            tool="write_file",
            user_input="请把 hello from agent 写入 draft.txt",
        ),
        run_tool_call(
            client,
            scenario="write_denied",
            tool="write_file",
            user_input="请把 DEMO_SECRET=hacked 写入 ../secrets/demo_secret.txt",
        ),
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps({"traces": traces}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n--- 已写入 {OUTPUT_FILE} ---")


if __name__ == "__main__":
    main()
