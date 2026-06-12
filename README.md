# AI Agent Runtime Security Lab

这是一个面向 **AI Agent Runtime Security** 的学习与实验仓库。目标是把传统安全工程、Linux runtime security、主机观测和 eBPF 能力，迁移到 LLM Agent、Tool Use、RAG 和 Code Interpreter 等场景中。

仓库当前处于学习与原型阶段：前 4 周补齐 LLM / Agent 应用基础，后续逐步构建一个本地单机研究型原型 **Code Interpreter Guard**，用于观察、归因和检测 Agent 工具调用引发的系统行为。

## 适合谁

- 有安全工程、主机安全、EDR、eBPF 或 Linux runtime 背景，想理解 AI Agent 安全的人
- 想从 LLM API 基础一路推进到 Agent tool calling、RAG 注入、运行时审计的人
- 想构建一个可演示、可复现、可公开展示的 Agent runtime security 原型的人

## 项目主线

本仓库围绕一个核心问题推进：

> 自然语言中的恶意指令，如何通过 Agent 决策和工具调用，转化成真实的进程、文件、网络行为？

最终目标不是训练模型，也不是做通用聊天机器人，而是形成一条可审计链路：

```text
prompt / messages
  -> model decision
  -> tool call
  -> runner execution
  -> process / file / network event
  -> task attribution
  -> detection / audit report
```

## 当前进度

当前处于 **第 1 阶段：AI Agent 基础与风险认知**，**第 2 周**。

已完成 Week 01（LLM API + tool schema/args）与 Week 02 Day 07–10（受控 read/write、tool call 日志、Agent loop）。

| 资源 | 链接 |
|------|------|
| 详细进度 | [docs/progress.md](docs/progress.md) |
| Week 01 笔记 | [docs/notes/week-01/](docs/notes/week-01/) |
| Week 02 笔记 | [docs/notes/week-02/](docs/notes/week-02/) |

下次任务：Day 11，加入受控 `run_shell_command`。

## 快速开始

### 1. 准备环境

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置 API Key

样例使用 Poe 的 OpenAI-compatible API。API key 只从环境变量读取，不写入代码或 `.env` 文件。

```bash
export POE_API_KEY=你的密钥
```

### 3. 运行 Week 01 样例

```bash
source .venv/bin/activate

python3 day-01-first-call/main.py
python3 day-02-message-role/main.py
python3 day-03-context-window/main.py
python3 day-04-temperature-streaming/main.py
python3 day-04-temperature-streaming/streaming_demo.py
```

## 目录结构

```text
.
├── day-01-first-call/              # 最小 LLM API 调用
├── day-02-message-role/            # system / user / assistant role 实验
├── day-03-context-window/          # 多轮 history、token、上下文窗口实验
├── day-04-temperature-streaming/   # temperature 和 streaming 实验
├── docs/
│   ├── notes/                      # 每日学习笔记
│   ├── weekly-plan.md              # 16 周主计划
│   ├── progress.md                 # 当前进度
│   ├── checkpoints.md              # 阶段验收标准
│   ├── code-interpreter-guard-design.md
│   └── lab-safety.md               # 安全实验边界
└── requirements.txt
```

## 16 周路线

路线分为 4 个阶段：

1. **第 1-4 周：AI Agent 基础与风险认知**  
   LLM API、message、context window、tool calling、Agent loop、RAG 注入。

2. **第 5-8 周：Agent Runner 与运行时观测**  
   构建最小 runner，记录 tool call，采集进程和文件事件。

3. **第 9-12 周：归因、规则与攻击链检测**  
   关联 task / tool call / runtime event，输出 detection report 和 audit report。

4. **第 13-16 周：Demo、评估与公开材料**  
   固化演示路径，整理技术文章、面试讲稿和最终项目说明。

完整计划见：[16 周主计划](docs/weekly-plan.md)。

## 核心学习对象

Week 01 的 LLM 最小闭环可以概括为：

```text
client -> model -> messages -> parameters -> response -> usage/logs
```

后续每个 Agent 安全问题都会回到这几个对象：

- `messages`：system prompt、user input、assistant history、tool result 都会影响模型决策
- `context window`：过长 history 可能挤掉早期策略或事实
- `temperature`：影响输出稳定性，安全检测应优先低温和可复现
- `streaming`：影响日志采集时机，必须确认流式响应是否完整
- `tool call`：自然语言风险进入系统行为的关键转换点
- `runtime event`：进程、文件、网络行为是最终可观测证据

## 安全边界

这个仓库只做本地、受控、可解释、可复现的安全实验。

明确禁止：

- 读取真实 SSH key、云凭证、浏览器 cookie 或真实业务配置
- 执行不可控的破坏性命令
- 对公网目标做扫描、爆破、利用或未授权请求
- 将真实密钥、token、个人数据写入样例或日志

详细规则见：[安全实验边界](docs/lab-safety.md)。

## 重要文档

- [完整学习路线](docs/ai-agent-security-learning-plan.md)
- [16 周主计划](docs/weekly-plan.md)
- [学习进度](docs/progress.md)
- [阶段验收](docs/checkpoints.md)
- [每次学习会话指南](docs/session-guide.md)
- [Code Interpreter Guard 设计](docs/code-interpreter-guard-design.md)
- [安全实验边界](docs/lab-safety.md)
- [可落地性与风险评估](docs/feasibility-and-risks.md)
- [学习笔记索引](docs/notes/README.md)

## 项目边界

`Code Interpreter Guard` 是研究型原型，目标是验证 Agent runtime 的观测、归因、审计和检测闭环。

它不是生产级 sandbox、EDR 或 Agent 防火墙；第一版不承诺强隔离、完整阻断、生产级检测准确率，也不覆盖容器、多租户、复杂 namespace、daemon 化绕过等场景。
