import os

import openai


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    chat = client.chat.completions.create(
        model="Claude-Opus-4.7",
        messages=[{"role": "user", "content": "你是什么大语言模型？"}],
    )
    print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()

