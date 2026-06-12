# Day 06：解析 Tool Args

**日期：** 2026-06-05  
**代码：** [`main.py`](../../../day-06-tool-args/main.py)

## 做了什么

day-05 解决「模型怎么看到工具、怎么生成 tool_calls」；day-06 聚焦 **tool args 到达执行层之后**怎么处理。

本 demo 用 `tool_choice` 强制调用 `read_file`，演示三步：

1. 从 `tool_call.function.arguments` 取出 JSON 字符串
2. `json.loads()` 解析成 dict
3. **读盘前**用 `resolve()` + `is_relative_to()` 校验路径，只允许 workspace 内文件

在临时目录创建 `workspace/notes.txt`，跑通允许路径的正常读取。

模型：`gpt-3.5-turbo`（Poe）。

## 核心概念

**arguments 是字符串，不是 dict**

模型返回的 `tool_call.function.arguments` 是 JSON **字符串**，例如 `{"path": "notes.txt"}`。Python 必须 `json.loads()` 后才能当 dict 用——这是 schema（day-05）到 runtime 执行之间的第一步。

**parameters 只管填参形状，不管权限**

day-05 的 `parameters` 告诉 LLM 调用时传什么参数，但**不能**阻止模型生成 `../secret.txt`、绝对路径等危险值。这些要在执行层拒绝。

**路径校验**

```python
path = (workspace / args["path"]).resolve()
if not path.is_relative_to(workspace.resolve()):
    # 拒绝
```

先 `resolve()` 消掉 `../`，再检查最终路径是否仍在 workspace 内；通过后才 `read_text()`。

## 实验设计

```python
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "请读取 notes.txt"}],
    tools=[tool_schema],
    tool_choice={"type": "function", "function": {"name": "read_file"}},
    temperature=0,
)

raw_args = tool_call.function.arguments   # JSON 字符串
args = json.loads(raw_args)               # dict

path = (workspace / args["path"]).resolve()
if not path.is_relative_to(workspace.resolve()):
    print("拒绝：路径越权")
    return

print(path.read_text())
```

与 day-05 的区别：`tool_choice` **强制**走 `read_file`，本课只关心参数解析和校验，不讨论模型选哪个工具。

## 实测结果

```
--- 模型生成的原始参数 ---
{"path": "notes.txt"}

--- Python 解析后的参数 ---
{'path': 'notes.txt'}

--- 读取结果 ---
这是允许读取的文件。
```

模型生成纯文件名 `notes.txt`，resolve 后落在临时 workspace 内，校验通过，读取成功。

若模型生成 `{"path": "../secret.txt"}`，同样代码会在 `is_relative_to` 处拒绝，不会读盘。

## 观察小结

```text
tool_call.function.arguments (JSON 字符串)
  → json.loads() → dict
  → resolve() + is_relative_to() 路径校验
  → 通过后才 read_text()
```

- schema / parameters 约束模型「参数长什么样」；路径是否越界由 runtime 校验
- day-06 用 `tempfile` 自包含实验；day-07 起改用项目级 `lab/workspace/`，校验逻辑相同

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-06-tool-args/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- **不信任模型生成的 args**：即使 temperature=0，prompt injection 仍可能诱导异常 path
- **原始 arguments 应进审计日志**：便于对比「模型说了什么」和「执行层实际做了什么」
- **校验失败也应回传 tool result**（如 `{"ok": false, "error": "..."}`），而不是静默吞掉——day-09 起会系统化记录
