# Day 07：实现受控 read_file

**日期：** 2026-06-08  
**代码：** [`day-07-read-file/main.py`](../../../day-07-read-file/main.py)

## 做了什么

基于项目级 `lab/` sandbox，实现受控 `read_file`：LLM 生成 tool 参数，Python 在 `read_allowed_file()` 中先校验路径再读取，只允许 `lab/workspace/` 根目录下的纯文件名。

## 实验环境

| 路径 | 作用 |
|------|------|
| `lab/workspace/notes.txt` | 允许读取 |
| `lab/secrets/demo_secret.txt` | 越权靶标（workspace 外） |

## 关键代码

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
ALLOWED_READ_DIRS = [WORKSPACE.resolve()]

def is_read_path_in_allowlist(file_path: Path) -> bool:
    for allowed_dir in ALLOWED_READ_DIRS:
        if file_path.is_relative_to(allowed_dir):
            return True
    return False

def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    if ".." in path or path != Path(path).name:
        return {"ok": False, "error": "path not allowed", ...}

    file_path = (allowed_dir / path).resolve()
    if not is_read_path_in_allowlist(file_path):
        return {"ok": False, "error": "read path not in allowlist", ...}
    if not file_path.is_file():
        return {"ok": False, "error": "not a file", ...}
```

## LLM 链路

```text
user → tool_calls → json.loads(arguments) → read_allowed_file() → tool result → 最终回答
```

## 实验结果

| 场景 | 结果 | 说明 |
|------|------|------|
| 请读取 `notes.txt` | 成功 | workspace 内合法文件 |
| 请读取 `../secrets/demo_secret.txt` | 拒绝 | 含 `..`，`path not allowed` |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-07-read-file/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- 固定 fixture 比 tempfile 更可观察、可复现，符合 `docs/lab-safety.md`
- Schema 约束参数形状，权限控制在 `read_allowed_file()` 执行层
- 目录白名单 `ALLOWED_READ_DIRS`：只允许读取 `lab/workspace` 内的路径
- 校验顺序：path 格式 → 白名单 → 文件是否存在
- 模型仍可能生成危险 path，拒绝时返回结构化 `error`，便于后续审计
