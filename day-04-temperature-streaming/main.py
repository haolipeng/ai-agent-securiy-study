import os

import openai

MODEL = "gpt-3.5-turbo"
QUESTION = "给一个 AI Agent 安全审计工具起一个中文名字，要求 2 到 6 个字，只输出名字"
TEMPERATURES = [0.0, 0.7, 1.5]
RUNS_PER_TEMPERATURE = 5


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    for temperature in TEMPERATURES:
        print(f"\n=== temperature={temperature} ===")

        for i in range(RUNS_PER_TEMPERATURE):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": QUESTION}],
                temperature=temperature,
                max_tokens=30,
            )

            result = response.choices[0].message.content.strip()
            print(f"{i + 1}. {result}")


if __name__ == "__main__":
    main()
