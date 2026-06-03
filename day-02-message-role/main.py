import json
import os

import openai

client = openai.OpenAI(
    api_key=os.getenv("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)


def chat(messages: list[dict[str, str]]) -> None:
    """发送 messages 并打印回复。每条 message 含 role（system/user/assistant）和 content。"""
    # 打印本次请求的 messages，便于对照输入与输出
    for msg in messages:
        print(f"[{msg['role']}] {msg['content']}")
    print("--------------------------------")
    print()
    
    # 调用 Chat Completions API，messages 按顺序构成对话上下文
    resp = client.chat.completions.create(model="Claude-Opus-4.7", messages=messages)

    # content：模型返回的回复文本
    print("--- content start---")
    print(resp.choices[0].message.content)
    print("--- content end ---")

    print()

    # response：完整 API 响应体（含 id、usage 等元数据）
    print("--- response start ---")
    print(json.dumps(resp.model_dump(), indent=2, ensure_ascii=False))
    print("--- response end ---")


def main() -> None:
    # 实验 1：system 设定人设与规则（改 content，观察语气、长度、侧重点变化）
    # system 的 content内容是一样的，只是在最后加上了一句采用英文回答，就能改变模型的回答语言
    messages = [
        {
            "role": "system",
            #"content": "你是有 5 年经验的安全工程师，只回答 Agent 运行时安全问题，回答简洁，不超过 80 字。",
            "content": "你是有 5 年经验的安全工程师，只回答 Agent 运行时安全问题，回答简洁，不超过 80 字。采用英文回答",
        },
        {"role": "user", "content": "什么是 prompt injection？"},
    ]
    chat(messages)

    # 实验 2：assistant 携带历史，承接多轮上下文（注释掉 assistant 再运行，对比「它」能否被理解）
    messages = [
        {"role": "system", "content": "你是一个 AI Agent 安全助教。"},
        {"role": "user", "content": "system、user、assistant 三种 role 分别做什么？"},
        #{
        #    "role": "assistant",
        #    "content": "system 设定规则和人设，user 是用户提问，assistant 是模型回复，也用于保存多轮对话历史。",
        #},
        {"role": "user", "content": "用简短的话语来描述，为什么 system 更像策略输入？"},
    ]
    chat(messages)


if __name__ == "__main__":
    main()
