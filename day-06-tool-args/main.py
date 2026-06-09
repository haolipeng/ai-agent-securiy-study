import json
import os
import tempfile
from pathlib import Path

import openai


tool_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取 workspace 目录里的文本文件。",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "文件路径，例如 notes.txt。"}},
            "required": ["path"],
        },
    },
}


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir) / "workspace"
        workspace.mkdir()
        (workspace / "notes.txt").write_text("这是允许读取的文件。\n", encoding="utf-8")

        client = openai.OpenAI(api_key=os.getenv("POE_API_KEY"), base_url="https://api.poe.com/v1")
        response = client.chat.completions.create(
            model=os.getenv("POE_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": "请读取 notes.txt"}],
            tools=[tool_schema],
            tool_choice={"type": "function", "function": {"name": "read_file"}},
            temperature=0,
        )

        tool_call = response.choices[0].message.tool_calls[0]
        raw_args = tool_call.function.arguments
        args = json.loads(raw_args)

        print("--- 模型生成的原始参数 ---")
        print(raw_args)

        print("\n--- Python 解析后的参数 ---")
        print(args)

        path = (workspace / args["path"]).resolve()
        if not path.is_relative_to(workspace.resolve()):
            print("\n拒绝：路径越权")
            return

        print("\n--- 读取结果 ---")
        print(path.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
