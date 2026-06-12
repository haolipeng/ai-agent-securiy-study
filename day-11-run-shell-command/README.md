# Day 11: 受控 run_shell_command

单次 tool calling 演示：LLM 生成 shell 命令参数，Python 在 allowlist 校验通过后才用 `subprocess` 执行（不用 `shell=True`）。

## 场景

| scenario | 说明 |
|----------|------|
| `shell_ok` | 模型生成 `ls`，列出 workspace 文件 |
| `shell_denied` | 模型生成 `rm`，执行层拒绝（不在 allowlist） |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-11-run-shell-command/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

## 笔记

[docs/notes/week-02/day-11-run-shell-command.md](../docs/notes/week-02/day-11-run-shell-command.md)

执行层代码：[`agent_tools/shell_tools.py`](../agent_tools/shell_tools.py)
