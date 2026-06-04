# Day 03：Context Window 与 Token

**日期：** 2026-06-03  
**代码：** [`day-03-context-window/main.py`](../../../day-03-context-window/main.py)

## 做了什么

多轮对话历史实验：对话开头埋入口令，中间追加 N 轮无关 user/assistant 往返，最后追问开头口令。通过 `usage.prompt_tokens` 观察上下文长度，验证早期事实是否在 history 过长时丢失。

模型：`gpt-3.5-turbo`（Poe，上下文窗口 16,384 tokens）。口令：`隐藏口令：我是小明`。

## 核心概念

**Token**

模型处理文本的最小单位，不是「一个字」或「一个词」。API 按 token 计费，也按 token 计量上下文长度。



**Context Window（上下文窗口）**

模型一次能「看见」的最大 token 总量，包括输入（prompt）和输出（completion）。超出窗口的内容会被截断或无法进入模型——这就是**截断**。

**截断的实际表现**

- `usage.prompt_tokens` 接近或超过模型窗口上限
- 对话开头的指令或事实，模型回答时「看不见」
- 模型可能**幻觉**出从未出现过的内容，而非简单回答「不知道」

## 实验设计

1. user 让模型记住口令
2. assistant 确认
3. 循环 `filler_rounds` 次，每轮追加一条 user + 一条 assistant 占位对话
4. 最后 user 追问开头口令

改 `FILLER_ROUNDS` 后重新运行，对比 token 用量与回答是否正确。

## 实测结果

| FILLER_ROUNDS | messages 条数 | 总字符数 | prompt_tokens | 模型回答 | 是否正确 |
|---------------|---------------|----------|---------------|----------|----------|
| 80 | 163 | 9,806 | 7,103 | 隐藏口令：我是小明 | 是 |
| 200 | 403 | 24,547 | 17,663 | 口令是"蓝色海洋"。 | 否（幻觉） |

**80 轮（未触顶）**

```
=== 多轮对话历史实验（填充轮数=80） ===
model: gpt-3.5-turbo
messages 条数: 163, 总字符数: 9,806
--- content ---
隐藏口令：我是小明
--- usage: prompt=7103, completion=9, total=7112 ---
```

`prompt_tokens` 约 7.1k，低于 16,384 窗口上限，模型仍能看见对话开头的口令。

**200 轮（超出窗口）**

```
=== 多轮对话历史实验（填充轮数=200） ===
model: gpt-3.5-turbo
messages 条数: 403, 总字符数: 24,547
--- content ---
口令是"蓝色海洋"。
--- usage: prompt=17663, completion=14, total=17677 ---
```

`prompt_tokens` 约 17.7k，**超过** gpt-3.5-turbo 的 16,384 窗口。开头口令很可能已被截断，模型没有回答「不知道」，而是**编造**了「蓝色海洋」——这在 Agent 安全里比「答错」更危险。

## 观察小结

- messages 条数：`2 + filler_rounds × 2 + 1`（开头 2 条 + 每轮 2 条 + 末尾追问 1 条）
- `prompt_tokens` 随填充轮数近似线性增长（80 轮 ≈ 7.1k，200 轮 ≈ 17.7k）
- 字符数不能代替 token 计量，但两者趋势一致
- 窗口未满时记忆正常；超出后不仅遗忘，还可能产生**可信但错误**的幻觉回答

## 响应里看 token

```python
usage = resp.usage
usage.prompt_tokens      # 全部 messages 消耗的 token（含多轮 history）
usage.completion_tokens  # 输出消耗的 token
usage.total_tokens       # 合计
```

## 运行

```bash
source .venv/bin/activate
python3 day-03-context-window/main.py
```

修改 `main.py` 中 `FILLER_ROUNDS`（如 80、120、200）多次运行，找记忆失效的拐点。

## 安全视角

- **上下文污染**：多轮 tool 返回、RAG 片段、闲聊 history 都会占 token，挤掉早期 system 指令或用户设定
- **截断 + 幻觉**：超出窗口后，模型可能编造看似合理的答案，审计时不能只看「有回答」就认为执行成功
- **日志留存**：需记录完整 messages 与 `prompt_tokens`；截断后「模型实际看到了什么」与原始输入不一致
- **检测 implication**：history 轮数或 `prompt_tokens` 异常偏高，可能是 context flooding 攻击前兆
