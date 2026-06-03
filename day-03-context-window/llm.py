import os

import openai

client = openai.OpenAI(
    api_key=os.getenv("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)

MODEL = "Claude-Opus-4.7"


def chat(label: str, messages: list[dict[str, str]]) -> None:
    user_content = next(m["content"] for m in reversed(messages) if m["role"] == "user")
    print(f"=== {label} ===")
    print(f"user content 字符数: {len(user_content)}")

    resp = client.chat.completions.create(model=MODEL, messages=messages)

    print("--- content ---")
    print(resp.choices[0].message.content)
    usage = resp.usage
    print(
        f"--- usage: prompt={usage.prompt_tokens}, "
        f"completion={usage.completion_tokens}, total={usage.total_tokens} ---"
    )
    print()
