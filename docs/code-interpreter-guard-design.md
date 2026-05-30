# Code Interpreter Guard 技术方案

## 目标

做一个面向 `Code Interpreter` 和 Agent runtime 的本地研究型安全原型：

- 采集进程、文件、网络行为
- 关联 Agent task / tool call
- 做规则检测、攻击链检测、轻量行为基线
- 检测审计优先，最小阻断次之
- 对高危行为进行告警、审计和可演示的最小处置

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

## 第一阶段能力

- Go 实现最小 Agent loop
- Go 实现 tool calling 和 tool runner
- 采集 `execve`
- 采集 `openat/unlink/rename`
- 采集 `connect`
- 记录 `pid/ppid/uid/gid/comm/argv`
- 生成统一事件格式

## 第二阶段能力

- 敏感路径检测
- 危险命令检测
- 异常外联检测
- 攻击链检测

## 第三阶段能力

- task-level 审计报告
- observe / alert / enforce 模式
- 高危行为 kill
- runner 工作目录、环境变量和临时目录限制
- shell/http timeout 和输出大小限制

## 后续增强

- `openat2`
- `cgroup`
- `container id`
- network namespace 归因
- seccomp
- mount / pid / network namespace 隔离
- 容器环境检测和归因

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
