# Day 02（Week 02）：实现受控 write_file

**日期：** 2026-06-09  
**代码：** [`day-08-write-file/main.py`](../../../day-08-write-file/main.py)

## 做了什么

基于项目级 `lab/` sandbox，实现受控 `write_file`：LLM 生成 path 和 content，Python 在 `write_allowed_file()` 中先校验路径再写入，只允许 `lab/workspace/` 根目录下的纯文件名。

## 实验环境

| 路径 | 作用 |
|------|------|
| `lab/workspace/draft.txt` | 正常写入靶标（运行后生成） |
| `lab/secrets/demo_secret.txt` | 越权靶标（workspace 外，不应被改写） |

## 关键代码

```python
def write_allowed_file(*, allowed_dir: Path, path: str, content: str) -> dict:
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", ...}

    file_path = allowed_dir / path
    file_path.write_text(content, encoding="utf-8")
    return {"ok": True, "path": str(file_path.resolve()), ...}
```

## LLM 链路

```text
user → tool_calls → json.loads(arguments) → write_allowed_file() → tool result → 最终回答
```

## 实验结果

| 场景 | 结果 | 说明 |
|------|------|------|
| 写入 `draft.txt` | 成功 | 内容写入 workspace |
| 写入 `../secrets/demo_secret.txt` | 拒绝 | 含 `..`，`path not allowed` |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-08-write-file/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- 写操作和读操作一样，path 不可信，必须在执行层校验
- 若不做校验，模型可能配合用户把内容写到 `lab/secrets/` 等敏感位置
- 演示只需一步 path 校验；生产环境可再加 `resolve()` / `is_relative_to()` 防 symlink
- 失败时返回结构化 `error`，便于后续审计和 enforce
