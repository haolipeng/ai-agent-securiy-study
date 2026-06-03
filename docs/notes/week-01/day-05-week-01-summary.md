# Day 05：Week 01 总结

**日期：** 2026-06-05  
**代码：**

- [`day-01-first-call/`](../../../day-01-first-call/)
- [`day-02-message-role/`](../../../day-02-message-role/)
- [`day-03-context-window/`](../../../day-03-context-window/)
- [`day-04-temperature-streaming/`](../../../day-04-temperature-streaming/)

## 做了什么

本周完成了 LLM API 的最小闭环：创建 client，选择 model，组织 messages，设置 generation 参数，读取 response，并观察 usage。对应样例从一次普通调用开始，逐步覆盖 role、history、context window、token、temperature 和 streaming。

LLM 应用的最小组成可以概括为：

```text
client -> model -> messages -> parameters -> response -> usage/logs
```

这条链路也是后续 Agent runtime security 的审计主线：输入是什么、策略是什么、模型看到了哪些上下文、参数如何影响输出、最终产生了什么响应。

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

## 安全视角

第一周的关键结论是：LLM 调用不是一次普通文本问答，而是一个可审计的运行时事件。后续做 Agent tool calling 时，必须把 `model`、`messages`、`temperature`、`stream`、`usage`、完整 response 和 tool call 结果一起纳入结构化日志。

否则，当 Agent 出现越权读取、危险命令或异常外联时，很难解释它是被 system 约束失败、上下文污染、截断、随机输出，还是 tool 参数校验缺失导致的。

## 下周连接点

Week 02 进入 Tool Calling。要重点追问：模型生成的 tool name 和 JSON args 是否可信？路径、命令、URL 等参数由谁校验？tool result 又如何进入下一轮 `messages` 并继续影响模型决策？
