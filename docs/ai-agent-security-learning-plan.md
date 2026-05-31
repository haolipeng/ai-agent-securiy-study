# AI 大模型安全学习路线：面向 Agent Runtime Security

## 目标定位

这份计划不是泛泛学习「大模型安全」，而是把已有的安全工程能力迁移到 AI Agent 场景：

> Linux runtime security / eBPF / sandbox / container isolation + LLM Agent tool-use 安全

核心问题是：

- Agent 为什么会从自然语言变成真实系统行为？
- Tool calling 如何触发本地命令、文件访问和网络访问？
- Prompt Injection、RAG 注入和恶意输入如何诱导 Agent 越权？
- 能不能用 eBPF 看清 Agent 触发的进程、文件、网络行为？
- 能不能把系统事件关联回 task / tool call / prompt？
- 能不能做检测、审计、最小阻断和公开可复现 Demo？

## 访谈后的能力假设

- 背景：安全基础扎实，有网络安全、主机安全、Linux runtime security 经验
- eBPF：有基础，能把 eBPF 作为后续项目优势
- AI / LLM：新手，只接触过一点 API
- Tool calling：没做过
- Agent：没做过
- RAG：没做过
- Prompt Injection / Jailbreak：没系统学过
- Code Interpreter / sandboxed execution：没系统学过
- 主语言：Go + C/libbpf
- Agent 侧语言：Go
- Python：只作为可选参考，不作为主线正式产出
- 环境：本地 Linux 物理机
- 模型：可以使用云端 LLM API，不要求离线或本地模型优先
- 时间：周一到周五每天 2 小时，周六可选复盘/补漏，周日休息
- 周期：16 周
- 最终目标优先级：
  1. 系统补 AI / LLM / Agent 基础
  2. 支撑求职 / 转向 AI Agent Security / Runtime Security
  3. 做出可落地的安全原型

## 学习深度边界

需要学到：

- LLM API 调用、message、role、context window、token、streaming
- tool calling / function calling 的数据结构和执行链路
- Agent loop：observe -> plan -> act -> observe
- 最小 RAG：load -> chunk -> retrieve -> generate
- Prompt Injection、Jailbreak、RAG 注入、工具滥用的区别
- Code Interpreter 类系统为什么会产生 runtime security 风险
- 如何把 Agent 行为映射到进程、文件、网络、syscall
- 如何用 eBPF、规则检测、审计报告和最小阻断形成闭环

暂时不作为主线：

- 从零训练模型
- Transformer 数学推导
- 微调工程
- 大规模模型部署
- 复杂 Agent 框架源码通读
- Web UI、多租户、企业级策略中心
- 第一版不实现容器归因、`cgroup`、`seccomp`、mount/pid/network namespace 隔离

## 每日学习节奏

周一到周五每天 2 小时：

- 30 分钟：概念学习
- 60 分钟：动手实验
- 30 分钟：短记录

每天记录固定回答：

- 今天学到的 AI / Agent 概念是什么？
- 它对应到系统安全里的什么对象？
- 今天做了哪个最小实验？
- 这个实验暴露了什么攻击面或防护点？

周六只作为可选复盘/补漏日，不引入新的主线概念和新功能；周日休息。

实际推进以 `docs/progress.md` 的完成状态为准，日期只作为参考。如果上次任务没有完成，下次优先续上，不按日历硬跳。

## 学习主线

1. 先补 AI 应用基础：LLM API、message、tool calling、Agent loop
2. 再理解攻击面：Prompt Injection、RAG 注入、工具滥用、Code Interpreter 风险
3. 再做 Go Agent：手写最小 Agent、tool runner、shell/file/http tools
4. 再做观测：用 eBPF 看 exec、file、network
5. 再做归因：把 task / tool call 和系统事件关联起来
6. 再做检测：敏感路径、危险命令、异常外联、攻击链
7. 最后做闭环：审计报告、最小阻断、公开 GitHub 项目、Demo、文章、面试讲稿

第一版坚持手写最小 Agent loop，不引入复杂 Agent 框架。RAG 只做关键词检索的最小 demo，用来理解外部文档如何污染 prompt 并诱导 tool use，不引入向量库和 embedding 工程。

## 执行计划

详细的 16 周按天执行计划见：

- [16 周按天执行计划](weekly-plan.md)

## 第一个项目：Code Interpreter Guard

建议做一个本地单机版 `Code Interpreter Guard`。它不是完整产品，而是可本地运行、可公开复现的研究型原型。

它不是生产级 sandbox、EDR 或 Agent 防火墙；第一版目标是观测、归因、审计和检测闭环，不承诺强隔离、完整阻断或生产级检测准确率。

### 项目目标

- Go 实现 Agent、tool runner、控制面、规则检测、审计输出
- C/libbpf 实现 eBPF 数据采集
- 采集进程、文件、网络行为
- 基于 runner pid 和 pid/ppid 做 best-effort task 归因
- 做规则检测和攻击链检测
- 输出审计报告和复现材料

### MVP 边界

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
- timeout、工作目录、环境变量、输出大小限制等最小处置能力

### 第一版运行边界

- 本地单机
- 非容器环境
- 默认 namespace
- IPv4 `connect` 观测
- 检测审计优先，最小处置作为增强项
- 不处理容器归因、`cgroup`、`container id`、独立 network namespace、代理和 NAT 场景
- 不实现 `seccomp`、mount namespace、pid namespace、network namespace 隔离

task 归因是 best-effort：第一版只覆盖当前 runner 直接或间接派生的进程，不保证 daemon 化、脱离父进程树、复杂并发、pid 复用、容器或 namespace 场景。

### 第一版 Tool 范围

- `run_shell_command`
- `read_file`
- `write_file`
- `http_get`

暂时不做：

- 浏览器自动化
- 数据库操作
- 云平台 API
- Kubernetes API
- SSH 到远端主机

### 推荐项目结构

```text
code-interpreter-guard/
  cmd/
    guard/
    runner/
  ebpf/
    exec.bpf.c
    file.bpf.c
    net.bpf.c
  pkg/
    agent/
    agentctx/
    detector/
    event/
    report/
    sandbox/
  rules/
  examples/
    llm-basic/
    tool-calling/
    min-agent/
    rag-min/
    attacks/
    benign/
  docs/
    notes/
    threat-model.md
    audit-report-example.md
    runner-boundary.md
    baseline.md
  README.md
```

### 最小闭环

```text
Go Agent
  -> tool call
  -> runner 执行 shell/file/http tool
  -> syscall / process / file / network
  -> eBPF events
  -> Go aggregator
  -> task 归因
  -> rule / attack-chain detection
  -> audit report
  -> optional enforce
```

## 面试重点

需要能讲清楚：

1. Agent 为什么会把自然语言风险变成 runtime security 风险
2. Tool calling 的数据结构和执行链路
3. Prompt Injection、Jailbreak、RAG 注入和工具滥用的区别
4. Code Interpreter 为什么必须考虑进程、文件、网络和资源边界
5. eBPF 为什么适合做 Agent runtime observability
6. 如何把 syscall 级事件和 Agent task / tool call 关联起来
7. 如何设计敏感路径、危险命令、异常外联和攻击链规则
8. 怎么控制误报和漏报
9. 自动处置有什么副作用
10. 第一版为什么选择本地单机、非容器、默认 namespace
11. seccomp、namespace、capabilities、cgroup 各自管什么，以及为什么放到后续增强
12. 为什么普通容器隔离不一定足够
12. gVisor、Firecracker、nsjail 这类方案各自适合什么边界

## 开源项目参考方式

减少固定源码阅读，按需参考，不做完整源码通读。

- AgentSight：需要参考 Agent 上下文和系统事件关联时再看
- Tetragon：需要参考 eBPF runtime security 事件和 policy 建模时再看
- Tracee：需要参考事件 pipeline、规则/signature 设计时再看
- Falco：需要参考规则语言和告警语义时再看
- nsjail：需要参考 namespace、cgroup、rlimit、seccomp 组合方式时再看
- OWASP GenAI Security Project：需要整理威胁分类和面试表达时再看
- garak / PyRIT / promptfoo：需要设计 LLM app red teaming 测试集时再看
- E2B / Open Interpreter：需要理解 Code Interpreter 产品形态时再看

当前最有价值的能力组合是：

> AI / Agent 应用基础 + 系统安全能力 + eBPF runtime observability + Agent 安全分析 + 可运行公开原型
