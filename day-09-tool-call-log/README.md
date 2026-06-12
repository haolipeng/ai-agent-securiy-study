# Day 09: 记录完整 tool calling 链路

运行 4 条 read/write tool calling，把 user_input、tool_args、tool_result 写入结构化 JSON 日志。

## 场景

| scenario | tool | 说明 |
|----------|------|------|
| `read_ok` | read_file | 读取 notes.txt |
| `read_denied` | read_file | 越权读取 ../secrets/demo_secret.txt |
| `write_ok` | write_file | 写入 draft.txt |
| `write_denied` | write_file | 越权写入 ../secrets/demo_secret.txt |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-09-tool-call-log/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

## 输出

- `output/tool-call-traces.json` — 每次运行生成（已 gitignore）
- `sample-traces.json` — 提交到仓库的精简样例

笔记：[docs/notes/week-02/day-09-tool-call-log.md](../docs/notes/week-02/day-09-tool-call-log.md)
