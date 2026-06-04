# 16 周主计划

## 高优先级事项

https://www.armosec.io/blog/ebpf-based-ai-agent-enforcement/



## AIRT 课程使用方式

本计划把本地 `/home/work/airt` 的 AIRT 课程作为攻击场景素材库，而不是替代主线课程。

使用原则：

- 主线仍然是 `Code Interpreter Guard`：Agent tool use -> runtime behavior -> eBPF 观测 -> task 归因 -> 检测报告。
- AIRT 只用于补攻击面理解、提供 payload 思路、生成受控 demo case。
- 每次最多抽取一个 AIRT lab 的一个攻击点，迁移成当前阶段需要的最小样例。
- 不以拿 flag 或完整刷完 AIRT 为目标，避免偏离 runtime security 主线。
- 所有从 AIRT 迁移的样例都必须转写成受控、本地、脱敏的 `examples/attacks/` 或 `examples/rag-min/` case。

推荐映射：

| AIRT 内容 | 放入本计划的位置 | 迁移目标 |
|---|---|---|
| Lab 02 Prompt Injection | 第 3 周、第 5 周 | 诱导 Agent 调用 `run_shell_command` / `read_file` 的 tool abuse case |
| Lab 03 RAG Exploitation | 第 4 周、第 5 周 | 恶意文档注入后触发 tool call 的 RAG case |
| Lab 04 Multi-Agent Exploitation | 第 5 周、第 12 周 | shared memory / delegation 污染导致工具滥用的攻击链参考 |
| Lab 07 Automation | 第 11-13 周 | prompt injection / RAG 注入回归测试集参考 |
| Lab 08 Full Engagement | 第 15-16 周 | 最终 Demo 攻击链和报告结构参考 |

## 执行约束

- 本文件是唯一主计划，已合并原日历视图。
- 起始日期固定为 2026/06/01。
- 周期：16 周
- 节奏：周一到周五正式学习，周六可选复盘/补漏，周日休息
- 每天投入：2 小时
- 每天结构：30 分钟概念学习 + 60 分钟动手实验 + 30 分钟短记录
- 每周有效学习时间：10 小时
- 原则：每天只完成一个明确闭环，优先形成可运行代码、可复现样例或可提交文档
- 实际推进以 `docs/progress.md` 的完成状态为准，日期只作为参考

## SMART 验收补充规则

每个正式学习日必须留下至少一种可检查证据：

- 可运行代码：示例目录、运行命令、实际输出
- 可复现样例：输入、预期行为、实际结果
- 结构化日志：tool call log、event log、audit report、detection report
- 学习笔记：300-800 字，包含概念、实验、系统安全映射、下一步
- 失败记录：如果未完成，记录当前进度、阻塞点和下次第一步

每周五必须形成一个可检查产物：

- 一个可运行 demo
- 一个样例目录
- 一个 JSON 日志或 report
- 一个设计文档或威胁模型更新

如果某日任务写的是“理解”“能解释”“整理”，必须把它落到笔记、代码、样例、日志或报告之一，不能只停留在阅读。

## 每日短记录模板

每天最后 30 分钟回答：

- 今天学到的 AI / Agent 概念是什么？
- 它对应到系统安全里的什么对象？
- 今天做了哪个最小实验？
- 这个实验暴露了什么攻击面或防护点？

更完整的笔记规范见 `docs/notes/README.md`。

## MVP 边界

必达闭环：

- Go 最小 Agent 支持 `run_shell_command`、`read_file`、`write_file`、`http_get`
- runner 记录 task / tool call 日志，并传递 `task_id`
- eBPF 采集 `execve`、`openat`、IPv4 `connect`
- Go aggregator 基于 runner pid、pid/ppid、进程树做 best-effort task 归因
- detector 输出敏感文件访问、危险命令、异常外联、敏感文件后外联报告

MVP 内增强：

- 采集 `unlink`
- 采集 `rename`

增强项，不作为 MVP 成败标准：

- 轻量行为基线
- `kill` / enforce
- runner 工作目录、环境变量、timeout、输出大小限制等最小处置能力

## 第一阶段：AI Agent 基础与风险认知（第 1-4 周）

阶段目标：补齐 LLM API、tool calling、Agent loop 和最小 RAG 基础，理解 Prompt Injection、RAG 注入和工具滥用如何转成 runtime security 风险。

## 第 1 周（2026/06/01 - 2026/06/07）：LLM API 和基础概念 / Tool Calling 基础

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

#### 原第 1 周主题：LLM API 和基础概念

目标：从安全工程视角理解 LLM 应用的基本对象。

### 周一（2026/06/01）：跑通第一次 LLM API 调用

- 概念：LLM API、model、request、response
- 实验：用 Python 调用一次云端 LLM API（样例：`day-01-first-call/`）
- 记录：安全边界

### 周二（2026/06/02）：理解 message 和 role

- 概念：system、user、assistant message
- 实验：修改不同 role 的内容，观察输出变化
- 记录：system prompt 为什么像策略输入

补一个思维导图，解释清楚system、user、assistant message的区别

### 周三（2026/06/03）：理解上下文窗口、token、temperature 和 streaming

- 概念：context window、token、截断
- 实验：构造长输入，观察模型响应变化
- 记录：上下文污染和日志留存风险

- 概念：temperature、determinism、streaming
- 实验：比较不同 temperature 和 streaming 输出
- 记录：安全检测为什么需要结构化日志

#### 原第 1 周验收标准

- 能解释 LLM API、message、role、context window、token、temperature、streaming 的基本含义
- 能运行一次 Python LLM API 调用
- 产出 `day-XX-*` 样例目录和 `docs/notes/week-01/`

#### 原第 2 周主题：Tool Calling 基础

目标：理解模型如何从文本生成结构化 tool call。

相关参考资料：

工具调用详解：人工智能代理的核心

https://composio.dev/content/ai-agent-tool-calling-guide

### 周四（2026/06/04）：理解 tool schema

- 概念：tool name、description、parameters
- 实验：定义 `read_file` 的 Go 结构体和 schema
- 记录：tool schema 为什么是攻击面

### 周五（2026/06/05）：解析 tool args

- 概念：结构化参数、JSON schema、参数校验
- 实验：让模型生成 `read_file` 参数并在 Go 侧解析
- 记录：参数校验和越权路径风险

### 周六（2026/06/06）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/06/07）：休息

- 不安排正式学习任务

## 第 2 周（2026/06/08 - 2026/06/14）：Tool Calling 基础 / 最小 Agent Loop

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/06/08）：实现 `read_file`

- 概念：tool result、错误返回、最小权限
- 实验：实现受控 `read_file`
- 记录：文件读取对应的系统安全对象

### 周二（2026/06/09）：实现 `write_file`

- 概念：写操作风险、覆盖、路径穿越
- 实验：实现受控 `write_file`
- 记录：写文件工具的防护点

### 周三（2026/06/10）：记录完整 tool calling 链路

- 概念：prompt -> tool call -> tool result -> final answer
- 实验：输出完整调用日志
- 记录：tool calling 数据结构样例

#### 原第 2 周验收标准

- 能解释 tool schema、tool args、tool result 和参数校验的安全意义
- 能跑通 `read_file` 和 `write_file` 的最小 tool calling 链路
- 产出 tool calling 数据结构样例和路径风险记录

#### 原第 3 周主题：最小 Agent Loop

目标：手写一个最小 Agent，理解 observe -> plan -> act -> observe。

AIRT 参考：只看 Lab 02 的 Prompt Injection 思路，用来理解恶意自然语言如何影响 Agent 决策；本周不追求跑完整 Lab 02。

### 周四（2026/06/11）：实现 Agent loop 骨架

- 概念：observe、plan、act、observe loop
- 实验：用 Go 写最小 Agent loop
- 记录：Agent 和普通 API 调用的区别

### 周五（2026/06/12）：加入 `run_shell_command`

- 概念：命令执行工具、stdout/stderr、exit code
- 实验：实现受控 shell command tool
- 记录：自然语言到 `execve` 的转换链路；从 AIRT Lab 02 抽取一个 prompt injection 思路，改写成受控 shell tool abuse 样例

### 周六（2026/06/13）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/06/14）：休息

- 不安排正式学习任务

## 第 3 周（2026/06/15 - 2026/06/21）：最小 Agent Loop / RAG 和上下文污染

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/06/15）：加入 `task_id`

- 概念：task、session、tool call id
- 实验：给每次 Agent 调用分配 `task_id`
- 记录：为什么安全审计需要 task 归因

### 周二（2026/06/16）：记录 tool call 运行细节

- 概念：输入、输出、错误、耗时、状态码
- 实验：输出结构化 tool call 日志
- 记录：审计字段初稿

### 周三（2026/06/17）：整理最小 Agent 样例

- 概念：Agent runtime 的最小边界
- 实验：整理 `examples/min-agent/`
- 记录：Agent 执行日志样例

#### 原第 3 周验收标准

- 能解释 Agent loop 和普通 API 调用的区别
- 能跑通最小 Agent loop、`run_shell_command` 和 task id 日志
- 产出 `examples/min-agent/`、Agent 执行日志样例和 1 个从 AIRT Lab 02 改写的受控 tool abuse prompt

#### 原第 4 周主题：RAG 和上下文污染

目标：理解 RAG 的基本链路和安全风险，不深入向量库工程。

AIRT 参考：只看 Lab 03 的 RAG poisoning / indirect prompt injection 思路；本计划仍使用关键词检索版最小 RAG，不引入 ChromaDB 和 LangChain 作为主线依赖。

### 周四（2026/06/18）：实现最小文档加载

- 概念：document、chunk、context
- 实验：读取本地文本并切分 chunk
- 记录：外部文档如何进入上下文

### 周五（2026/06/19）：实现最小检索

- 概念：retrieve、top-k、相关性
- 实验：用关键词检索代替复杂向量库
- 记录：检索结果为什么会污染 prompt

### 周六（2026/06/20）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/06/21）：休息

- 不安排正式学习任务

## 第 4 周（2026/06/22 - 2026/06/28）：RAG 和上下文污染 / Agent 攻击样例

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/06/22）：把检索结果拼入 prompt

- 概念：RAG prompt template
- 实验：把 chunk 注入 LLM 上下文并生成回答
- 记录：RAG 链路的信任边界

### 周二（2026/06/23）：构造恶意文档注入

- 概念：RAG Prompt Injection
- 实验：参考 AIRT Lab 03 的 poisoned document，把恶意文档改写成诱导 Agent 调用 tool 的本地样例
- 记录：文档输入如何变成系统行为；记录和 AIRT 原始 RAG lab 的差异

### 周三（2026/06/24）：整理威胁模型初版

- 概念：Prompt Injection、Jailbreak、RAG 注入、工具滥用
- 实验：对比 4 类风险样例
- 记录：`docs/threat-model.md` 初版

#### 原第 4 周验收标准

- 能解释最小 RAG 链路和 RAG prompt injection 风险
- 能跑通关键词检索版 RAG demo 和恶意文档注入样例
- 产出 `docs/threat-model.md` 初版和 1 个从 AIRT Lab 03 改写的 RAG 注入 case

#### 原第 5 周主题：Agent 攻击样例

目标：把 AI 风险转成真实系统行为。

AIRT 参考：集中整理 Lab 02、Lab 03、Lab 04 的攻击点，但只迁移能落到 shell/file/http tool 的最小样例。

### 周四（2026/06/25）：构造 Prompt Injection 样例

- 概念：指令覆盖、间接注入、上下文污染
- 实验：参考 AIRT Lab 02，诱导 Agent 偏离原始任务并调用受控 tool
- 记录：攻击前置条件；原始 prompt、tool call、预期 runtime 行为

### 周五（2026/06/26）：构造敏感文件读取样例

- 概念：越权文件访问、敏感路径
- 实验：读取 `/etc/passwd`、模拟 SSH key、模拟云凭证
- 记录：敏感路径规则草案

### 周六（2026/06/27）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/06/28）：休息

- 不安排正式学习任务

## 第二阶段：攻击样例、项目骨架与 eBPF 观测（第 5-8 周）

阶段目标：把 AI 风险转成真实系统行为，建立项目骨架，并完成进程和文件观测的基础闭环。

## 第 5 周（2026/06/29 - 2026/07/05）：Agent 攻击样例 / Go Tool Runner 和项目骨架

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/06/29）：构造网络外联样例

- 概念：数据外传、allowlist、外联审计
- 实验：参考 AIRT Lab 03/08 的 exfil 思路，用 `http_get` 或 shell 触发受控外联
- 记录：外联检测字段草案；区分 tool 层 URL 和系统层 connect 事件

### 周二（2026/06/30）：构造受控资源滥用样例

- 概念：CPU、memory、pids、fork bomb 风险
- 实验：运行受控资源压测样例
- 记录：资源限制需求

### 周三（2026/07/01）：整理攻击链

- 概念：prompt -> tool call -> process -> syscall
- 实验：把 4 类样例整理到 `examples/attacks/`，并标注来源是 AIRT Lab 02/03/04 的改写还是自定义样例
- 记录：攻击链说明；每条链必须写清楚 prompt/task/tool/runtime evidence

#### 原第 5 周验收标准

- 能解释 Prompt Injection、敏感文件读取、外联和资源滥用的攻击前置条件
- 能跑通 4 类受控攻击样例
- 产出 `examples/attacks/`、AIRT 改写样例索引和攻击链说明

#### 原第 6 周主题：Go Tool Runner 和项目骨架

目标：把实验样例收敛成 `Code Interpreter Guard` 项目骨架。

### 周四（2026/07/02）：建立项目目录

- 概念：guard、runner、agent、event 的职责
- 实验：创建 `cmd/guard`、`cmd/runner`、`pkg/*`
- 记录：目录结构说明

### 周五（2026/07/03）：固化 tool runner

- 概念：tool 执行边界、工作目录、超时
- 实验：把 shell/file/http tools 接入 runner
- 记录：runner 责任边界

### 周六（2026/07/04）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/07/05）：休息

- 不安排正式学习任务

## 第 6 周（2026/07/06 - 2026/07/12）：Go Tool Runner 和项目骨架 / eBPF 进程观测

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/07/06）：定义 task 和 tool call 结构

- 概念：task id、tool call id、parent relation
- 实验：实现 Go 数据结构
- 记录：归因字段设计

### 周二（2026/07/07）：定义 event 结构

- 概念：process/file/network event
- 实验：实现统一 JSON event 类型
- 记录：事件字段设计

### 周三（2026/07/08）：跑通最小项目闭环

- 概念：Agent -> runner -> JSON log
- 实验：输出一次完整 task 日志
- 记录：第一个端到端样例

#### 原第 6 周验收标准

- 能解释 guard、runner、agent、event 的职责边界
- 能跑通 Agent -> runner -> JSON log 的最小闭环
- 产出项目骨架、task/tool call 结构和统一 event 结构初稿

#### 原第 7 周主题：eBPF 进程观测

目标：采集 Agent 触发的进程执行行为。

### 周四（2026/07/09）：搭建 libbpf 骨架

- 概念：tracepoint/kprobe、ringbuf/perfbuf
- 实验：创建 `ebpf/exec.bpf.c`
- 记录：采集点选择

### 周五（2026/07/10）：采集 `execve`

- 概念：exec 行为、argv、comm
- 实验：捕获进程执行事件
- 记录：从 shell tool 到 exec 事件

### 周六（2026/07/11）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/07/12）：休息

- 不安排正式学习任务

## 第 7 周（2026/07/13 - 2026/07/19）：eBPF 进程观测 / eBPF 文件观测

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/07/13）：补充进程上下文

- 概念：pid、ppid、uid、gid、argv
- 实验：补充第一版进程事件字段
- 记录：进程归因字段；`cgroup/container id` 作为后续增强

### 周二（2026/07/14）：Go 侧消费事件

- 概念：用户态聚合、事件解码
- 实验：`cmd/guard observe` 输出 exec 事件
- 记录：eBPF 到 Go 的数据流

### 周三（2026/07/15）：还原进程树

- 概念：process tree、parent-child relation
- 实验：按 `pid/ppid` 还原一次 Agent task
- 记录：进程树审计输出

#### 原第 7 周验收标准

- 能解释 `execve` 采集点、进程上下文和进程树审计价值
- 能跑通 eBPF `execve` 采集和 Go 侧消费
- 产出进程事件字段和进程树审计样例

#### 原第 8 周主题：eBPF 文件观测

目标：采集文件访问和文件修改行为。

### 周四（2026/07/16）：采集 `openat`

- 概念：文件打开、路径、权限
- 实验：捕获 `openat` 事件
- 记录：文件读取和敏感路径

### 周五（2026/07/17）：测试 `openat` 路径语义

- 概念：相对路径、绝对路径、cwd、dfd
- 实验：测试 `openat` 在不同路径输入下的事件表现
- 记录：第一版路径解析限制；`openat2` 作为后续增强

### 周六（2026/07/18）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/07/19）：休息

- 不安排正式学习任务

## 第 8 周（2026/07/20 - 2026/07/26）：eBPF 文件观测 / eBPF 网络观测

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/07/20）：采集 `unlink`

- 概念：文件删除风险
- 实验：捕获删除事件
- 记录：破坏性操作审计

### 周二（2026/07/21）：采集 `rename`

- 概念：文件重命名、覆盖、规避
- 实验：捕获重命名事件
- 记录：修改类事件字段

### 周三（2026/07/22）：验证敏感路径访问

- 概念：敏感路径检测前置数据
- 实验：用攻击样例触发文件事件
- 记录：文件访问事件样例

#### 原第 8 周验收标准

- 能解释 `openat`、`unlink`、`rename` 的安全意义和路径语义限制
- 能跑通文件访问、删除、重命名事件采集
- 产出文件访问事件样例和路径解析限制记录

#### 原第 9 周主题：eBPF 网络观测

目标：采集 Agent 触发的网络外联行为。

### 周四（2026/07/23）：选择网络采集点

- 概念：connect、目标 IP、端口
- 实验：确定采集字段
- 记录：网络事件设计

### 周五（2026/07/24）：采集 `connect`

- 概念：外联行为
- 实验：捕获 TCP connect 事件
- 记录：外联事件样例

### 周六（2026/07/25）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/07/26）：休息

- 不安排正式学习任务

## 第三阶段：网络观测、归因、规则与攻击链检测（第 9-12 周）

阶段目标：完成网络观测、best-effort task 归因、规则检测和 Agent security 攻击链报告。

## 第 9 周（2026/07/27 - 2026/08/02）：eBPF 网络观测 / Task 归因和审计报告

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/07/27）：补充进程上下文

- 概念：网络事件归因
- 实验：关联 pid、comm
- 记录：外联和进程关系；`cgroup/netns/container context` 作为后续增强

### 周二（2026/07/28）：统一三类事件 JSON

- 概念：process/file/network event schema
- 实验：统一事件输出格式
- 记录：统一事件字段

### 周三（2026/07/29）：验证 shell 和 http 外联

- 概念：tool 层外联和系统层外联
- 实验：分别用 `http_get` 和 shell 触发外联
- 记录：网络观测验证结果

#### 原第 9 周验收标准

- 能解释 IPv4 `connect` 采集字段和网络事件归因需求
- 能跑通 shell/http 外联观测和 process/file/network 统一 JSON 输出
- 产出网络事件样例和网络观测验证记录

#### 原第 10 周主题：Task 归因和审计报告

目标：把应用侧 task / tool call 和系统侧事件连起来。

### 周四（2026/07/30）：定义 task id 生命周期

- 概念：task start、tool call、task end
- 实验：固化 task id 生成和结束逻辑
- 记录：task 生命周期说明

### 周五（2026/07/31）：传递 task id 到 runner

- 概念：环境变量、wrapper 参数、继承关系
- 实验：通过 env 或 argv 传递 task id
- 记录：传递方式取舍

### 周六（2026/08/01）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/08/02）：休息

- 不安排正式学习任务

## 第 10 周（2026/08/03 - 2026/08/09）：Task 归因和审计报告 / 规则检测

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/08/03）：关联进程事件

- 概念：task -> process tree
- 实验：把 exec 事件归因到 task
- 记录：进程归因样例

### 周二（2026/08/04）：关联文件和网络事件

- 概念：task -> file/network behavior
- 实验：把 file/network 事件归因到 task
- 记录：行为归因样例

### 周三（2026/08/05）：输出 task-level 审计报告

- 概念：审计报告、可复现证据
- 实验：生成 JSON report
- 记录：`docs/audit-report-example.md`

#### 原第 10 周验收标准

- 能解释 task id 生命周期和 best-effort task attribution 边界
- 能把进程、文件、网络事件归因到同一 task
- 产出 task-level JSON 审计报告和 `docs/audit-report-example.md`

#### 原第 11 周主题：规则检测

目标：实现最小可用检测能力。

AIRT 参考：从前期迁移的 AIRT 攻击样例中挑选稳定 case，作为规则检测的回归输入；不引入自动化红队工具作为 MVP 必需项。

### 周四（2026/08/06）：设计规则格式

- 概念：condition、severity、reason、evidence
- 实验：定义 `rules/*.yaml`
- 记录：规则格式说明

### 周五（2026/08/07）：实现敏感路径规则

- 概念：path match、home dir、云凭证
- 实验：检测 `/etc/shadow`、`~/.ssh`、模拟云凭证
- 记录：敏感路径检测样例

### 周六（2026/08/08）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/08/09）：休息

- 不安排正式学习任务

## 第 11 周（2026/08/10 - 2026/08/16）：规则检测 / 攻击链检测

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/08/10）：实现危险命令规则

- 概念：危险命令、命令组合、管道
- 实验：检测 `nc`、`curl | sh`、`chmod +s`
- 记录：危险命令规则样例

### 周二（2026/08/11）：实现异常网络规则

- 概念：allowlist、unknown destination
- 实验：检测非 allowlist 外联
- 记录：异常网络规则样例

### 周三（2026/08/12）：输出检测报告

- 概念：风险等级、触发原因、证据
- 实验：对至少 1 个 AIRT 改写样例生成 detection report
- 记录：检测报告样例；说明命中的规则和未覆盖风险

#### 原第 11 周验收标准

- 能解释规则 condition、severity、reason、evidence 的设计
- 能跑通敏感路径、危险命令、异常外联检测
- 产出规则样例和 detection report

#### 原第 12 周主题：攻击链检测

目标：做出 Agent Security 特色分析，而不是普通主机告警。

AIRT 参考：用 Lab 04 的 shared memory / delegation 污染和 Lab 08 的 full engagement 思路，帮助设计 timeline 表达；本周只实现单机单 runner 的 attack-chain report。

### 周四（2026/08/13）：串联 prompt 和 tool call

- 概念：意图层信号
- 实验：保存 prompt 和 tool call 映射
- 记录：prompt 证据字段

### 周五（2026/08/14）：串联系统事件

- 概念：行为层证据
- 实验：把 exec/file/network 纳入同一 task timeline
- 记录：timeline 样例

### 周六（2026/08/15）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/08/16）：休息

- 不安排正式学习任务

## 第 12 周（2026/08/17 - 2026/08/23）：攻击链检测 / 行为基线轻量版

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/08/17）：实现敏感文件意图规则

- 概念：prompt 请求敏感文件
- 实验：检测 prompt 层敏感意图
- 记录：意图规则样例

### 周二（2026/08/18）：实现实际访问规则

- 概念：tool 实际访问敏感文件
- 实验：检测文件事件层敏感访问
- 记录：行为规则样例

### 周三（2026/08/19）：实现外联组合规则

- 概念：敏感文件访问后外联
- 实验：用 AIRT 改写样例生成 attack-chain report
- 记录：攻击链报告样例；说明从 AI 输入到 runtime evidence 的完整链路

#### 原第 12 周验收标准

- 能解释意图层信号、行为层证据和 attack-chain timeline
- 能跑通敏感文件访问后外联的组合规则
- 产出 attack-chain report 和 timeline 样例

#### 原第 13 周主题：行为基线轻量版

目标：补充研究深度，但不做复杂异常检测平台。

### 周四（2026/08/20）：定义正常任务集合

- 概念：benign task、baseline scope
- 实验：定义数学计算、文件处理、数据分析任务
- 记录：正常任务清单

### 周五（2026/08/21）：采集正常进程行为

- 概念：正常进程集合
- 实验：运行正常任务并采集 exec
- 记录：进程基线样例

### 周六（2026/08/22）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/08/23）：休息

- 不安排正式学习任务

## 第四阶段：基线/处置增强、公开发布与表达材料（第 13-16 周）

阶段目标：补充研究深度和最小处置能力，把项目整理成可公开、可演示、可面试讲解的材料。

## 第 13 周（2026/08/24 - 2026/08/30）：行为基线轻量版 / Runner 边界和最小处置

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/08/24）：采集正常文件和网络行为

- 概念：正常文件路径、正常外联
- 实验：采集 file/network 行为
- 记录：文件和网络基线样例

### 周二（2026/08/25）：实现简单偏离检测

- 概念：rare process/path/destination
- 实验：检测偏离正常集合的行为
- 记录：偏离检测样例

### 周三（2026/08/26）：记录误报和漏报

- 概念：false positive、false negative
- 实验：用正常样例和攻击样例验证
- 记录：`docs/baseline.md`

#### 原第 13 周验收标准

- 能解释 benign task、baseline scope、false positive、false negative
- 能跑通轻量 allowlist / rare behavior heuristic
- 产出 `docs/baseline.md`，但该能力不作为 MVP 成败标准

#### 原第 14 周主题：Runner 边界和最小处置

目标：检测审计优先，补一个可演示的最小处置闭环。

### 周四（2026/08/27）：设计运行模式

- 概念：observe、alert、enforce
- 实验：实现模式参数
- 记录：模式语义说明

### 周五（2026/08/28）：实现高危 kill

- 概念：进程处置、副作用
- 实验：高危规则触发后 kill 相关进程
- 记录：kill 处置边界

### 周六（2026/08/29）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/08/30）：休息

- 不安排正式学习任务

## 第 14 周（2026/08/31 - 2026/09/06）：Runner 边界和最小处置 / 公开项目整理

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/08/31）：限制 runner 环境变量和工作目录

- 概念：working directory、env、tmp dir
- 实验：限制 runner 的工作目录、环境变量和临时目录
- 记录：本地单机 runner 基础边界说明

### 周二（2026/09/01）：加入 timeout 和输出大小限制

- 概念：执行超时、stdout/stderr 上限、响应大小上限
- 实验：为 shell/http tool 加 timeout 和输出大小限制
- 记录：资源滥用处置边界

### 周三（2026/09/02）：整理 runner 边界设计

- 概念：本地单机、非容器、默认 namespace 的边界
- 实验：验证 kill、timeout、工作目录、环境变量限制
- 记录：`docs/runner-boundary.md`；seccomp、namespace、cgroup、容器归因作为后续增强

#### 原第 14 周验收标准

- 能解释 observe、alert、enforce 的模式语义和副作用
- 能演示 kill、timeout、工作目录、环境变量等最小处置能力
- 产出 `docs/runner-boundary.md`，但 enforce 不作为 MVP 成败标准

#### 原第 15 周主题：公开项目整理

目标：把原型整理成可公开 GitHub 项目。

AIRT 参考：参考 Lab 08 的 engagement structure 组织 Demo，但公开仓库里的 payload 必须受控、脱敏、可本地复现。

### 周四（2026/09/03）：整理 README

- 概念：项目定位、读者路径
- 实验：写背景、架构、安装、运行方式
- 记录：README 初稿

### 周五（2026/09/04）：整理 Demo 场景

- 概念：最小可展示攻击链
- 实验：固定 1-2 个稳定 Demo，其中至少 1 个来自 AIRT Lab 02/03/08 思路的受控改写
- 记录：Demo 脚本；标注攻击链阶段和 Guard 输出

### 周六（2026/09/05）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/09/06）：休息

- 不安排正式学习任务

## 第 15 周（2026/09/07 - 2026/09/13）：公开项目整理 / 文章和面试材料

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/09/07）：清理公开风险

- 概念：脱敏、受控 payload、安全声明
- 实验：清理敏感信息和破坏性样例
- 记录：公开发布检查清单

### 周二（2026/09/08）：补充使用样例

- 概念：可复现性
- 实验：补充命令、输入、输出样例
- 记录：复现步骤

### 周三（2026/09/09）：项目预发布检查

- 概念：仓库质量、目录一致性
- 实验：从零跑一遍 README 流程
- 记录：待修复问题清单

#### 原第 15 周验收标准

- 能从 README 从零复现 1-2 个稳定 Demo
- 清理公开风险，确保样例脱敏、受控、可复现
- 产出 README、Demo 脚本、复现步骤和预发布问题清单

#### 原第 16 周主题：文章和面试材料

目标：让项目可讲、可展示、可用于求职。

AIRT 参考：用 AIRT 作为攻击面学习来源来讲清楚“为什么需要 runtime guard”，但项目亮点要落在 eBPF 观测、task 归因和检测闭环。

### 周四（2026/09/10）：写技术文章大纲

- 概念：从 Prompt Injection 到 syscall 观测
- 实验：整理文章结构和关键截图/日志
- 记录：文章大纲

### 周五（2026/09/11）：完成技术文章初稿

- 概念：问题、方法、实现、结果
- 实验：写完整初稿
- 记录：待补证据

### 周六（2026/09/12）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/09/13）：休息

- 不安排正式学习任务

## 第 16 周（2026/09/14 - 2026/09/20）：文章和面试材料

说明：本周按真实日历归属安排，正式学习任务只放在周一到周五，周六复盘，周日休息。

### 周一（2026/09/14）：整理面试讲稿

- 概念：项目亮点、架构取舍、风险边界
- 实验：写 5 分钟项目讲解稿
- 记录：面试问答清单

### 周二（2026/09/15）：录制或彩排 Demo

- 概念：演示路径、故障预案
- 实验：录制或完整彩排 3-5 分钟 Demo
- 记录：Demo 复盘

### 周三（2026/09/16）：最终复盘

- 概念：能力迁移总结
- 实验：检查 GitHub 项目、文章、Demo、问答清单
- 记录：项目复盘

#### 原第 16 周验收标准

- 能完成 3-5 分钟 Demo 彩排
- 能用 5 分钟讲清楚项目背景、架构、取舍和边界
- 产出技术文章初稿、面试讲稿、问答清单和最终复盘记录

### 周六（2026/09/19）：可选复盘与补漏

- 复跑本周实验，补齐未完成笔记，整理问题清单
- 不引入新的主线概念和新功能

### 周日（2026/09/20）：休息

- 不安排正式学习任务
