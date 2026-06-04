### TL;DR

+   **它是什么：** Tool Calling 为大型语言模型（Large Language Models，LLM）提供 I/O（Input/Output，输入/输出）层，让模型既能读取外部数据，也能调用外部系统完成具体任务。
    
+   **为什么重要：** Tool Calling 将 LLM 从被动的文本生成器，转变为能够主动与 GitHub 等外部系统交互的 Agent。
    
+   **问题所在：** 真正的挑战并不是 LLM 的推理能力，而是如何安全、可靠地执行工具调用，例如认证、重试、错误处理和权限控制。
    
+   **解决方案：** Composio 提供托管的执行层，负责处理集成相关的底层工作，让你可以专注于构建 Agent。
    

从“聊天机器人”到“[AI Agent](https://composio.dev/blog/ai-agents)”的转变，取决于一项核心技术能力：**Tool Calling**。

对于正在评估集成策略的工程负责人来说，需要区分核心机制（Tool Calling）、工具发现机制（Tool Search）以及新兴的接口协议（MCP）。它们是不同的层，各自有不同的目的。

本文将拆解现代 Tool Calling 技术栈，从基础概念一直讲到企业级架构。我们会揭示其中隐藏的工程负担，尤其是“发现”一个工具与在生产环境中安全“执行”这个工具之间的差距。

## 一、什么是 Tool Calling？为什么它很重要？

大型语言模型（Large Language Models，LLM）是强大的推理引擎，但它们本质上是孤立的。模型的知识停留在训练数据中，无法直接获取最新信息，也无法主动与外部世界交互。

**Tool Calling**（通常也叫 Function Calling）提供了打破这种隔离的 I/O 层。它允许模型输出结构化数据（通常是 JSON（JavaScript Object Notation，JavaScript 对象表示法）），指示外部系统执行动作，而不仅仅是生成文本。

有了这项能力，模型不再只是生成判断或建议，还能把结果交给外部系统，转化为可以执行的具体操作。对开发者来说，它带来了三项关键能力：

1.  **访问实时数据：** 通过获取实时股票价格、天气或最新数据库记录，突破训练数据截止时间的限制。
    
2.  **执行动作：** 将 LLM 从被动观察者转变为主动参与者，让它能够改变外部系统中的数据或状态，例如发送邮件、更新 CRM，或者部署代码。
    
3.  **结构化互操作：** 将 LLM 自由、非结构化的推理结果，转换为外部系统可以识别和处理的严格机器可读格式。

## 二、从理论到现实：真实世界中的 Tool Call 是什么样的？

教程里经常用 `get_weather(city="San Francisco")` 这类简单示例来展示 Tool Calling。

但在生产级企业环境中，复杂度不会只是简单增加，而是会随着系统、权限和步骤变多而成倍放大。

### 2.1 简单用例：数据检索

用户问客服机器人：“我的订单在哪里？”Agent 调用 `shopify_get_order_status(order_id="123")`。这里的复杂度仍然很低：一次只读 API（Application Programming Interface，应用程序接口）调用。

### 2.2 企业级挑战：多步骤编排

考虑一个销售运营 Agent。用户输入：*"官网表单刚收到一个新的企业客户线索。请创建客户档案，分配给我，并同步它之前的沟通记录。"*

这需要 Agent 在多个彼此独立的业务系统之间完成一组连续操作：

1.  **获取上下文：** Agent 调用营销系统或官网表单系统的 API，获取该线索的来源、提交内容和历史互动记录。
    
2.  **转换数据：** Agent 将线索数据转换为 CRM 系统可以接受的客户、联系人或商机字段。
    
3.  **执行写入：** Agent 调用 CRM API，创建客户档案或商机记录。
    
4.  **处理状态：** Agent 解析 CRM 返回的结果，获取新建记录的 ID。
    
5.  **串联动作：** Agent 使用这个记录 ID 创建跟进任务，并将任务分配给对应销售，也可以同步到飞书、企业微信或钉钉等协作工具。
    

瓶颈不在于 LLM 的推理能力，而在于要编写大量容易出错的集成代码，才能跨越不同 API 标准完成认证、数据映射和操作执行。

## 三、分类：Tool Calling、Tool Search 与 MCP

在为这些复杂工作流设计解决方案之前，需要先区分三个经常在开发者讨论中被混为一谈的概念。

| **概念**         | **作用**                                                     | **类比**                                                     |
| :--------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Tool Calling** | **机制层。** 模型输出结构化 JSON 参数，而不是普通文本的基础能力。 | **执行之手。** 它让大脑（LLM）能够操作外部对象。 |
| **Tool Search**  | **发现层。** 让模型从大型工具目录（1,000+）中找到合适工具定义的方法，同时避免撑爆上下文窗口。 | **工具索引。** 只有需要时，才查找对应的工具定义。 |
| **MCP**          | **接口标准。** 一种开放协议，即[模型上下文协议（Model Context Protocol，MCP）](https://composio.dev/blog/what-is-model-context-protocol-mcp-explained)，用于标准化工具的定义和连接方式。 | **USB-C 接口。** 无论外设来自哪个厂商，都使用同一种标准接口连接。 |

## 四、机制：Agent 的 6 步执行循环

早期文档描述的是一个简单的 5 步循环。在使用动态发现的现代生产环境中，这个循环已经演进为 6 步流程。

1.  **工具发现（第 0 步）：** 应用根据用户意图查询工具注册表（通过 MCP 或向量存储），找到相关工具定义。这一步可以避免上下文窗口被塞满。
    
2.  **工具定义：** LLM 接收已发现工具的具体定义，例如 JSON Schema。
    
3.  **用户提示词：** 用户提出一个需要外部动作的请求。
    
4.  **LLM 预测：** 模型结合提示词和工具定义进行分析，输出一段结构化 JSON 数据，也就是“Tool Call”。
    
5.  **执行（瓶颈）：** 应用代码接收 JSON，处理认证，对外部 API 执行业务逻辑，并管理错误。
    
6.  **最终响应：** 工具输出回传给 LLM，由 LLM 生成面向用户的可读确认信息。
    

## 五、用 Anthropic 的 Tool Search 解决“上下文爆炸”问题

随着 Agent 从演示走向企业使用场景，所需工具数量会急剧增长。一个处理 IT 支持的 Agent，可能需要访问 Jira、GitHub、PagerDuty、Slack 和 AWS。

把 50 多个工具的定义全部加载进系统提示词，会带来两个问题：

1.  **成本与延迟：** 工具定义会消耗输入 Token。[Anthropic 的内部测试](https://www.anthropic.com/engineering/advanced-tool-use)显示，58 个工具可能消耗约 55k Token。
    
2.  **准确率下降：** 随着工具选项数量增加，模型选择正确工具的能力会下降。
    

Anthropic 的 [**Tool Search**](https://docs.anthropic.com/en/docs/tool-use#tool-search) 等方案通过允许模型“搜索”工具，而不是预先加载所有工具，来解决这个问题。

**影响：**

+   **Token 减少：** 动态加载可以将 Token 用量减少 **85%**（在大规模工具目录测试中，从约 77k 降到约 8.7k）。
    
+   **准确率：** 在包含大量工具集的测试中，准确率从 [**79.5% 提升到 88.1%**](https://www.anthropic.com/engineering/advanced-tool-use)（Claude Opus 4.5）。
    

不过，Tool Search 多了一步搜索过程，因此会让整体响应变慢一些。Anthropic 建议，当你的 Agent 需要访问 **30 个以上工具**时，再使用 Tool Search。

## 六、MCP：AI 工具的“USB-C”

**模型上下文协议（Model Context Protocol，MCP）**解决的是工具连接方式不统一的问题。过去，将 Agent 连接到 Google Drive 和连接到 Slack，往往需要两套不同实现。MCP 则把工具的描述和连接方式标准化。

如果你使用一个[兼容 MCP 的服务器](https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch)，Agent 就可以通过标准的 `tools/list` 和 `tools/call` 协议接入对应资源。这种方法非常适合标准化，但理解 MCP **不做什么**同样关键。

MCP 规定的是工具如何暴露、如何被调用。它不负责工具调用真正执行时所需的认证、重试、限流和审计。MCP 不解决：

+   面向 10,000 名用户的 OAuth 2.0 生命周期管理。
    
+   API 返回 `429` 时的速率限制处理。
    
+   针对每一次操作的 SOC 2 合规日志。
    

## 七、执行鸿沟：为什么工具发现不等于生产就绪？

这个鸿沟是工程团队最常见的失败点。他们实现了 Tool Search（发现），也使用了 MCP（标准化），却低估了**执行层**的复杂度。

找到该调用哪个工具只是第一步。真正困难的是，让每一次工具调用都能在生产环境中安全、稳定地执行，并正确处理认证、权限和异常情况。

### 7.1 大规模按用户认证的挑战

在演示中，你可以把 API Key 存在 `.env` 文件里。在生产环境中，你有 5,000 个用户，他们都需要连接GitHub账号。

你必须构建 OAuth 客户端，处理授权重定向，安全存储刷新 Token，并在 Token 过期前自动刷新。

更麻烦的是，你支持的每一个集成都可能有不同的认证流程，因此需要分别维护。关于这个认证挑战的更多内容，可以阅读我们关于[开始构建 AI Agent](https://composio.dev/blog/build-effective-ai-agents) 的文章。

### 7.2 管理 API 的可靠性和异构性

生产环境中的 API 调用并不总是稳定。

**速率限制：** 当你的 Agent 触发速率限制时会发生什么？LLM 并不知道如何进行指数退避。你的代码必须处理这种情况。

**分页：** LLM 可能会请求“所有工单”，但 API 返回的是 50 页中的第 1 页。你的执行层必须抽象分页，否则 Agent 可能会基于不完整数据，给出看似合理但实际错误的回答。

### 7.3 处理 Agent 治理

如果你的 Agent 可以访问 GitHub 中的 `delete_repo`，那么谁可以调用它？MCP 提供了能力，但不强制执行策略。

## 八、解决方案：将 Composio 作为执行层

Composio 充当“第 5 步”执行阶段的托管基础设施。我们抽象掉认证和 API 交互的复杂性，让你可以使用 MCP 和 Tool Search，而不用从零开始构建认证、重试、错误处理等集成基础设施。

### 8.1 统一连接与托管认证

你不需要为 200 多个服务构建 OAuth 流程，Composio 会处理完整生命周期。你只需认证用户一次，我们会处理 Token 刷新、存储和安全。更多内容见我们的 *OAuth 深度解析*。

### 8.2 实现方式的差异

**方案 A：手动方式（DIY）** 你需要编写集成代码，解释 LLM 输出的 JSON、发起 HTTP 请求、处理认证，并解析错误。

```javascript
# The "Hidden" Complexity of Manual Tool Execution
import requests

def execute_github_star(tool_call, user_id):
    # 1. Retrieve User's Token (Secure Database logic required here)
    token = db.get_token(user_id, "github")
    
    # 2. Check Expiry & Refresh if needed (OAuth logic required here)
    if token.is_expired():
        token = refresh_oauth_token(token)
    
    # 3. Execute
    try:
        repo = tool_call['args']['repo']
        response = requests.put(
            f"https://api.github.com/user/starred/{repo}",
            headers={"Authorization": f"Bearer {token.access_token}"}
        )
        response.raise_for_status()
    except requests.exceptions.RateLimitExceeded:
        # 4. Implement Retry Logic
        return "Error: Rate limit exceeded. Try again later."
    except Exception as e:
        return f"Error: {str(e)}"
        
    return "Success"
```

**方案 B：Composio 方式。** Composio 充当路由器和执行器。我们向 LLM 提供工具（兼容 OpenAI、Claude 等），并负责执行。

```javascript
from composio import Composio

# Composio handles Auth, Retries, Rate Limits, and Schema definitions
composio = Composio()

# 1. Get the tool definition (Formatted for your specific LLM)
tools = composio.tools.get(
    user_id=user_id,
    tools=["GITHUB_STAR_REPO"]  # Note: 'tools' parameter, not 'actions'
)

# ... LLM generates a tool call ...

# 2. Handle tool calls - use provider.handle_tool_calls()
result = composio.provider.handle_tool_calls(
    user_id=user_id,
    response=tool_call_response  # The LLM response containing tool calls
)
```

### 8.3 兼容现代发现机制

Composio 可以与现代技术栈集成。我们支持 **MCP**，这意味着你可以把 Composio 的 [850+](https://composio.dev/toolkits) 个集成挂载为 MCP 服务器。你将获得标准 MCP 接口，同时享受 Composio 托管的认证与可靠性能力。

## 九、生产就绪检查清单

如果你选择自行构建执行层，请在部署到生产环境之前，确保已经覆盖以下运维要求。

| **组件**             | **要求**                                  | **风险**                                                     |
| :------------------- | :---------------------------------------- | :----------------------------------------------------------- |
| **认证管理**         | 按用户刷新和存储 OAuth Token             | 可能发生[安全漏洞](https://composio.dev/blog/secure-ai-agent-infrastructure-guide)，或者 Agent 因 Token 过期而在任务中途失败。 |
| **可观测性**         | 记录每一次工具调用的输入和输出           | 当 Agent 删除生产数据库时，无法追踪原因。 |
| **速率限制**         | 指数退避和重试逻辑                       | 一个过于激进的 Agent 可能导致你的整个 IP 被 Salesforce 封禁。 |
| **输出标准化**       | 将不同 API 返回的 JSON 输出统一格式      | LLM 可能被 XML 或大量未解析的响应数据干扰。 |
| **权限**             | 权限范围校验（读 vs. 写）                | 一个只被授权“读取”工单的 Agent，可能意外“删除”工单。 |

## 十、总结

Tool Calling 已经成熟。借助 Claude Tool Search，我们已经解决了上下文窗口问题。借助 MCP，我们正在解决接口标准化问题。

但标准化并不等于执行。工程挑战已经从“我该如何连接它”，转变为“我该如何为 10,000 个用户安全地运行它”。

你可以自己构建认证、重试逻辑和治理层，也可以使用专门的执行平台。如果你已经准备好专注于 Agent 行为，而不是集成维护，可以今天就[**用 Composio 连接你的第一个工具**](https://platform.composio.dev/auth)。

> 这是一篇由 [**Manveer Chawla**](https://substack.com/@manveerc) 撰写的客座文章。他是 [Zenith](https://www.tryzenith.ai/) 的联合创始人，他们正在为营销团队构建 AI Agent。他此前曾任 Confluent 工程总监，并在 Dropbox 领导增长工程平台。

## 十一、常见问题

### 11.1 Tool Calling 和 Function Calling 有什么区别？ 

它们通常可以互换使用，都是指 LLM 输出结构化数据来调用外部工具的能力。

### 11.2 什么时候应该使用 Tool Search？ 

Anthropic 建议，当你的 Agent 需要访问 30 个或更多工具时使用 Tool Search，以避免上下文窗口限制并提升准确率。

### 11.3 模型上下文协议（MCP）不解决什么问题？ 

MCP 标准化的是通信，但不处理执行层复杂性，例如 OAuth、速率限制处理或合规日志。

### 11.4 Composio 如何简化工具执行？

Composio 管理完整的执行层，包括认证、Token 刷新和可靠性，同时抽象掉生产环境中所需的复杂集成代码。

### 11.5 Tool Calling 和 Prompt Engineering 有什么区别？

Prompt Engineering 是通过设计提示词来引导 LLM 的**内部推理**，例如要求它“逐步思考”。Tool Calling 则是让 LLM 与**外部系统**交互的能力。你可以使用 Prompt Engineering 帮助模型判断该使用*哪个*工具，但真正执行动作的机制是 Tool Calling。

### 11.6 Tool Calling vs. RAG：我需要哪一个？

你很可能两者都需要，但它们服务于不同目的。

+   **RAG（Retrieval Augmented Generation，检索增强生成）**：用于**读取**静态知识。它检索数据（PDF、文档）为回答提供上下文。
    
+   **Tool Calling：** 用于**行动**以及获取动态数据。它允许 Agent 发送邮件、更新数据库或查看实时股票价格，这些都是静态向量数据库做不到的事情。
    

### 11.7 我可以在 Llama 3 这样的开源模型中使用 Tool Calling 吗？

可以。Llama 3 和 Mistral Large 等现代开源模型已经针对 Tool Calling 进行了微调，可以兼容标准格式。不过，复杂的多步骤编排对模型的结构化输出能力要求更高。相比更小的本地模型，Claude 4.5 Sonnet 或 GPT-5 这类前沿模型，在遵循严格 JSON Schema 方面通常更可靠。

### 11.8 如何处理危险操作（Human-in-the-Loop）？

对于敏感操作，例如 `delete_repo` 或 `transfer_funds`，你不应该允许 LLM 自主执行。你的执行层应该支持 **Human-in-the-Loop（HITL，人在回路）**审批流程：Agent 准备好 Tool Call 后先暂停执行，等人类用户通过 UI 明确批准后再继续。
