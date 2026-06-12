# Day 10：Agent Loop 骨架

**日期：** 2026-06-11  
**代码：** [`day-10-agent-loop/main.py`](../../../day-10-agent-loop/main.py)  
**公共组件：** [`agent_tools/`](../../../agent_tools/)  
**运行输出：** `day-10-agent-loop/output/agent-run.json`（已 gitignore）

## 做了什么

在 day-09 单次 tool calling 之上，用 `while True` 实现最小 Agent loop：同时注册 `read_file` 和 `write_file`，由模型自主决定调用顺序和次数，直到不再返回 `tool_calls`。

默认任务：读取 `notes.txt`，将其内容写入 `summary.txt`（至少两轮 tool call + 一轮最终回答）。

工具执行层抽到 [`agent_tools/`](../../../agent_tools/)，day-10 只保留 loop 逻辑。

模型：`gpt-3.5-turbo`（Poe）。

## 核心概念

**与 day-09 的区别**

| | day-09 | day-10 |
|--|--------|--------|
| 工具选择 | `tool_choice` 强制指定 | 同时注册两个工具，模型自选 |
| 调用次数 | 固定 1 次 tool call | `while` 循环，可多轮 |
| API 调用 | 两次独立 `create()` | 每轮一次，`messages` 持续累积 |
| 典型任务 | 单步 read 或 write | 多步 read → write |

**observe → plan → act**

每轮 loop 对应：

- **observe** — 收到 user 输入，或上一轮 `role: tool` 的结果
- **plan** — LLM 返回 `tool_calls`（或不再返回 → 结束）
- **act** — `execute_tool()` 受控执行
- **observe** — tool result 写回 `messages`，进入下一轮

**终止条件**

`model_reply.tool_calls` 为空时 `break`，`content` 即最终自然语言回答。

## 关键代码

```python
while True:
    response = client.chat.completions.create(
        messages=messages,
        tools=TOOLS,          # read_file + write_file
        temperature=0,
    )
    model_reply = response.choices[0].message

    if not model_reply.tool_calls:
        break                 # 任务完成

    messages.append(model_reply)
    for tool_call in model_reply.tool_calls:
        tool_result = execute_tool(tool=..., args=json.loads(...))
        messages.append({"role": "tool", "tool_call_id": ..., "content": ...})
```

与 day-09 四阶段的关系：day-09 的「阶段 1–3」= loop 里的一轮；「阶段 4」不再单独开 API，而是 tool result 追加到 `messages` 后继续 loop，直到模型直接给最终回答。

## 输出 JSON 字段

| 字段 | 含义 |
|------|------|
| `user_input` | 用户原始输入 |
| `rounds` | 每轮 tool call 记录（含 iteration、tool、args、result） |
| `final_answer` | 模型最后一轮的自然语言回答 |

## 实测结果

3 轮完成 read → write → 最终回答：

**round 1 — read_file**

```
tool_args: {"path": "notes.txt"}
tool_result: {"ok": true, "content": "这是允许读取的文件。\n..."}
```

**round 2 — write_file**

```
tool_args: {"content": "这是允许读取的文件。\n...", "path": "summary.txt"}
tool_result: {"ok": true, "bytes_written": 81}
```

**round 3 — 无 tool_calls**

```
final_answer: 已成功将 notes.txt 的内容写入 summary.txt 文件中。
```

## 观察小结

- Agent loop = 把 day-09 的单次 pipeline 包进循环，让模型自主编排多步工具调用
- `messages` 是 loop 的状态载体：每轮 append assistant message + tool result，上下文越来越长
- 工具实现复用 `agent_tools`，loop 代码只关心「何时调 API、何时 break」

完整链路：

```text
user_input
  → round 1: plan → read_file → observe
  → round 2: plan → write_file → observe
  → round 3: plan → 无 tool_calls → final_answer
```

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-10-agent-loop/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- **多轮 = 攻击面扩大**：模型每一步都可能生成越权 path；每轮都必须走同样的执行层校验（`agent_tools`）
- **loop 需要可审计**：`rounds` 日志记录每步调了什么工具、传了什么参数、结果如何
- **终止仅靠模型自觉**：生产环境通常还要加 `max_iterations` 等兜底，防止无限 tool call
