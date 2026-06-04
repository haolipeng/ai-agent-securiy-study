from llm import chat

NEEDLE = "隐藏口令：我是小明"

# 改大这个值，观察 prompt_tokens 是否接近模型上下文上限。
FILLER_ROUNDS = 170


def experiment_multi_turn_history(filler_rounds: int = FILLER_ROUNDS) -> None:
    messages: list[dict[str, str]] = [
        {"role": "user", "content": f"请记住这个口令：{NEEDLE}"},
        {"role": "assistant", "content": "好的，我已经记住了。"},
    ]

    # 模仿在会话中不断添加新内容，导致上下文被污染的场景
    for i in range(1, filler_rounds + 1):
        messages.extend(
            [
                {
                    "role": "user",
                    "content": f"第 {i} 轮：请用两句话介绍 Agent runtime security，这段内容用于增加对话历史长度。",
                },
                {
                    "role": "assistant",
                    "content": "Agent runtime security 关注智能体运行时的权限、工具调用、数据泄露和异常行为。它通过日志、策略和人工确认来降低风险。",
                },
            ]
        )

    messages.append(
        {
            "role": "user",
            "content": "对话最开始我让你记住的口令是什么？只回答口令，不要解释。",
        }
    )

    #模拟平时多轮会话输入导致的上下文污染的场景，观察输出效果
    chat(
        f"多轮对话历史实验（填充轮数={filler_rounds}）",
        messages,
    )


if __name__ == "__main__":
    experiment_multi_turn_history()
