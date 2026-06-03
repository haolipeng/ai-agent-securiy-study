# Day 04: Temperature 与 Streaming

演示同一个开放问题在不同 temperature 下的输出差异。

实验会对每个 temperature 连续请求 5 次，方便观察：

- `0.0`：输出更稳定
- `0.7`：可能有轻微变化
- `1.5`：输出更发散

当前包含两个实验：

- `main.py`：temperature 对比
- `streaming_demo.py`：streaming 流式输出

## 实测结果（gpt-3.5-turbo，每档 5 次）

| temperature | 输出 | 不同名字数 |
|-------------|------|------------|
| 0.0 | 安审通、安审者、安审者、安审通、安审通 | 2 |
| 0.7 | 安审宝、安审者、安审者、安审神、安审通 | 5 |
| 1.5 | 安延检、安审大师、审睿达、"安净检"、安标睿OPSEC | 5 |

1.5 时出现引号包裹、英文后缀、超长名字，格式遵守明显变差。

详细分析与原始输出见 [Day 04 笔记](../docs/notes/week-01/day-04-temperature-streaming.md)。

在项目根目录执行（需已设置环境变量 `POE_API_KEY`）：

```bash
source .venv/bin/activate
python3 day-04-temperature-streaming/main.py
python3 day-04-temperature-streaming/streaming_demo.py
```
