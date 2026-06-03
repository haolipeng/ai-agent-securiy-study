# 阶段验收

每 4 周做一次 checkpoint。未满足当前 checkpoint 时，优先补齐缺口，再进入下一阶段。

样例与笔记约定：

- **Python 概念学习样例**：项目根目录 `day-XX-*/`（如 `day-01-first-call/`）
- **Go Agent / 攻击样例**：`examples/` 或 Code Interpreter Guard 项目骨架内
- **学习笔记**：`docs/notes/week-XX/` 下按天一篇（如 `day-01-first-call.md`）

## 第 4 周 Checkpoint

目标：形成 AI Agent 基础与风险认知。

必须能解释：

- LLM API、message、role、context window、token、streaming
- tool calling 如何从文本变成结构化调用
- Agent loop 和普通 API 调用的区别
- RAG 注入如何污染 prompt 并诱导 tool use
- Prompt Injection、Jailbreak、RAG 注入、工具滥用的区别

必须能跑通：

- Python LLM API 最小样例（`day-01-first-call/` 等 `day-XX-*`）
- Go `read_file` / `write_file` tool calling 样例
- 最小 Agent loop（Go）
- 关键词检索版最小 RAG demo
- 一个恶意文档注入样例
- 一个从 AIRT Lab 02 改写的受控 tool abuse prompt
- 一个从 AIRT Lab 03 改写的 RAG 注入样例

必须产出：

- `day-XX-*` LLM 基础样例（Python）
- `docs/notes/week-01/` ~ `docs/notes/week-04/` 按天笔记
- Go tool calling / 最小 Agent 样例（如 `examples/min-agent/`）
- 关键词检索版 RAG demo（如 `examples/rag-min/`）
- `docs/threat-model.md` 初版
- AIRT 样例迁移记录，说明原始攻击点、改写方式和预期 runtime 行为

## 第 8 周 Checkpoint

目标：形成 Agent runner 与进程/文件观测闭环。

必须能解释：

- runner、agent、event 的职责边界
- tool 执行边界和 task id 的作用
- `execve`、`openat`、`unlink`、`rename` 的安全意义
- 第一版路径解析限制

必须能跑通：

- Agent -> runner -> JSON log
- eBPF 采集 `execve`
- eBPF 采集 `openat`
- MVP 内增强采集 `unlink` / `rename`
- 一次敏感路径访问样例
- 至少一个 AIRT 改写攻击样例触发进程或文件事件

必须产出：

- Code Interpreter Guard 项目骨架
- 统一事件结构初稿
- 进程树审计样例
- 文件访问事件样例
- `examples/attacks/` 中的 AIRT 改写样例索引
- `docs/notes/week-05/` ~ `docs/notes/week-08/` 按天笔记

## 第 12 周 Checkpoint

目标：形成网络观测、task 归因、规则与攻击链检测闭环。

必须能解释：

- IPv4 `connect` 采集点选择
- best-effort task attribution 的边界
- 敏感路径、危险命令、异常外联规则的 evidence 字段
- Agent security 攻击链和普通主机告警的区别

必须能跑通：

- shell/http 外联观测
- process/file/network 统一事件输出
- runner pid + pid/ppid 归因
- task-level 审计报告
- 敏感文件访问后外联的 attack-chain report
- 对至少一个 AIRT 改写样例输出 detection report 或 attack-chain report

必须产出：

- `docs/audit-report-example.md`
- 规则样例
- detection report 样例
- attack-chain report 样例
- AIRT 改写样例的检测覆盖说明
- `docs/notes/week-09/` ~ `docs/notes/week-12/` 按天笔记

## 第 16 周 Checkpoint

目标：形成可公开、可展示、可面试讲解的项目材料。

必须能解释：

- 为什么 Agent runtime security 是自然语言风险到系统行为风险的转换问题
- 为什么 eBPF 适合做 runtime observability
- 第一版为什么选择本地单机、非容器、默认 namespace
- 归因、误报、最小处置的边界和副作用

必须能跑通：

- 1-2 个稳定 demo
- 从根目录 `README.md` 配置环境并复现主流程
- 3-5 分钟演示路径
- 至少一个 demo 来自 AIRT Lab 02/03/08 思路的受控改写

必须产出：

- 根目录 `README.md`（环境准备 + 文档索引）
- 技术文章初稿
- 5 分钟面试讲稿
- 常见问答清单
- `docs/notes/week-16/` 最终复盘记录
- AIRT 到 Code Interpreter Guard 的迁移说明
