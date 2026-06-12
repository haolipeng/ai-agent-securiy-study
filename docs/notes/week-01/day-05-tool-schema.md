# Day 05：Tool Schema

**日期：** 2026-06-04  
**代码：** [`main.py`](../../../day-05-tool-schema/main.py)

## 做了什么

用户问「查询上海的天气」，模型根据两个 tool schema 分两步调用：先用 `get_city_location` 查经纬度，再用 `get_current_weather` 查温度。全程由 Python 执行层调用 Open-Meteo 免费 API 返回真实数据。

模型：`gpt-3.5-turbo`（Poe）。

## 核心概念

**Tool Schema 怎么写**

OpenAI API 里，每个工具是一个 JSON 对象，固定包在 `type: "function"` 下：

```json
{
  "type": "function",
  "function": {
    "name": "get_city_location",
    "description": "查询某个城市的经纬度。",
    "parameters": {
      "type": "object",
      "properties": {
        "city": { "type": "string", "description": "城市名称，例如 Shanghai。" }
      },
      "required": ["city"]
    }
  }
}
```

| 字段 | 作用 |
|------|------|
| `name` | 调用哪个函数；模型输出 `tool_calls` 时引用 |
| `description` | **什么时候**该用这个工具；影响模型在多个工具间的选择 |
| `parameters` | **调用时传什么参数**；写给 LLM 的入参说明书（填哪些项、什么类型、哪些必填） |

三个字段合起来描述「怎么调用」：`name` 选函数，`description` 决定何时选它，`parameters` 决定选中后 arguments JSON 长什么样。

多个工具组成列表，通过 `tools=[...]` 传给 API。

**注册到大模型的作用**

每次 `chat.completions.create(..., tools=TOOL_SCHEMAS)` 时，schema 会随请求进入模型上下文。模型据此知道「当前有哪些能力可用」，并在需要时输出结构化 `tool_calls`（工具名 + JSON 参数），而不是只回自然语言。

本 demo 里用户问天气，模型看到两份 schema：`description` 帮它决定先调 `get_city_location`、再调 `get_current_weather`；`parameters` 帮它生成 `{"city": "Shanghai"}` 和 `{"latitude": ..., "longitude": ...}`。

**Schema 不等于执行** — schema 只参与模型决策；真正跑代码的是 runtime（`AVAILABLE_TOOLS`）。模型返回 `tool_calls` 后，执行层负责解析、校验、调用。

**tool_choice** — `"auto"` 时模型自选工具；也可强制指定（day-06 会用）。

## 实验设计

```python
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "根据经纬度查询当前位置的当前天气。",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", ...},
                "longitude": {"type": "number", ...},
            },
            "required": ["latitude", "longitude"],
        },
    },
}

LOCATION_TOOL = { ... "name": "get_city_location", "required": ["city"] ... }

client.chat.completions.create(
    messages=messages,
    tools=[WEATHER_TOOL, LOCATION_TOOL],
    tool_choice="auto",
    temperature=0,
)
```

system prompt 明确要求「先查经纬度，再查天气」，引导模型按依赖顺序选工具。

## 实测结果

### 第 1 次工具调用

```
模型选择工具: get_city_location
模型生成参数: {"city": "Shanghai"}
解析后的参数: {"city": "Shanghai"}
工具返回结果:
{
  "city": "Shanghai, China",
  "latitude": 31.22222,
  "longitude": 121.45806
}
```

用户说的是「上海」，模型把 city 填成 `"Shanghai"`（英文地名），说明 **parameters 里字段的 description 示例会影响填参格式**。

### 第 2 次工具调用

```
模型选择工具: get_current_weather
模型生成参数: {"latitude": 31.22222, "longitude": 121.45806}
工具返回结果:
{
  "纬度": 31.22222,
  "经度": 121.45806,
  "温度": "31.0°C",
  "时间": "2026-06-12T09:45"
}
```

第 2 次请求的 `messages` 已包含第 1 次的 assistant `tool_calls` 和 `role: tool` 结果，模型从 tool result 里取出经纬度，没有再让用户重复提供。

## 观察小结

- schema 告诉模型「有哪些工具、何时选用、传什么参数」，但不执行代码、不代替 runtime 校验
- 多工具调用顺序靠 system prompt + 上一轮 tool result 引导，不由 parameters 决定
- `description` 影响选工具；`parameters` 里各字段的 `description` 影响填参格式

完整链路：

```text
user input
  → LLM 看 tools schema，返回 tool_calls
  → runtime 执行 get_city_location
  → role: tool 回传经纬度
  → LLM 再次返回 tool_calls
  → runtime 执行 get_current_weather
  → 得到温度
```

## 运行

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-05-tool-schema/main.py
```

可选：`export POE_MODEL=Claude-Opus-4.7`

## 安全视角

- **Schema 是声明，不是 enforcement**：参数校验、权限控制都在执行层完成（day-06 起展开）
- **工具注册表是边界**：`AVAILABLE_TOOLS` 只暴露允许的函数；模型 hallucinate 出 schema 里没有的工具名，执行层也应拒绝
- **审计要记 schema 版本**：工具增删、description 改动会改变模型行为，日志里应能还原当时注册了哪些 tools
