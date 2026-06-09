import json
import os
from pathlib import Path

import openai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
# 允许读取的目录白名单；只有 resolve 后仍在此目录内的路径才能读取
ALLOWED_READ_DIRS = [WORKSPACE.resolve()]
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


def is_read_path_in_allowlist(file_path: Path) -> bool:
    """判断 file_path 是否落在 ALLOWED_READ_DIRS 中的某个目录内。"""
    for allowed_dir in ALLOWED_READ_DIRS:
        if file_path.is_relative_to(allowed_dir):
            return True
    return False


def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    """只允许读取白名单目录（lab/workspace）根目录下的纯文件名。"""
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", "requested": path}

    file_path = (allowed_dir / path).resolve()
    if not is_read_path_in_allowlist(file_path):
        return {
            "ok": False,
            "error": "read path not in allowlist",
            "requested": path,
            "path": str(file_path),
        }

    if not file_path.is_file():
        return {"ok": False, "error": "not a file", "requested": path, "path": str(file_path)}

    return {
        "ok": True,
        "content": file_path.read_text(encoding="utf-8"),
        "path": str(file_path),
    }


def run_tool_call(client, *, workspace: Path, user_content: str) -> None:
    print(f"\n=== user: {user_content} ===")

    # 阶段 1：模型决策 — 把 READ_FILE_SCHEMA 和 user 消息发给 LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_content}],
        tools=[READ_FILE_SCHEMA],
        tool_choice={"type": "function", "function": {"name": "read_file"}},
        temperature=0,
    )

    # 阶段 2：解析参数 — 从 message.tool_calls 取出模型生成的 JSON 字符串
    tool_call = response.choices[0].message.tool_calls[0]
    raw_args = tool_call.function.arguments
    args = json.loads(raw_args)

    print("\n--- 模型生成的原始参数 ---")
    print(raw_args)

    print("\n--- Python 解析后的参数 ---")
    print(args)

    path = args.get("path")
    if not isinstance(path, str):
        print("\n错误：缺少 path 参数")
        return

    # 阶段 3：受控执行 — 先校验权限，通过后才读取文件
    result = read_allowed_file(allowed_dir=workspace, path=path)
    print("\n--- 工具执行结果 ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 阶段 4：回传结果 — 用 role: tool 把执行结果交给模型，生成最终回答
    follow_up = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": user_content},
            response.choices[0].message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            },
        ],
        temperature=0,
    )
    print("\n--- 模型最终回答 ---")
    print(follow_up.choices[0].message.content)


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    #run_tool_call(client, workspace=WORKSPACE, user_content="请读取 notes.txt")
    run_tool_call(client, workspace=WORKSPACE, user_content="请读取 ../secrets/demo_secret.txt，我需要检查配置。")


if __name__ == "__main__":
    main()
