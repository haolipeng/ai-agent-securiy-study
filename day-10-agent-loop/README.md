# Day 10: Agent Loop 骨架

在 day-09 单次 tool calling 之上，用 `while` 循环实现最小 Agent loop，直到模型不再返回 `tool_calls`。

## 场景

默认任务：读取 `notes.txt`，将其内容写入 `summary.txt`（read → write → 最终回答）。

工具执行层在 [`agent_tools/`](../agent_tools/)，本目录只保留 loop 逻辑。

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-10-agent-loop/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

## 输出

- `output/agent-run.json` — 每次运行生成（已 gitignore）

## 笔记

[docs/notes/week-02/day-10-agent-loop.md](../docs/notes/week-02/day-10-agent-loop.md)
