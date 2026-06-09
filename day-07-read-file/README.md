# Day 07: 受控 read_file

使用项目级 `lab/` sandbox，实现 LLM tool calling + 纯文件名路径校验。

## 实验环境

| 路径 | 作用 |
|------|------|
| `lab/workspace/` | 允许读取的目录 |
| `lab/workspace/notes.txt` | 正常读取靶标 |
| `lab/secrets/demo_secret.txt` | workspace 外的模拟敏感文件 |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-07-read-file/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

## 预期结果

- 场景 1（`notes.txt`）→ 读取成功
- 场景 2（`../secrets/demo_secret.txt`）→ 拒绝，`error: path not allowed`

笔记：[docs/notes/week-02/day-01-read-file.md](../docs/notes/week-02/day-01-read-file.md)
