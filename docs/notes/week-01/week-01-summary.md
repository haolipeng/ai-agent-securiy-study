# Week 01 总结

**日期：** 2026-06-06（复盘）  
**代码与笔记：**

- LLM 基础：[`day-01-first-call/`](../../../day-01-first-call/) … [`day-04-temperature-streaming/`](../../../day-04-temperature-streaming/)
- Tool 入门：[`day-05-tool-schema/`](../../../day-05-tool-schema/)、[`day-06-tool-args/`](../../../day-06-tool-args/)
- 笔记索引：[week-01/README.md](README.md)

## 做了什么

Week 01 完成两条线：

**LLM API 最小闭环** — 从一次普通调用开始，逐步覆盖 role、history、context window、token、temperature 和 streaming。

**Tool Calling 入门** — 理解 tool schema 如何注册给模型、模型如何生成 `tool_calls`，以及 Python 侧如何解析 args 并在执行前校验。

LLM 应用的最小组成：

```text
client -> model -> messages -> parameters -> response -> usage/logs
```

Tool calling 在之上追加：

```text
tools schema -> tool_calls -> json.loads(args) -> runtime 校验与执行
```

## Grill Me 自检

**Q1：如果只能记录一个输入对象，应该记录什么？**  
推荐答案：记录完整 `messages`，而不是只记录最后一条 user prompt。因为 system、assistant history 和前文 tool result 都会影响模型行为。

**Q2：system prompt 为什么像安全策略？**  
推荐答案：它定义模型身份、边界和输出规则。它不是强制隔离机制，但在 LLM 应用层承担策略输入角色，所以需要版本化、审计和防篡改。

**Q3：为什么 context window 是安全问题？**  
推荐答案：history、RAG 文档和 tool result 会消耗 token，挤掉早期关键信息。超出窗口后，模型可能遗忘规则或事实，并编造看似可信的回答。

**Q4：temperature 对安全检测有什么影响？**  
推荐答案：高 temperature 会让输出更发散，甚至破坏格式。安全判定、结构化抽取、tool call 参数生成应使用低 temperature，并做 schema 校验。

**Q5：streaming 的审计风险是什么？**  
推荐答案：流式输出需要逐 chunk 拼接。连接中断或提前落库会导致日志不完整，因此审计记录应标记流是否完整结束。

**Q6：tool schema 和权限控制是什么关系？**  
推荐答案：schema 只描述参数形状，告诉 LLM 怎么填单；路径、命令等是否允许执行，必须在 runtime 执行层校验。

## 安全视角

LLM 调用不是一次普通文本问答，而是一个可审计的运行时事件。审计时应记录 `model`、`messages`、`temperature`、`stream`、`usage`、完整 response；进入 tool calling 后还要记录 tool name、args 和 tool result。

模型生成的 tool args **不可信**——schema 约束的是输出格式，不是安全边界。

## 下周连接点

Week 02 在 `lab/workspace` 固定沙箱里实现受控 `read_file` / `write_file`，记录完整调用链路，再包一层 Agent loop。重点追问：每一步 tool call 是否都经过同样的执行层校验？多轮 loop 里 `messages` 如何累积？
