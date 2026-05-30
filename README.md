# AI Agent Runtime Security 学习计划

面向 `Agent Runtime Security` 的 16 周学习与项目路线，重点把已有安全工程、`eBPF`、主机安全和 Linux runtime security 能力迁移到 LLM Agent / Tool Use / Code Interpreter 安全。

## 文档入口

- [完整学习路线](docs/ai-agent-security-learning-plan.md)
- [16 周按天执行计划](docs/weekly-plan.md)
- [项目技术方案](docs/code-interpreter-guard-design.md)

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
