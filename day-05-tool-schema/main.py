import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

import openai

MODEL = "gpt-3.5-turbo"
USER_INPUT = "查询上海的天气"

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "根据经纬度查询当前位置的当前天气。",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "纬度，例如 31.22222。",
                },
                "longitude": {
                    "type": "number",
                    "description": "经度，例如 121.45806。",
                }
            },
            "required": ["latitude", "longitude"],
        },
    },
}


LOCATION_TOOL = {
    "type": "function",
    "function": {
        "name": "get_city_location",
        "description": "查询某个城市的经纬度。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如 Shanghai、Beijing 或 New York。",
                }
            },
            "required": ["city"],
        },
    },
}

TOOL_SCHEMAS = [WEATHER_TOOL, LOCATION_TOOL]


def get_json(url: str, params: dict) -> dict:
    query = urlencode(params)
    return json.loads(urlopen(f"{url}?{query}", timeout=10).read())


def get_city_location(city: str) -> dict:
    geo = get_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": city, "count": 1, "language": "en", "format": "json"},
    )
    location = geo["results"][0]

    return {
        "city": f"{location['name']}, {location['country']}",
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


def get_current_weather(latitude: float, longitude: float) -> dict:
    weather = get_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m", #当前 2 米高度气温
            "timezone": "auto",
        },
    )

    # 获取天气数据和单位比如 °C
    current = weather["current"]
    units = weather["current_units"]

    # 返回工具结果，给读者查看
    return {
        "纬度": latitude,
        "经度": longitude,
        "温度": f"{current['temperature_2m']}{units['temperature_2m']}",
        "时间": current["time"],
    }


AVAILABLE_TOOLS = {
    "get_current_weather": get_current_weather,
    "get_city_location": get_city_location,
}


def chat(client, messages):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto",
        temperature=0,
    )


def run_tool_call(tool_call) -> dict:
    tool_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments
    arguments = json.loads(tool_call.function.arguments)
    result = AVAILABLE_TOOLS[tool_name](**arguments)

    print(f"模型选择工具: {tool_name}")
    print(f"模型生成参数: {raw_arguments}")
    print(f"解析后的参数: {json.dumps(arguments, ensure_ascii=False)}")
    print(f"Agent runtime 执行: AVAILABLE_TOOLS[{tool_name!r}](**arguments)")
    print("工具返回结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


def main() -> None:
    client = openai.OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )

    messages = [
        {
            "role": "system",
            "content": "你是天气助手。查询天气时，先用 get_city_location 查询经纬度，再用 get_current_weather 查询天气。",
        },
        {"role": "user", "content": USER_INPUT},
    ]

    print("--- 工具 schema 列表 ---")
    print(json.dumps(TOOL_SCHEMAS, indent=2, ensure_ascii=False))

    print("\n--- 用户输入 ---")
    print(USER_INPUT)

    print("\n--- 第 1 次请求：让模型选择第一个工具 ---")
    print(json.dumps(messages, indent=2, ensure_ascii=False))
    first_response = chat(client, messages)

    first_message = first_response.choices[0].message
    first_tool_call = first_message.tool_calls[0]

    print("\n--- 第 1 次工具调用：查询经纬度 ---")
    first_result = run_tool_call(first_tool_call)

    messages.append(first_message.model_dump())
    messages.append(
        {
            "role": "tool",
            "tool_call_id": first_tool_call.id,
            "content": json.dumps(first_result, ensure_ascii=False),
        }
    )

    print("\n--- 第 2 次请求：把第 1 次工具结果交回模型 ---")
    print(json.dumps(messages, indent=2, ensure_ascii=False))
    second_response = chat(client, messages)
    second_tool_call = second_response.choices[0].message.tool_calls[0]

    print("\n--- 第 2 次工具调用：查询天气 ---")
    run_tool_call(second_tool_call)


if __name__ == "__main__":
    main()
