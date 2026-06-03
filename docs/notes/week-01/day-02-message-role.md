# Day 02：Message 与 Role

**日期：** 2026-06-02  
**代码：** [`day-02-message-role/main.py`](../../../day-02-message-role/main.py)  
**实验输出：** [`day-02-message-role/result.md`](../../../day-02-message-role/result.md)

## 做了什么

在 Day 01 基础上，用 `messages` 列表演示三种 role，并对比有无 `assistant` 历史时输出差异。

## 三种 Role

把一次 API 调用想成「带着聊天记录去提问」——`messages` 就是那份记录，里面每条消息都有一个 `role`：

**System —— 开聊前的规矩**

开发者在对话开始前写好，告诉模型：你是谁、能答什么、不能答什么、怎么说。

它不像聊天内容，更像贴在墙上的**考场纪律**。实验 1 里这句就是 system：

> 你是有 5 年经验的安全工程师，只回答 Agent 运行时安全问题，回答简洁，不超过 80 字。

后面 user 问什么，模型都会按这套规矩来答。改 system，输出风格就变；这就是为什么 system 更像**策略输入**。

**User —— 你真正想问的**

用户每次输入的问题或指令。实验 1 里：

> 什么是 prompt injection？

这就是今天要做的事。User 推动对话，但不决定模型「以什么身份、什么规则」来回答——那是 system 的事。

**Assistant —— 模型上一轮说了什么**

正常流程里，assistant 是 API 返回的回复。多轮对话时，你要把**之前的 assistant 回复**也放进 `messages`，模型才知道上下文。

实验 2 里手动填的 assistant，就是在模拟「上一轮已经解释过三种 role 了」。所以第二轮 user 只问「为什么 system 更像策略输入」，模型能接上；如果把 assistant 删掉，模型就不知道你在追问什么，会从头再讲一遍。

**顺序：** `system → user → assistant → user → …`

**为什么要带全？** API 本身不记历史——每次请求都是全新的，你发什么它看什么。漏了 assistant，就等于跟模型说「我们之前没聊过」。

## 实验设计

**实验 1：system 控制输出**

```python
messages = [
    {"role": "system", "content": "你是有 5 年经验的安全工程师，只回答 Agent 运行时安全问题，回答简洁，不超过 80 字。"},
    {"role": "user", "content": "什么是 prompt injection？"},
]
```

改 system 的 `content`（如换成「用英文回答」），输出风格会变，user 可不变。

**实验 2：assistant 承载上下文**

```python
messages = [
    {"role": "system", "content": "你是一个 AI Agent 安全助教。"},
    {"role": "user", "content": "system、user、assistant 三种 role 分别做什么？"},
    {"role": "assistant", "content": "system 设定规则和人设，user 是用户提问，assistant 是模型回复，也用于保存多轮对话历史。"},
    {"role": "user", "content": "用简短的话语来描述，为什么 system 更像策略输入？"},
]
```

注释掉 `assistant` 条目再运行，第二轮 user 的追问缺少上文，模型会重新解释三种 role。

## 实验结果

| 条件 | 行为 | completion tokens |
|------|------|-------------------|
| 无 assistant | 重新解释 role，再答「为什么 system 像策略输入」 | ~222 |
| 有 assistant | 直接简短回答追问 | ~73 |

结论：`assistant` 是对话记忆；缺失时追问语义断裂，token 消耗也更高。

## 响应体怎么看

```python
resp.choices[0].message.content   # 回复文本（str）
resp.choices[0].message.model_dump()  # 单条 message（含 role）
resp.model_dump()                 # 完整响应（含 usage）
```

## 运行

在项目根目录执行：

```bash
source .venv/bin/activate
python3 day-02-message-role/main.py
```
