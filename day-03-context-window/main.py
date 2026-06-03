from llm import chat

# 实验：改大此值（如 100、300），观察 prompt_tokens 上升及文首信息是否被遗忘
FILLER_PARAGRAPHS = 80


def filler(paragraphs: int) -> str:
    return "\n".join(
        f"[段落 {i}] Agent runtime security 学习占位文本，用于撑长输入上下文。"
        for i in range(1, paragraphs + 1)
    )


def experiment_short_input() -> None:
    chat(
        "实验 1：短输入",
        [{"role": "user", "content": "用一句话解释 token 和 context window 分别是什么。"}],
    )


def experiment_long_input(paragraphs: int = FILLER_PARAGRAPHS) -> None:
    needle = "隐藏口令：BLUE-42"
    long_content = (
        f"{needle}\n\n"
        f"{filler(paragraphs)}\n\n"
        "请只回答文首的隐藏口令是什么，不要解释。"
    )
    chat(
        "实验 2：长输入 + 文首追问",
        [{"role": "user", "content": long_content}],
    )


def main() -> None:
    experiment_short_input()
    experiment_long_input()


if __name__ == "__main__":
    main()
