# 16 周按天执行计划

## 执行约束

- 周期：16 周
- 节奏：周一到周五学习，周末休息
- 每天投入：2 小时
- 每天结构：30 分钟概念学习 + 60 分钟动手实验 + 30 分钟短记录
- 每周有效学习时间：10 小时
- 原则：每天只完成一个明确闭环，优先形成可运行代码、可复现样例或可提交文档

## 每日短记录模板

每天最后 30 分钟回答：

- 今天学到的 AI / Agent 概念是什么？
- 它对应到系统安全里的什么对象？
- 今天做了哪个最小实验？
- 这个实验暴露了什么攻击面或防护点？

## 第 1 周：LLM API 和基础概念

目标：从安全工程视角理解 LLM 应用的基本对象。

### 周一：跑通第一次 LLM API 调用

- 概念：LLM API、model、request、response
- 实验：用 Go 调用一次云端 LLM API
- 记录：API 调用链和安全边界

### 周二：理解 message 和 role

- 概念：system、user、assistant message
- 实验：修改不同 role 的内容，观察输出变化
- 记录：system prompt 为什么像策略输入

### 周三：理解上下文窗口和 token

- 概念：context window、token、截断
- 实验：构造长输入，观察模型响应变化
- 记录：上下文污染和日志留存风险

### 周四：理解 temperature 和 streaming

- 概念：temperature、determinism、streaming
- 实验：比较不同 temperature 和 streaming 输出
- 记录：安全检测为什么需要结构化日志

### 周五：整理 Go LLM 基础样例

- 概念：LLM 应用最小组成
- 实验：整理 `examples/llm-basic/`
- 记录：`docs/notes/week-01.md`

### 周末：休息

- 不安排正式学习任务

## 第 2 周：Tool Calling 基础

目标：理解模型如何从文本生成结构化 tool call。

### 周一：理解 tool schema

- 概念：tool name、description、parameters
- 实验：定义 `read_file` 的 Go 结构体和 schema
- 记录：tool schema 为什么是攻击面

### 周二：解析 tool args

- 概念：结构化参数、JSON schema、参数校验
- 实验：让模型生成 `read_file` 参数并在 Go 侧解析
- 记录：参数校验和越权路径风险

### 周三：实现 `read_file`

- 概念：tool result、错误返回、最小权限
- 实验：实现受控 `read_file`
- 记录：文件读取对应的系统安全对象

### 周四：实现 `write_file`

- 概念：写操作风险、覆盖、路径穿越
- 实验：实现受控 `write_file`
- 记录：写文件工具的防护点

### 周五：记录完整 tool calling 链路

- 概念：prompt -> tool call -> tool result -> final answer
- 实验：输出完整调用日志
- 记录：tool calling 数据结构样例

### 周末：休息

- 不安排正式学习任务

## 第 3 周：最小 Agent Loop

目标：手写一个最小 Agent，理解 observe -> plan -> act -> observe。

### 周一：实现 Agent loop 骨架

- 概念：observe、plan、act、observe loop
- 实验：用 Go 写最小 Agent loop
- 记录：Agent 和普通 API 调用的区别

### 周二：加入 `run_shell_command`

- 概念：命令执行工具、stdout/stderr、exit code
- 实验：实现受控 shell command tool
- 记录：自然语言到 `execve` 的转换链路

### 周三：加入 `task_id`

- 概念：task、session、tool call id
- 实验：给每次 Agent 调用分配 `task_id`
- 记录：为什么安全审计需要 task 归因

### 周四：记录 tool call 运行细节

- 概念：输入、输出、错误、耗时、状态码
- 实验：输出结构化 tool call 日志
- 记录：审计字段初稿

### 周五：整理最小 Agent 样例

- 概念：Agent runtime 的最小边界
- 实验：整理 `examples/min-agent/`
- 记录：Agent 执行日志样例

### 周末：休息

- 不安排正式学习任务

## 第 4 周：RAG 和上下文污染

目标：理解 RAG 的基本链路和安全风险，不深入向量库工程。

### 周一：实现最小文档加载

- 概念：document、chunk、context
- 实验：读取本地文本并切分 chunk
- 记录：外部文档如何进入上下文

### 周二：实现最小检索

- 概念：retrieve、top-k、相关性
- 实验：用关键词检索代替复杂向量库
- 记录：检索结果为什么会污染 prompt

### 周三：把检索结果拼入 prompt

- 概念：RAG prompt template
- 实验：把 chunk 注入 LLM 上下文并生成回答
- 记录：RAG 链路的信任边界

### 周四：构造恶意文档注入

- 概念：RAG Prompt Injection
- 实验：让恶意文档诱导 Agent 调用 tool
- 记录：文档输入如何变成系统行为

### 周五：整理威胁模型初版

- 概念：Prompt Injection、Jailbreak、RAG 注入、工具滥用
- 实验：对比 4 类风险样例
- 记录：`docs/threat-model.md` 初版

### 周末：休息

- 不安排正式学习任务

## 第 5 周：Agent 攻击样例

目标：把 AI 风险转成真实系统行为。

### 周一：构造 Prompt Injection 样例

- 概念：指令覆盖、间接注入、上下文污染
- 实验：诱导 Agent 偏离原始任务
- 记录：攻击前置条件

### 周二：构造敏感文件读取样例

- 概念：越权文件访问、敏感路径
- 实验：读取 `/etc/passwd`、模拟 SSH key、模拟云凭证
- 记录：敏感路径规则草案

### 周三：构造网络外联样例

- 概念：数据外传、allowlist、外联审计
- 实验：用 `http_get` 或 shell 触发外联
- 记录：外联检测字段草案

### 周四：构造受控资源滥用样例

- 概念：CPU、memory、pids、fork bomb 风险
- 实验：运行受控资源压测样例
- 记录：资源限制需求

### 周五：整理攻击链

- 概念：prompt -> tool call -> process -> syscall
- 实验：把 4 类样例整理到 `examples/attacks/`
- 记录：攻击链说明

### 周末：休息

- 不安排正式学习任务

## 第 6 周：Go Tool Runner 和项目骨架

目标：把实验样例收敛成 `Code Interpreter Guard` 项目骨架。

### 周一：建立项目目录

- 概念：guard、runner、agent、event 的职责
- 实验：创建 `cmd/guard`、`cmd/runner`、`pkg/*`
- 记录：目录结构说明

### 周二：固化 tool runner

- 概念：tool 执行边界、工作目录、超时
- 实验：把 shell/file/http tools 接入 runner
- 记录：runner 责任边界

### 周三：定义 task 和 tool call 结构

- 概念：task id、tool call id、parent relation
- 实验：实现 Go 数据结构
- 记录：归因字段设计

### 周四：定义 event 结构

- 概念：process/file/network event
- 实验：实现统一 JSON event 类型
- 记录：事件字段设计

### 周五：跑通最小项目闭环

- 概念：Agent -> runner -> JSON log
- 实验：输出一次完整 task 日志
- 记录：第一个端到端样例

### 周末：休息

- 不安排正式学习任务

## 第 7 周：eBPF 进程观测

目标：采集 Agent 触发的进程执行行为。

### 周一：搭建 libbpf 骨架

- 概念：tracepoint/kprobe、ringbuf/perfbuf
- 实验：创建 `ebpf/exec.bpf.c`
- 记录：采集点选择

### 周二：采集 `execve`

- 概念：exec 行为、argv、comm
- 实验：捕获进程执行事件
- 记录：从 shell tool 到 exec 事件

### 周三：补充进程上下文

- 概念：pid、ppid、uid、gid、argv
- 实验：补充第一版进程事件字段
- 记录：进程归因字段；`cgroup/container id` 作为后续增强

### 周四：Go 侧消费事件

- 概念：用户态聚合、事件解码
- 实验：`cmd/guard observe` 输出 exec 事件
- 记录：eBPF 到 Go 的数据流

### 周五：还原进程树

- 概念：process tree、parent-child relation
- 实验：按 `pid/ppid` 还原一次 Agent task
- 记录：进程树审计输出

### 周末：休息

- 不安排正式学习任务

## 第 8 周：eBPF 文件观测

目标：采集文件访问和文件修改行为。

### 周一：采集 `openat`

- 概念：文件打开、路径、权限
- 实验：捕获 `openat` 事件
- 记录：文件读取和敏感路径

### 周二：测试 `openat` 路径语义

- 概念：相对路径、绝对路径、cwd、dfd
- 实验：测试 `openat` 在不同路径输入下的事件表现
- 记录：第一版路径解析限制；`openat2` 作为后续增强

### 周三：采集 `unlink`

- 概念：文件删除风险
- 实验：捕获删除事件
- 记录：破坏性操作审计

### 周四：采集 `rename`

- 概念：文件重命名、覆盖、规避
- 实验：捕获重命名事件
- 记录：修改类事件字段

### 周五：验证敏感路径访问

- 概念：敏感路径检测前置数据
- 实验：用攻击样例触发文件事件
- 记录：文件访问事件样例

### 周末：休息

- 不安排正式学习任务

## 第 9 周：eBPF 网络观测

目标：采集 Agent 触发的网络外联行为。

### 周一：选择网络采集点

- 概念：connect、目标 IP、端口
- 实验：确定采集字段
- 记录：网络事件设计

### 周二：采集 `connect`

- 概念：外联行为
- 实验：捕获 TCP connect 事件
- 记录：外联事件样例

### 周三：补充进程上下文

- 概念：网络事件归因
- 实验：关联 pid、comm
- 记录：外联和进程关系；`cgroup/netns/container context` 作为后续增强

### 周四：统一三类事件 JSON

- 概念：process/file/network event schema
- 实验：统一事件输出格式
- 记录：统一事件字段

### 周五：验证 shell 和 http 外联

- 概念：tool 层外联和系统层外联
- 实验：分别用 `http_get` 和 shell 触发外联
- 记录：网络观测验证结果

### 周末：休息

- 不安排正式学习任务

## 第 10 周：Task 归因和审计报告

目标：把应用侧 task / tool call 和系统侧事件连起来。

### 周一：定义 task id 生命周期

- 概念：task start、tool call、task end
- 实验：固化 task id 生成和结束逻辑
- 记录：task 生命周期说明

### 周二：传递 task id 到 runner

- 概念：环境变量、wrapper 参数、继承关系
- 实验：通过 env 或 argv 传递 task id
- 记录：传递方式取舍

### 周三：关联进程事件

- 概念：task -> process tree
- 实验：把 exec 事件归因到 task
- 记录：进程归因样例

### 周四：关联文件和网络事件

- 概念：task -> file/network behavior
- 实验：把 file/network 事件归因到 task
- 记录：行为归因样例

### 周五：输出 task-level 审计报告

- 概念：审计报告、可复现证据
- 实验：生成 JSON report
- 记录：`docs/audit-report-example.md`

### 周末：休息

- 不安排正式学习任务

## 第 11 周：规则检测

目标：实现最小可用检测能力。

### 周一：设计规则格式

- 概念：condition、severity、reason、evidence
- 实验：定义 `rules/*.yaml`
- 记录：规则格式说明

### 周二：实现敏感路径规则

- 概念：path match、home dir、云凭证
- 实验：检测 `/etc/shadow`、`~/.ssh`、模拟云凭证
- 记录：敏感路径检测样例

### 周三：实现危险命令规则

- 概念：危险命令、命令组合、管道
- 实验：检测 `nc`、`curl | sh`、`chmod +s`
- 记录：危险命令规则样例

### 周四：实现异常网络规则

- 概念：allowlist、unknown destination
- 实验：检测非 allowlist 外联
- 记录：异常网络规则样例

### 周五：输出检测报告

- 概念：风险等级、触发原因、证据
- 实验：生成 detection report
- 记录：检测报告样例

### 周末：休息

- 不安排正式学习任务

## 第 12 周：攻击链检测

目标：做出 Agent Security 特色分析，而不是普通主机告警。

### 周一：串联 prompt 和 tool call

- 概念：意图层信号
- 实验：保存 prompt 和 tool call 映射
- 记录：prompt 证据字段

### 周二：串联系统事件

- 概念：行为层证据
- 实验：把 exec/file/network 纳入同一 task timeline
- 记录：timeline 样例

### 周三：实现敏感文件意图规则

- 概念：prompt 请求敏感文件
- 实验：检测 prompt 层敏感意图
- 记录：意图规则样例

### 周四：实现实际访问规则

- 概念：tool 实际访问敏感文件
- 实验：检测文件事件层敏感访问
- 记录：行为规则样例

### 周五：实现外联组合规则

- 概念：敏感文件访问后外联
- 实验：生成 attack-chain report
- 记录：攻击链报告样例

### 周末：休息

- 不安排正式学习任务

## 第 13 周：行为基线轻量版

目标：补充研究深度，但不做复杂异常检测平台。

### 周一：定义正常任务集合

- 概念：benign task、baseline scope
- 实验：定义数学计算、文件处理、数据分析任务
- 记录：正常任务清单

### 周二：采集正常进程行为

- 概念：正常进程集合
- 实验：运行正常任务并采集 exec
- 记录：进程基线样例

### 周三：采集正常文件和网络行为

- 概念：正常文件路径、正常外联
- 实验：采集 file/network 行为
- 记录：文件和网络基线样例

### 周四：实现简单偏离检测

- 概念：rare process/path/destination
- 实验：检测偏离正常集合的行为
- 记录：偏离检测样例

### 周五：记录误报和漏报

- 概念：false positive、false negative
- 实验：用正常样例和攻击样例验证
- 记录：`docs/baseline.md`

### 周末：休息

- 不安排正式学习任务

## 第 14 周：Runner 边界和最小处置

目标：检测审计优先，补一个可演示的最小处置闭环。

### 周一：设计运行模式

- 概念：observe、alert、enforce
- 实验：实现模式参数
- 记录：模式语义说明

### 周二：实现高危 kill

- 概念：进程处置、副作用
- 实验：高危规则触发后 kill 相关进程
- 记录：kill 处置边界

### 周三：限制 runner 环境变量和工作目录

- 概念：working directory、env、tmp dir
- 实验：限制 runner 的工作目录、环境变量和临时目录
- 记录：本地单机 runner 基础边界说明

### 周四：加入 timeout 和输出大小限制

- 概念：执行超时、stdout/stderr 上限、响应大小上限
- 实验：为 shell/http tool 加 timeout 和输出大小限制
- 记录：资源滥用处置边界

### 周五：整理 runner 边界设计

- 概念：本地单机、非容器、默认 namespace 的边界
- 实验：验证 kill、timeout、工作目录、环境变量限制
- 记录：`docs/runner-boundary.md`；seccomp、namespace、cgroup、容器归因作为后续增强

### 周末：休息

- 不安排正式学习任务

## 第 15 周：公开项目整理

目标：把原型整理成可公开 GitHub 项目。

### 周一：整理 README

- 概念：项目定位、读者路径
- 实验：写背景、架构、安装、运行方式
- 记录：README 初稿

### 周二：整理 Demo 场景

- 概念：最小可展示攻击链
- 实验：固定 1-2 个稳定 Demo
- 记录：Demo 脚本

### 周三：清理公开风险

- 概念：脱敏、受控 payload、安全声明
- 实验：清理敏感信息和破坏性样例
- 记录：公开发布检查清单

### 周四：补充使用样例

- 概念：可复现性
- 实验：补充命令、输入、输出样例
- 记录：复现步骤

### 周五：项目预发布检查

- 概念：仓库质量、目录一致性
- 实验：从零跑一遍 README 流程
- 记录：待修复问题清单

### 周末：休息

- 不安排正式学习任务

## 第 16 周：文章和面试材料

目标：让项目可讲、可展示、可用于求职。

### 周一：写技术文章大纲

- 概念：从 Prompt Injection 到 syscall 观测
- 实验：整理文章结构和关键截图/日志
- 记录：文章大纲

### 周二：完成技术文章初稿

- 概念：问题、方法、实现、结果
- 实验：写完整初稿
- 记录：待补证据

### 周三：整理面试讲稿

- 概念：项目亮点、架构取舍、风险边界
- 实验：写 5 分钟项目讲解稿
- 记录：面试问答清单

### 周四：录制或彩排 Demo

- 概念：演示路径、故障预案
- 实验：录制或完整彩排 3-5 分钟 Demo
- 记录：Demo 复盘

### 周五：最终复盘

- 概念：能力迁移总结
- 实验：检查 GitHub 项目、文章、Demo、问答清单
- 记录：项目复盘

### 周末：休息

- 不安排正式学习任务
