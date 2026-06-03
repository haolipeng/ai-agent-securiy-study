# Day 03: Context Window 与 Token

理解 context window、token 用量，以及多轮对话 history 对模型回答的影响。

本目录只保留一个实验：在对话开头埋入口令，中间追加多轮无关历史，最后追问开头口令。

默认使用 `gpt-3.5-turbo`，当前 Poe models 列表中它的上下文窗口是 16,384 tokens，适合演示小上下文窗口。这里不使用 1M tokens 级别的 `Claude-Opus-4.7`。

如需临时换模型：

```bash
export POE_MODEL=其他模型名
```

## 实测结果（gpt-3.5-turbo，口令：隐藏口令：我是小明）

| FILLER_ROUNDS | prompt_tokens | 回答 | 结果 |
|---------------|---------------|------|------|
| 80 | 7,103 | 隐藏口令：我是小明 | 正确 |
| 200 | 17,663 | 口令是"蓝色海洋"。 | 错误（超出 16k 窗口，幻觉） |

详细分析与原始输出见 [Day 03 笔记](../docs/notes/week-01/day-03-context-window.md)。

在项目根目录执行（需已设置环境变量 `POE_API_KEY`）：

```bash
source .venv/bin/activate
python3 day-03-context-window/main.py
```
