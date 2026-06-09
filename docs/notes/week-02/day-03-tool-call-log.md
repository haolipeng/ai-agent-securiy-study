# Day 03（Week 02）：记录完整 tool calling 链路

**日期：** 2026-06-10  
**代码：** [`day-09-tool-call-log/main.py`](../../../day-09-tool-call-log/main.py)  
**数据结构样例：** [`day-09-tool-call-log/sample-traces.json`](../../../day-09-tool-call-log/sample-traces.json)

## 做了什么

新建 `day-09-tool-call-log/`，跑 4 条 read/write tool calling，把 user_input、tool_args、tool_result 写入 `output/tool-call-traces.json`；仓库留 `sample-traces.json` 作固定样例。

## trace 字段

| 字段 | 含义 |
|------|------|
| `tool` / `tool_name` | 调用的工具名 |
| `scenario` | 场景标识（read_ok / read_denied / write_ok / write_denied） |
| `user_input` | 用户原始输入 |
| `tool_args` | 模型生成并经 `json.loads` 解析后的参数 |
| `tool_result` | 执行层 `read_allowed_file` / `write_allowed_file` 的返回 |

不含 `tool_args_raw`、`final_answer`（阶段 4 仍执行，但不进 trace）。

## 四阶段链路

```text
user_input
  → 阶段 1：LLM 返回 tool_calls
  → 阶段 2：json.loads → tool_args
  → 阶段 3：受控执行 → tool_result
  → 阶段 4：role: tool 回传 → 最终回答（不写入 trace）
```

## 实验结果

| scenario | tool_result | 路径风险 |
|----------|-------------|----------|
| read_ok | ok | 无，`notes.txt` 在 workspace 内 |
| read_denied | path not allowed | 模型生成 `../secrets/...`，执行层拒绝 |
| write_ok | ok | 无，写入 workspace |
| write_denied | path not allowed | 模型配合越权 path，执行层拒绝 |

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-09-tool-call-log/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- **tool schema**：只描述参数形状，不等于权限控制
- **tool_args**：模型输出不可信，必须解析后再校验
- **tool_result**：结构化记录成功/失败，便于审计；denied 场景的 `error` 即路径风险记录
- 完整链路日志是后续 Agent loop 和 enforce 层的基础
