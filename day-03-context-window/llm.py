import os

import openai

client = openai.OpenAI(
    api_key=os.getenv("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)

MODEL = os.getenv("POE_MODEL", "gpt-3.5-turbo")


def chat(label: str, messages: list[dict[str, str]]) -> None:
    total_chars = sum(len(m["content"]) for m in messages)
    print(f"=== {label} ===")
    print(f"model: {MODEL}")
    print(f"messages 条数: {len(messages)}, 总字符数: {total_chars:,}")

    resp = client.chat.completions.create(model=MODEL, messages=messages)

    print("--- content ---")
    print(resp.choices[0].message.content)
    usage = resp.usage
    print(
        f"--- usage: prompt={usage.prompt_tokens}, "
        f"completion={usage.completion_tokens}, total={usage.total_tokens} ---"
    )
    print()
