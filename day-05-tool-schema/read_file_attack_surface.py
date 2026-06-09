import json
import tempfile
from pathlib import Path


read_file_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "读取工作区里的文本文件。",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "要读取的文件路径，例如 notes.txt。",
                }
            },
            "required": ["path"],
        },
    },
}


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        workspace = base_dir / "workspace"
        workspace.mkdir()

        (base_dir / "secret.txt").write_text("DEMO_SECRET=do_not_expose\n", encoding="utf-8")

        attack_args = {"path": "../secret.txt"}

        print("--- read_file tool schema ---")
        print(json.dumps(read_file_schema, indent=2, ensure_ascii=False))

        print("\n--- 模型生成的危险参数 ---")
        print(json.dumps(attack_args, ensure_ascii=False))

        print("\n--- 没有校验：直接读取模型给的 path ---")
        print((workspace / attack_args["path"]).read_text(encoding="utf-8").strip())

        safe_path = (workspace / attack_args["path"]).resolve()

        print("\n--- 加上校验：只允许读取 workspace 目录内的文件 ---")
        if not safe_path.is_relative_to(workspace.resolve()):
            print(f"拒绝读取越权路径: {attack_args['path']}")
        else:
            print(safe_path.read_text(encoding="utf-8").strip())

        print("\n结论：schema 只是参数说明，不是权限控制；path 必须在执行前校验。")


if __name__ == "__main__":
    main()
