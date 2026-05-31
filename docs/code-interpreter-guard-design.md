# Code Interpreter Guard 技术方案

## 目标

做一个面向 `Code Interpreter` 和 Agent runtime 的本地研究型安全原型：

- 采集进程、文件、网络行为
- 基于 runner pid 和 pid/ppid 做 best-effort task 归因
- 做规则检测和攻击链检测
- 检测审计优先，最小阻断次之
- 对高危行为进行告警、审计和可演示的最小处置

## 项目性质

这是本地单机研究型原型，目标是验证 Agent runtime 的观测、归因、审计和检测闭环。

它不是生产级 sandbox、EDR 或 Agent 防火墙；第一版不承诺强隔离、完整阻断或生产级检测准确率。

## 技术栈

- Go：Agent、tool runner、控制面、编排、规则判定、审计输出
- C / libbpf：eBPF 程序与内核态采集
- Python：可选参考脚本，不作为主线正式产出

## 第一版 Tool 范围

- `run_shell_command`
- `read_file`
- `write_file`
- `http_get`

暂时不接浏览器、数据库、云平台 API、Kubernetes API 和远端 SSH。

## 第一版运行边界

- 本地单机
- 非容器环境
- 默认 namespace
- IPv4 `connect` 观测
- 不处理容器归因、`cgroup`、`container id`、独立 network namespace、代理和 NAT 场景
- 不实现 `seccomp`、mount namespace、pid namespace、network namespace 隔离

## Task 归因边界

第一版归因是 best-effort：

- runner 启动时记录 runner pid
- Agent / runner 侧记录 task id 和 tool call id
- 根据 runner pid、pid/ppid 和进程树把系统事件归因到 task
- 只覆盖当前 runner 直接或间接派生的进程

第一版不保证以下场景的准确归因：

- daemon 化或主动脱离父进程树
- 复杂并发任务
- pid 复用导致的历史归因歧义
- 容器、cgroup、network namespace、代理和 NAT 场景

## 数据流

```text
User prompt
  -> Agent
  -> tool call
  -> code runner
  -> syscall / process / file / network
  -> eBPF events
  -> Go aggregator
  -> detector / policy
  -> alert / audit / optional enforce
```

## MVP 必达

- Go 实现最小 Agent loop
- Go 实现 tool calling 和 tool runner
- 记录 task / tool call 日志，并传递 `task_id`
- 采集 `execve`
- 采集 `openat`
- 采集 IPv4 `connect`
- 记录 `pid/ppid/uid/gid/comm/argv`
- 生成统一事件格式
- 基于 runner pid 和 pid/ppid 做 best-effort task 归因
- 敏感路径检测
- 危险命令检测
- 异常外联检测
- 敏感文件访问后外联的攻击链检测
- task-level 审计报告

## MVP 内增强

- 采集 `unlink`
- 采集 `rename`

`unlink` 和 `rename` 纳入 MVP 范围，但优先级低于 `execve`、`openat`、IPv4 `connect`。如果进度受限，先保证核心三类事件和报告闭环。

## 后续增强

- 轻量行为基线
- observe / alert / enforce 模式
- 高危行为 kill
- runner 工作目录、环境变量和临时目录限制
- shell/http timeout 和输出大小限制
- `openat2`
- `cgroup`
- `container id`
- network namespace 归因
- seccomp
- mount / pid / network namespace 隔离
- 容器环境检测和归因

## 明确非目标

- 生产级 sandbox
- 生产级 EDR
- Agent 防火墙或完整阻断系统
- 多租户策略中心
- 完整 RAG 平台
- 复杂 Agent 框架适配
- 浏览器、数据库、云平台 API、Kubernetes API、远端 SSH tool

## 推荐目录

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

## 最小闭环

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
