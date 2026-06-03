# Day 01：第一次 LLM API 调用

**日期：** 2026-06-01  
**代码：** [`day-01-first-call/main.py`](../../../day-01-first-call/main.py)

## 做了什么

用 OpenAI SDK 调用 Poe 兼容接口，完成最小 Chat Completions 请求：

一条 `user` message 输入，一段文本输出。



## 关键代码

```python
client = openai.OpenAI(
    api_key=os.getenv("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)

resp = client.chat.completions.create(
    model="Claude-Opus-4.7",
    messages=[{"role": "user", "content": "你是什么大语言模型？"}],
)

print(resp.choices[0].message.content)
```

## 对象说明

| 对象 | 含义 |
|------|------|
| `model` | 使用的模型名 |
| `messages` | 输入对话列表（Day 01 只有一条 user消息） |
| `resp` | 完整响应，含 `id`、`choices`、`usage` |
| `message.content` | **模型回复的纯文本在这里** |

## 运行

在项目根目录执行：

```bash
source .venv/bin/activate
python3 day-01-first-call/main.py
```



## 安全视角

- `POE_API_KEY` 是出站凭证，只能来自环境变量，不能写进代码或提交到 Git
- 每次调用都会产生 request/response，后续 Agent 审计需要记录这类边界流量
