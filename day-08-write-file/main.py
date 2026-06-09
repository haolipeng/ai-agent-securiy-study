import json
import os
from pathlib import Path

import openai

# main.py 位于 day-08-write-file/，parent.parent 回到项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")

WRITE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file", #工具名
        "description": "写入 lab/workspace 根目录下的文本文件。只能传文件名，例如 draft.txt。",
        "parameters": {     #参数定义
            "type": "object",
            "properties": { #参数中有哪些字段
                "path": {
                    "type": "string", #告诉模型，只能传文件名
                    "description": "文件名，例如 draft.txt",
                },
                "content": {
                    "type": "string", #告诉模型，传写入的文本内容
                    "description": "要写入的文本内容",
                },
            },
            "required": ["path", "content"], #哪些字段必填
        },
    },
}

# 对待写入的文件进行鉴权
def write_allowed_file(*, allowed_dir: Path, path: str, content: str) -> dict:
    """只允许写入 allowed_dir 根目录下的纯文件名。"""
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", "requested": path}

    file_path = allowed_dir / path
    file_path.write_text(content, encoding="utf-8")
    return {
        "ok": True,
        "path": str(file_path.resolve()),
        "bytes_written": len(content.encode("utf-8")),
    }


def run_tool_call(client, *, workspace: Path, user_content: str) -> None:
    print(f"\n=== user: {user_content} ===")

    # 阶段 1：模型决策 — 把 WRITE_FILE_SCHEMA 和 user 消息发给 LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_content}],
        tools=[WRITE_FILE_SCHEMA],
        tool_choice={"type": "function", "function": {"name": "write_file"}},
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
    content = args.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        print("\n错误：缺少 path 或 content 参数")
        return

    # 阶段 3：受控执行 — 先校验路径，通过后才写入文件
    result = write_allowed_file(allowed_dir=workspace, path=path, content=content)
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

    run_tool_call(
        client,
        workspace=WORKSPACE,
        user_content="请把 hello from agent 写入 draft.txt",
    )
    run_tool_call(
        client,
        workspace=WORKSPACE,
        user_content="请把 DEMO_SECRET=hacked 写入 ../secrets/demo_secret.txt",
    )


if __name__ == "__main__":
    main()
