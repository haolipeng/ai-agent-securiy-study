# Day 04：Temperature 与 Streaming

**日期：** 2026-06-04  
**代码：**

- [`main.py`](../../../day-04-temperature-streaming/main.py) — temperature 对比
- [`streaming_demo.py`](../../../day-04-temperature-streaming/streaming_demo.py) — streaming 对比

## 做了什么

**实验 1：temperature 对比**

对同一个开放问题（给 AI Agent 安全审计工具起中文名），分别在 `temperature=0.0 / 0.7 / 1.5` 下各请求 5 次，观察输出稳定性与发散程度。

**实验 2：streaming 对比**

同一 prompt 分别用 `stream=False`（一次性返回）和 `stream=True`（逐 chunk 打印），对比返回方式差异。

模型：`gpt-3.5-turbo`（Poe）。

## 核心概念

**Temperature（温度）——模型有多「敢乱猜」**

可以把它想成**胆量的旋钮**，一般取值 0～2：

- **调低（0.0）**：模型挑「最有把握」的那个词，同样问题多次问，答案往往差不多。你的实验里 5 次只冒出「安审通」「安审者」两个名字，就是这个效果。
- **中间（0.7）**：有一点变化，但不会太离谱。5 次出了 5 个不同名字，但都还是「安审 ××」这类风格。
- **调高（1.5）**：模型更愿意尝试冷门选项，输出更花——出现「安审大师」、带引号的 `"安净检"`、甚至混进英文的 `安标睿OPSEC`。

**什么时候用什么温度？**

- 要**稳定、可重复**（判恶意/ benign、抽字段、跑规则）：用低温，比如 0～0.3。
- 要**写文案、头脑风暴**：可以用 0.7 左右。
- 安全场景里**很少**故意用高温——答案飘了，同一条日志两次结论可能不一样。

**Determinism（确定性）——同样的问题，会不会每次一样？**

不一定。即使 temperature 设成 0，有些 API/模型仍可能有微小随机性；但**温度越低，越像「复制粘贴」**，温度越高越像「每次重新掷骰子」。

**Streaming（流式输出）——字是一个一个蹦出来的**

普通调用：等模型全部写完，一次性返回整段话。  
Streaming：像 ChatGPT 打字那样，**边想边吐字**，前端可以边收边显示。

对用户只是「快一点看到第一个字」；做安全审计时要注意：如果只记录了流的前半截、或者连接中途断了，日志里可能**没有完整回答**。

## 实验设计

**实验 1：temperature**

```python
QUESTION = "给一个 AI Agent 安全审计工具起一个中文名字，要求 2 到 6 个字，只输出名字"
TEMPERATURES = [0.0, 0.7, 1.5]
RUNS_PER_TEMPERATURE = 5
```

同一 prompt、同一 model，只改 `temperature`，每档连跑 5 次。

**实验 2：streaming**

```python
# stream=False：response.choices[0].message.content 一次拿全文
# stream=True：遍历 chunk.choices[0].delta.content 逐块拼接
```

同一 prompt、`temperature=0.7`，先后跑两种模式。最终文本应一致，差别在传输方式与首字到达时间。

## 实测结果

### temperature=0.0

```
=== temperature=0.0 ===
1. 安审通
2. 安审者
3. 安审者
4. 安审通
5. 安审通
```

5 次输出仅 **2 个不同名字**（安审通 ×3、安审者 ×2），高度稳定。

### temperature=0.7

```
=== temperature=0.7 ===
1. 安审宝
2. 安审者
3. 安审者
4. 安审神
5. 安审通
```

5 次输出 **5 个不同名字**，仍集中在「安审 + 单字」风格，整体可控。

### temperature=1.5

```
=== temperature=1.5 ===
1. 安延检
2. 安审大师
3. 审睿达
4. "安净检"
5. 安标睿OPSEC
```

输出明显发散：字数更长（「安审大师」4 字）、结构更多样（「审睿达」去掉「安」前缀）、出现**引号包裹**（`"安净检"`）、甚至混入**英文后缀**（`安标睿OPSEC`），部分结果违反「只输出名字」的隐含格式要求。

## 观察小结

### temperature

| temperature | 5 次中不同名字数 | 稳定性 | 格式遵守 |
|-------------|------------------|--------|----------|
| 0.0 | 2 | 高，大量重复 | 良好 |
| 0.7 | 5 | 中，有变化但语义相近 | 良好 |
| 1.5 | 5 | 低，风格跳跃 | 较差（引号、英文、超长） |

- 开放创意题上，**temperature 越高，同 prompt 的输出方差越大**
- 安全审计、策略判定、结构化抽取等场景，宜用 **低 temperature**，便于复现与规则匹配
- 高 temperature 不仅「更有创意」，还可能**不遵守输出格式**，Agent 若依赖解析器处理 tool 名/JSON，需额外校验

### streaming

- `stream=False`：等模型写完，从 `message.content` 取完整文本，适合落库、审计归档
- `stream=True`：边收边显示，需自己拼接 chunk；审计时必须等流结束再写日志，或标记 `stream_complete=false`
- 两种模式**最终内容应相同**（同 prompt、同 temperature）；差异在 UX 和日志采集时机

## 运行

```bash
source .venv/bin/activate
python3 day-04-temperature-streaming/main.py
python3 day-04-temperature-streaming/streaming_demo.py
```

## 安全视角

- **检测可复现性**：同一告警摘要 + 低 temperature，便于建立 baseline；高 temperature 会使同一输入的判定结果漂移，不利于规则回归测试
- **结构化输出**：Agent tool call、JSON 抽取应使用低 temperature，并对输出做 schema 校验——高 temperature 易出现引号、多余文字、字段漂移
- **结构化日志**：审计时应记录 `temperature`、`model`、`stream`、完整 prompt 与 response，否则无法解释「同输入为何不同结论」
- **streaming 日志**：流式场景需确认是否收到完整响应；连接中断时只记了前半段，等于审计证据不完整
