# 学习进度

## 当前状态

- 起始日期：2026/06/01
- 推进方式：以完成状态推进，日期只作为参考
- 当前阶段：第 1 阶段，AI Agent 基础与风险认知
- 当前周次：第 2 周
- 当前任务：Day 11，加入受控 `run_shell_command`
- 状态：未开始

## 已完成任务

**Week 01 — LLM API 与 Tool Calling 入门**

- Day 01：跑通第一次 LLM API 调用（`day-01-first-call/`）
- Day 02：理解 message 和 role（`day-02-message-role/`）
- Day 03：理解上下文窗口和 token（`day-03-context-window/`）
- Day 04：理解 temperature 和 streaming（`day-04-temperature-streaming/`）
- Day 05：理解 tool schema（`day-05-tool-schema/`）
- Day 06：解析 tool args（`day-06-tool-args/`）

**Week 02 — Tool Calling 与最小 Agent Loop**

- Day 07：实现受控 read_file（`day-07-read-file/`）
- Day 08：实现受控 write_file（`day-08-write-file/`）
- Day 09：记录完整 tool calling 链路（`day-09-tool-call-log/`）
- Day 10：Agent loop 骨架（`day-10-agent-loop/`、`agent_tools/`）

## 当前阻塞

暂无。

## 下次继续

从 Week 02 Day 11 开始：

- 概念：受控 shell 工具与命令滥用攻击面
- 实验：在 Agent loop 上加入 `run_shell_command`，记录输出与退出码
- 记录：`docs/notes/week-02/`

## 最近学习记录

**Week 01**

- [Day 01 笔记](notes/week-01/day-01-first-call.md)
- [Day 02 笔记](notes/week-01/day-02-message-role.md)
- [Day 03 笔记](notes/week-01/day-03-context-window.md)
- [Day 04 笔记](notes/week-01/day-04-temperature-streaming.md)
- [Day 05 笔记](notes/week-01/day-05-tool-schema.md)
- [Day 06 笔记](notes/week-01/day-06-tool-args.md)
- [Week 01 总结](notes/week-01/week-01-summary.md)

**Week 02**

- [Day 07 笔记](notes/week-02/day-07-read-file.md)
- [Day 08 笔记](notes/week-02/day-08-write-file.md)
- [Day 09 笔记](notes/week-02/day-09-tool-call-log.md)
- [Day 10 笔记](notes/week-02/day-10-agent-loop.md)
- [Week 02 总结](notes/week-02/week-02-summary.md)
