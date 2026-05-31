# AI Agent Runtime Security 学习计划

面向 `Agent Runtime Security` 的 16 周学习与项目路线，重点把已有安全工程、`eBPF`、主机安全和 Linux runtime security 能力迁移到 LLM Agent / Tool Use / Code Interpreter 安全。

## 文档入口

- [完整学习路线](docs/ai-agent-security-learning-plan.md)
- [16 周主计划](docs/weekly-plan.md)
- [项目技术方案](docs/code-interpreter-guard-design.md)
- [每次学习会话指南](docs/session-guide.md)
- [学习进度](docs/progress.md)
- [阶段验收](docs/checkpoints.md)
- [安全实验边界](docs/lab-safety.md)
- [可落地性与风险评估](docs/feasibility-and-risks.md)

## 如何继续学习

每次开始学习时：

1. 先读 [每次学习会话指南](docs/session-guide.md)。
2. 查看 [学习进度](docs/progress.md)，确认当前 Week / Day 和状态。
3. 按 [16 周主计划](docs/weekly-plan.md) 执行当前任务。
4. 学习结束后更新进度，并把记录写入 `docs/notes/week-XX.md`。

实际推进以 `docs/progress.md` 的完成状态为准，日期只作为参考；如果上次任务没有完成，下次优先续上。

## 当前建议

先补齐 AI / LLM / Agent 应用基础，再做一个可公开 GitHub 的研究型原型 `Code Interpreter Guard`：

- Go 做 Agent、tool runner、控制面、规则检测和审计输出
- C/libbpf 做数据采集
- 第一版 tool 范围控制在 shell、read_file、write_file、http_get
- 采集进程、文件、网络行为
- 关联 Agent task / tool call
- 做规则检测、攻击链检测、轻量行为基线
- 检测审计优先，最小阻断次之
- 输出审计报告、Demo、技术文章和面试讲稿

## 边界声明

`Code Interpreter Guard` 是本地单机研究型原型，目标是验证 Agent runtime 的观测、归因、审计和检测闭环。

它不是生产级 sandbox、EDR 或 Agent 防火墙；第一版不承诺强隔离、完整阻断、生产级检测准确率，也不覆盖容器、多租户、复杂 namespace、daemon 化绕过等场景。
