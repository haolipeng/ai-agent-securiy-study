# Day 05: Tool Schema

演示两个最小工具的 tool schema。

这个 demo 使用真实链路：

```text
user input
  -> LLM 调用 get_city_location
  -> 工具返回 latitude / longitude
  -> LLM 调用 get_current_weather
  -> 工具返回当前温度
```

它会调用 Poe 的 OpenAI-compatible API，让模型根据 schema 生成 `tool_calls`，再调用 Open-Meteo 的免费 API 查询真实数据。

当前提供两个工具：

- `get_city_location`：查询城市经纬度
- `get_current_weather`：根据经纬度查询当前温度

核心结构：

- `name`：工具名称
- `description`：工具能做什么
- `parameters`：工具需要哪些参数
- `required`：哪些参数必须提供

`get_city_location` 要求城市名称：

```json
{
  "city": "Shanghai"
}
```

`get_current_weather` 要求经纬度：

```json
{
  "latitude": 31.22222,
  "longitude": 121.45806
}
```

在项目根目录执行：

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-05-tool-schema/main.py
```

默认模型是 `gpt-3.5-turbo`。如需切换：

```bash
export POE_MODEL=Claude-Opus-4.7
```

观察输出中的几段内容：

- `tool schema`：工具说明书列表
- `user input`：用户原始输入
- `第 1 次工具调用`：模型先查询城市经纬度
- `第 2 次工具调用`：模型再用经纬度查询天气

## read_file 攻击面演示

离线运行：

```bash
python3 day-05-tool-schema/read_file_attack_surface.py
```

这个脚本演示同一个 `read_file` schema 下，模型参数 `{"path": "../demo_secret.txt"}` 如果直接执行，会读到工作区外的文件；加上路径归一化和目录边界校验后，会被拒绝。
