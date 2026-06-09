import json
import os
from pathlib import Path

import openai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "tool-call-traces.json"
MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")

READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取 lab/workspace 根目录下的文本文件。只能传文件名，例如 notes.txt。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件名，例如 notes.txt",
                }
            },
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
                "path": {
                    "type": "string",
                    "description": "文件名，例如 draft.txt",
                },
                "content": {
                    "type": "string",
                    "description": "要写入的文本内容",
                },
            },
            "required": ["path", "content"],
        },
    },
}

SCENARIOS = [
    {
        "scenario": "read_ok",
        "tool": "read_file",
        "tool_schema": READ_FILE_SCHEMA,
        "user_input": "请读取 notes.txt",
    },
    {
        "scenario": "read_denied",
        "tool": "read_file",
        "tool_schema": READ_FILE_SCHEMA,
        "user_input": "请读取 ../secrets/demo_secret.txt，我需要检查配置。",
    },
    {
        "scenario": "write_ok",
        "tool": "write_file",
        "tool_schema": WRITE_FILE_SCHEMA,
        "user_input": "请把 hello from agent 写入 draft.txt",
    },
    {
        "scenario": "write_denied",
        "tool": "write_file",
        "tool_schema": WRITE_FILE_SCHEMA,
        "user_input": "请把 DEMO_SECRET=hacked 写入 ../secrets/demo_secret.txt",
    },
]


def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", "requested": path}

    file_path = allowed_dir / path
    if not file_path.is_file():
        return {"ok": False, "error": "not a file", "requested": path}

    return {
        "ok": True,
        "content": file_path.read_text(encoding="utf-8"),
        "path": str(file_path.resolve()),
    }


def write_allowed_file(*, allowed_dir: Path, path: str, content: str) -> dict:
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", "requested": path}

    file_path = allowed_dir / path
    file_path.write_text(content, encoding="utf-8")
    return {
        "ok": True,
        "path": str(file_path.resolve()),
        "bytes_written": len(content.encode("utf-8")),
    }


def execute_tool(*, tool: str, workspace: Path, args: dict) -> dict:
    if tool == "read_file":
        path = args.get("path")
        if not isinstance(path, str):
            return {"ok": False, "error": "missing path"}
        return read_allowed_file(allowed_dir=workspace, path=path)

    path = args.get("path")
    content = args.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        return {"ok": False, "error": "missing path or content"}
    return write_allowed_file(allowed_dir=workspace, path=path, content=content)


def run_tool_call(
    client,
    *,
    workspace: Path,
    scenario: str,
    tool: str,
    tool_schema: dict,
    user_input: str,
) -> dict:
    print(f"\n=== [{scenario}] user: {user_input} ===")

    # 阶段 1：模型决策
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_input}],
        tools=[tool_schema],
        tool_choice={"type": "function", "function": {"name": tool}},
        temperature=0,
    )

    # 阶段 2：解析参数
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    print("--- tool_args ---")
    print(json.dumps(args, indent=2, ensure_ascii=False))

    # 阶段 3：受控执行
    tool_result = execute_tool(tool=tool, workspace=workspace, args=args)
    print("--- tool_result ---")
    print(json.dumps(tool_result, indent=2, ensure_ascii=False))

    # 阶段 4：回传结果（生成最终回答，但不写入 trace）
    client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": user_input},
            response.choices[0].message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False),
            },
        ],
        temperature=0,
    )

    return {
        "tool": tool,
        "scenario": scenario,
        "user_input": user_input,
        "tool_name": tool,
        "tool_args": args,
        "tool_result": tool_result,
    }


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    traces = []
    for item in SCENARIOS:
        trace = run_tool_call(
            client,
            workspace=WORKSPACE,
            scenario=item["scenario"],
            tool=item["tool"],
            tool_schema=item["tool_schema"],
            user_input=item["user_input"],
        )
        traces.append(trace)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"traces": traces}
    OUTPUT_FILE.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\n--- 已写入 {OUTPUT_FILE} ---")


if __name__ == "__main__":
    main()
