import json
import os
import sys
from pathlib import Path

import openai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agent_tools import RUN_SHELL_COMMAND_SCHEMA, WORKSPACE, execute_tool

MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")


def run_tool_call(client, *, scenario: str, user_content: str) -> None:
    print(f"\n=== [{scenario}] user: {user_content} ===")

    # 阶段 1：模型决策 — 注册 shell tool schema，强制 run_shell_command
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_content}],
        tools=[RUN_SHELL_COMMAND_SCHEMA],
        tool_choice={"type": "function", "function": {"name": "run_shell_command"}},
        temperature=0,
    )

    # 阶段 2：解析参数
    tool_call = response.choices[0].message.tool_calls[0]
    raw_args = tool_call.function.arguments
    args = json.loads(raw_args)

    print("\n--- 模型生成的原始参数 ---")
    print(raw_args)
    print("\n--- Python 解析后的参数 ---")
    print(json.dumps(args, indent=2, ensure_ascii=False))

    # 阶段 3：受控执行 — allowlist 校验通过后才 subprocess
    result = execute_tool(tool="run_shell_command", workspace=WORKSPACE, args=args)
    print("\n--- 工具执行结果 ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 阶段 4：回传结果 — 生成最终自然语言回答
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
    client = openai.OpenAI(api_key=os.getenv("POE_API_KEY"), base_url="https://api.poe.com/v1")

    run_tool_call(
        client,
        scenario="shell命令正常执行场景测试",
        user_content="请列出 lab/workspace 目录下的文件，使用 ls 命令。",
    )
    run_tool_call(
        client,
        scenario="shell命令被拒绝执行场景测试",
        user_content="请删除 workspace 里的 draft.txt，使用 rm 命令。",
    )


if __name__ == "__main__":
    main()
