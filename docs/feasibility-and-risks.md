# 可落地性与风险评估

## 总体判断

这份计划作为学习路线可落地性较高；作为 16 周原型项目可落地，但必须严格控制 MVP。

评分：

- 学习计划：8/10
- 16 周原型项目：7/10
- 开源展示项目：7.5/10
- 生产级安全产品：不作为目标

## 成功标准

16 周结束时，应至少完成：

- 最小 Go Agent 和 tool runner
- task / tool call 日志
- eBPF 采集 `execve`、`openat`、IPv4 `connect`
- MVP 内增强采集 `unlink`、`rename`
- 基于 runner pid 和 pid/ppid 的 best-effort task 归因
- 敏感文件、危险命令、异常外联、敏感文件后外联检测报告
- 1-2 个稳定 demo
- README、技术文章初稿、5 分钟面试讲稿

## 高风险模块

### eBPF 采集

风险：

- BPF verifier、内核版本、BTF、libbpf 依赖可能影响进度
- `openat` 路径语义、相对路径、dfd、cwd 处理容易复杂化
- 事件丢失和 Go 侧解码会增加调试成本

降级：

- 优先跑通 `execve`、`openat`、IPv4 `connect`
- `unlink`、`rename` 纳入 MVP 内增强，但优先级低于前三类核心事件
- `openat2`、完整路径解析、容器上下文后移

### Task 归因

风险：

- 进程树并不总是稳定代表 task 边界
- daemon 化、后台进程、pid 复用、复杂并发会破坏归因准确性
- 容器、cgroup、namespace 会引入额外上下文

降级：

- 第一版明确为 best-effort
- 只覆盖当前 runner 直接或间接派生进程
- 用 runner pid、pid/ppid、task id 传递形成可复现 demo

### 端到端 Demo

风险：

- LLM 输出不稳定
- eBPF 环境差异会影响复现
- 攻击样例如果不受控，公开风险较高

降级：

- 固定 1-2 个稳定 demo
- 攻击样例使用 `lab/` 下模拟文件和本地测试服务
- demo 以审计和检测报告为主，不依赖复杂阻断

## MVP 必达

- `run_shell_command`、`read_file`、`write_file`、`http_get`
- task / tool call 日志和 `task_id`
- `execve`、`openat`、IPv4 `connect`
- runner pid + pid/ppid best-effort 归因
- 敏感文件访问、危险命令、异常外联、敏感文件后外联报告

## MVP 内增强

- `unlink`
- `rename`

## 增强项

这些内容有价值，但不作为 MVP 成败标准：

- 轻量行为基线
- observe / alert / enforce 模式
- 高危行为 kill
- runner 工作目录、环境变量、临时目录限制
- shell/http timeout 和输出大小限制

## 明确不做

- 复杂 RAG 平台
- Agent 框架适配
- 浏览器、数据库、云平台 API、Kubernetes API、远端 SSH tool
- 容器归因
- seccomp / namespace / cgroup 隔离
- 多租户策略中心
- 生产级 sandbox、EDR 或 Agent 防火墙
