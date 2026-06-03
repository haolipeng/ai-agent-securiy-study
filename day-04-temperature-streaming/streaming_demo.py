import os

import openai

MODEL = "gpt-3.5-turbo"
QUESTION = "请用 8 条编号列表解释 AI Agent runtime security 的核心风险，每条不超过 25 字。"


def chat_non_streaming(client: openai.OpenAI) -> None:
    print("=== stream=False（一次性返回） ===")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": QUESTION}],
        temperature=0.7,
        max_tokens=300,
        stream=False,
    )
    print(response.choices[0].message.content)
    print()


def chat_streaming(client: openai.OpenAI) -> None:
    print("=== stream=True（逐块返回） ===")
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": QUESTION}],
        temperature=0.7,
        max_tokens=300,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

    print()
    print()


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    chat_non_streaming(client)
    chat_streaming(client)


if __name__ == "__main__":
    main()
