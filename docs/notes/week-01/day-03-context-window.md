# Day 03：Context Window 与 Token

**日期：** 2026-06-03  
**代码：** [`day-03-context-window/main.py`](../../../day-03-context-window/main.py)

## 做了什么

对比短输入与长输入两次 API 调用，通过 `usage` 字段观察 token 用量，并验证文首信息在长上下文中是否会被「挤掉」。

## 核心概念

**Token**

模型处理文本的最小单位，不是「一个字」或「一个词」。英文常按子词切分，中文通常接近字/词粒度。API 按 token 计费，也按 token 计量上下文长度。

**Context Window（上下文窗口）**

模型一次能「看见」的最大 token 总量，包括输入（prompt）和输出（completion）。超出窗口的内容会被截断或无法进入模型——这就是**截断**。

**截断的实际表现**

- `usage.prompt_tokens` 不再随输入线性增长（触顶）
- 文首、文中的重要指令或事实，模型回答时「看不见」
- Agent 场景下，早期 system 规则或被 RAG 注入的恶意内容，都可能因截断而失效或产生非预期优先级

## 实验设计

**实验 1：短输入基线**

```python
{"role": "user", "content": "用一句话解释 token 和 context window 分别是什么。"}
```

记录 `prompt_tokens`、`completion_tokens`、`total_tokens` 作为对照。

**实验 2：长输入 + 文首追问**

文首写入 `隐藏口令：BLUE-42`，中间用 `FILLER_PARAGRAPHS` 段占位文本撑长输入，末尾追问口令。

```python
FILLER_PARAGRAPHS = 80  # 改大（如 100、300）再运行，对比结果
```

## 建议对比

| 操作 | 观察点 |
|------|--------|
| 默认 `FILLER_PARAGRAPHS = 80` | 能否答对 BLUE-42；`prompt_tokens` 多少 |
| 改大到 200+ | 是否答错或含糊；`prompt_tokens` 是否触顶 |
| 把 needle 改到文中间 | 比文首更容易被遗忘 |

## 响应里看 token

```python
usage = resp.usage
usage.prompt_tokens      # 输入消耗的 token
usage.completion_tokens  # 输出消耗的 token
usage.total_tokens       # 合计
```

## 运行

```bash
source .venv/bin/activate
python3 day-03-context-window/main.py
```

## 安全视角

- **上下文污染**：RAG 检索、工具返回、历史对话都会占 token；恶意内容挤占窗口可覆盖原有 system 指令
- **日志留存**：审计 Agent 行为需记录完整 prompt 与 token 用量；截断后「模型实际看到了什么」与原始输入可能不一致
- **检测 implication**：异常长的 user/RAG 输入可能是攻击前兆（flooding context）
