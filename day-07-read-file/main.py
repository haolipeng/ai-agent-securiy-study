import json
import os
from pathlib import Path

import openai

WORKSPACE = Path(__file__).resolve().parent.parent / "lab" / "workspace"
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


def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    """只允许读取 allowed_dir 根目录下的纯文件名。"""
    # path 不可信：拒绝 .. 和子目录，只允许 notes.txt 这类纯文件名
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", "requested": path}

    # 判断文件是否存在，allowed_dir = lab/workspace/，path = notes.txt
    # 拼接后的file_path = lab/workspace/notes.txt
    # is_file标识文件存在，并且是一个普通文件
    file_path = allowed_dir / path
    if not file_path.is_file():
        return {"ok": False, "error": "not a file", "requested": path}

    return {
        "ok": True,
        "content": file_path.read_text(encoding="utf-8"),
        "path": str(file_path.resolve()),
    }


def run_tool_call(client, *, workspace: Path, user_content: str) -> None:
    print(f"\n=== user: {user_content} ===")

    # 阶段 1：模型决策 — 把 READ_FILE_SCHEMA 和 user 消息发给 LLM
    # 返回response
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

    # 校验是否传递了path参数
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
