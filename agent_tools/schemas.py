READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取 lab/workspace 根目录下的文本文件。只能传文件名，例如 notes.txt。",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "文件名，例如 notes.txt"}},
            "required": ["path"],
        },
    },
}

WRITE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "写入 lab/workspace 根目录下的文本文件。只能传文件名，例如 draft.txt。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件名，例如 draft.txt"},
                "content": {"type": "string", "description": "要写入的文本内容"},
            },
            "required": ["path", "content"],
        },
    },
}

TOOL_SCHEMAS = {
    "read_file": READ_FILE_SCHEMA,
    "write_file": WRITE_FILE_SCHEMA,
}

TOOLS = [READ_FILE_SCHEMA, WRITE_FILE_SCHEMA]
