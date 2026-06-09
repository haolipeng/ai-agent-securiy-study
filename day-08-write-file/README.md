# Day 08: 受控 write_file

使用项目级 `lab/` sandbox，实现 LLM tool calling + 纯文件名路径校验。

## 实验环境

| 路径 | 作用 |
|------|------|
| `lab/workspace/` | 允许写入的目录 |
| `lab/workspace/draft.txt` | 正常写入时生成的文件 |
| `lab/secrets/demo_secret.txt` | workspace 外的模拟敏感文件（越权靶标） |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-08-write-file/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

## 预期结果

- 场景 1（写入 `draft.txt`）→ 写入成功，`lab/workspace/draft.txt` 被创建
- 场景 2（写入 `../secrets/demo_secret.txt`）→ 拒绝，`error: path not allowed`

笔记：[docs/notes/week-02/day-02-write-file.md](../docs/notes/week-02/day-02-write-file.md)
