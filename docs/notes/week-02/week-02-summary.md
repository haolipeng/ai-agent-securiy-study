# Week 02 总结

**日期：** 2026-06-13（复盘）  
**代码与笔记：**

- [`day-07-read-file/`](../../../day-07-read-file/) … [`day-10-agent-loop/`](../../../day-10-agent-loop/)
- 公共组件：[`agent_tools/`](../../../agent_tools/)
- 笔记索引：[week-02/README.md](README.md)

## 做了什么

Week 02 在 Week 01 tool 入门之上，走完「受控工具 → 链路日志 → Agent loop」：

| Day | 里程碑 |
|-----|--------|
| 07 | 项目级 `lab/workspace` 沙箱 + 受控 `read_file` |
| 08 | 受控 `write_file`，读写对称的路径校验 |
| 09 | 四阶段 tool calling 链路 + 结构化 trace 日志 |
| 10 | `while` Agent loop，模型自主多轮选工具；执行层抽到 `agent_tools/` |
| 11 | 受控 `run_shell_command`（单次 tool call）；allowlist 仅 `echo`/`ls`；`rm` 拒绝 |

演进线：

```text
单次 tool call + 强制 tool_choice (07/08/09)
  → 结构化 trace (09)
    → 多轮 loop + 模型自选工具 (10)
```

## Grill Me 自检

**Q1：day-09 和 day-10 的本质区别是什么？**  
推荐答案：day-09 每次只跑一个 tool、用 `tool_choice` 强制指定；day-10 同时注册多个 tool，用 loop 让模型自己决定调几次、调哪个，直到不再返回 `tool_calls`。

**Q2：observe / plan / act 在 loop 里怎么对应？**  
推荐答案：observe = 收到 user 或 tool result；plan = LLM 返回 `tool_calls`；act = runtime 执行工具；tool result 写回 messages 后进入下一轮 observe。

**Q3：为什么 path 必须在执行层校验？**  
推荐答案：模型可能生成 `../secrets/...`，schema 只要求 `path: string`，不会阻止越权。校验要在 `resolve()` + 目录白名单里做。

**Q4：trace 里为什么要记 tool_args 和 tool_result？**  
推荐答案：审计需要还原「模型请求了什么」和「执行层实际做了什么」，两者可能不一致（如 path 被拒绝）。

**Q5：Agent loop 带来了什么新攻击面？**  
推荐答案：多轮意味着多次 tool 决策机会；`messages` 越来越长，可能挤占 context window；需要可审计的多轮日志和终止兜底。

## 安全视角

Week 02 的核心结论：**自然语言 → tool_calls → runtime 执行** 这条链上，唯一可信的是执行层的校验与日志，不是模型的参数输出。

- day-07/08：path 不可信，读写都要 allowlist
- day-09：结构化 trace 是后续 enforce 的基础
- day-10：loop 放大步数与上下文，每轮仍需同样校验；`agent_tools/` 作为执行层单一来源

## 下周连接点

Week 02 剩余：加入受控 `run_shell_command`（命令滥用攻击面）。Week 03 起：`task_id`、更细的工具日志、整理 `examples/min-agent/` 样例。
