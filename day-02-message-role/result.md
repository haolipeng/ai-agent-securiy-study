一、注释掉assistant提示词的结果

```
[system] 你是一个 AI Agent 安全助教。
[user] system、user、assistant 三种 role 分别做什么？
[user] 用简短的话语来描述，为什么 system 更像策略输入？
--- content ---
# 三种 Role 的作用

- **system**：设定规则、人设、任务边界、输出格式等"运行策略"。通常在对话最开始，由开发者写入。
- **user**：终端用户的输入，提出问题或下达指令。
- **assistant**：模型的回复，也作为多轮对话的历史上下文。

# 为什么 system 更像"策略输入"

因为它不是用来"被回答"的内容，而是用来**约束模型如何回答**——定义角色、权限、风格和禁区。它在整段对话中持续生效，优先级高于 user，相当于给模型预设了一份"行为策略/规则"，而不是一次具体的任务请求。
--- response ---
{
  "id": "chatcmpl-0453ada54b91519156d43e5b",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "# 三种 Role 的作用\n\n- **system**：设定规则、人设、任务边界、输出格式等\"运行策略\"。通常在对话最开始，由开发者写入。\n- **user**：终端用户的输入，提出问题或下达指令。\n- **assistant**：模型的回复，也作为多轮对话的历史上下文。\n\n# 为什么 system 更像\"策略输入\"\n\n因为它不是用来\"被回答\"的内容，而是用来**约束模型如何回答**——定义角色、权限、风格和禁区。它在整段对话中持续生效，优先级高于 user，相当于给模型预设了一份\"行为策略/规则\"，而不是一次具体的任务请求。",
        "refusal": null,
        "role": "assistant",
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1780392080,
  "model": "Claude-Opus-4.7",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 222,
    "prompt_tokens": 54,
    "total_tokens": 276,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  }
}

```



二、有assistant提示词的结果

```
[system] 你是一个 AI Agent 安全助教。
[user] system、user、assistant 三种 role 分别做什么？
[assistant] system 设定规则和人设，user 是用户提问，assistant 是模型回复，也用于保存多轮对话历史。
[user] 用简短的话语来描述，为什么 system 更像策略输入？

--- content ---
因为 system 不是普通对话内容，而是给模型设定的行为准则、角色和约束，决定它"怎么回答"而不是"回答什么"，类似于在执行前注入的策略配置。

--- response ---
{
  "id": "chatcmpl-eaad1b00298590bd3b96ef05",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "因为 system 不是普通对话内容，而是给模型设定的行为准则、角色和约束，决定它\"怎么回答\"而不是\"回答什么\"，类似于在执行前注入的策略配置。",
        "refusal": null,
        "role": "assistant",
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1780392105,
  "model": "Claude-Opus-4.7",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 73,
    "prompt_tokens": 89,
    "total_tokens": 162,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  }
}

```

