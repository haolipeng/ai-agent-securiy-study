# Day 06: 解析 Tool Args

演示模型生成 `read_file` 的结构化参数后，Python 如何解析 JSON，并在执行前做路径校验。

核心点：

- `tool_call.function.arguments` 是模型生成的 JSON 字符串
- Python 侧需要用 `json.loads()` 解析
- 解析后不能直接执行，要先校验参数
- 文件路径必须限制在允许目录内，避免 `../` 越权读取

在项目根目录执行：

```bash
source .venv/bin/activate
export POE_API_KEY=你的密钥
python3 day-06-tool-args/main.py
```

观察输出：

- `模型生成的原始参数`：模型返回的 JSON 字符串
- `Python 解析后的参数`：`json.loads()` 后的 dict
- `读取结果`：路径校验通过后才读取文件

这个 demo 的安全结论：JSON schema 只能约束参数形状，不能代表权限控制。`path` 这类参数必须在工具执行前做目录边界校验。
