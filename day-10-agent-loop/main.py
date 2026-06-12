import json
import os
import sys
from pathlib import Path

import openai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agent_tools import TOOLS, WORKSPACE, execute_tool

OUTPUT_FILE = Path(__file__).resolve().parent / "output" / "agent-run.json"
MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")


def main() -> None:
    client = openai.OpenAI(api_key=os.getenv("POE_API_KEY"), base_url="https://api.poe.com/v1")
    user_input = "请读取 notes.txt 的内容，然后把它写入 summary.txt"

    print(f"\n=== user: {user_input} ===")
    messages = [{"role": "user", "content": user_input}]
    rounds: list[dict] = []
    iteration = 0
    final_answer = None

    # Agent loop：每轮 observe → plan → act → observe，直到模型不再返回 tool_calls
    while True:
        iteration += 1
        print(f"\n--- round {iteration}: plan ---")
        # plan — 把累积的 messages 和全部 tools 发给 LLM，由模型决定下一步要不要调工具
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
        )
        model_reply = response.choices[0].message

        # 终止条件：无 tool_calls 表示任务完成，content 即最终自然语言回答
        if not model_reply.tool_calls:
            final_answer = model_reply.content or "";
            print(f"--- final answer ---\n{final_answer}")
            break

        messages.append(model_reply)
        round_record = {"iteration": iteration, "tool_calls": []}

        for tool_call in model_reply.tool_calls:
            # act — 解析 tool_calls的参数去执行（read_file / write_file）
            tool = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"--- round {iteration}: act [{tool}] ---")
            print("tool_args:", json.dumps(args, indent=2, ensure_ascii=False))

            # 真正执行工具调用
            tool_result = execute_tool(tool=tool, workspace=WORKSPACE, args=args)
            print("tool_result:", json.dumps(tool_result, indent=2, ensure_ascii=False))

            round_record["tool_calls"].append({"tool": tool, "args": args, "result": tool_result})
            # observe — 把 tool result 写回 messages，作为下一轮的输入
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, ensure_ascii=False),
                }
            )

        # 收集每一轮tool工具的执行，将执行结果写入到output/agent-run.json文件中
        rounds.append(round_record)

    run = {
        "user_input": user_input,
        "rounds": rounds,
        "final_answer": final_answer,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n--- 已写入 {OUTPUT_FILE} ---")


if __name__ == "__main__":
    main()
