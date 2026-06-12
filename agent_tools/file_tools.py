from pathlib import Path

from agent_tools.paths import resolve_allowed_path
from agent_tools.shell_tools import run_allowed_command


def read_allowed_file(*, allowed_dir: Path, path: str) -> dict:
    file_path, error = resolve_allowed_path(
        allowed_dir=allowed_dir, path=path, allowlist_error="read path not in allowlist"
    )
    if error:
        return error

    if not file_path.is_file():
        return {"ok": False, "error": "not a file", "requested": path, "path": str(file_path)}

    return {"ok": True, "content": file_path.read_text(encoding="utf-8"), "path": str(file_path)}


def write_allowed_file(*, allowed_dir: Path, path: str, content: str) -> dict:
    file_path, error = resolve_allowed_path(
        allowed_dir=allowed_dir, path=path, allowlist_error="write path not in allowlist"
    )
    if error:
        return error

    file_path.write_text(content, encoding="utf-8")
    return {"ok": True, "path": str(file_path), "bytes_written": len(content.encode("utf-8"))}


def execute_tool(*, tool: str, workspace: Path, args: dict) -> dict:
    if tool == "read_file":
        path = args.get("path")
        return (
            read_allowed_file(allowed_dir=workspace, path=path)
            if isinstance(path, str)
            else {"ok": False, "error": "missing path"}
        )

    if tool == "write_file":
        path, content = args.get("path"), args.get("content")
        if not isinstance(path, str) or not isinstance(content, str):
            return {"ok": False, "error": "missing path or content"}
        return write_allowed_file(allowed_dir=workspace, path=path, content=content)

    if tool == "run_shell_command":
        command = args.get("command")
        cmd_args = args.get("args", [])
        if not isinstance(command, str):
            return {"ok": False, "error": "missing command"}
        if cmd_args is None:
            cmd_args = []
        return run_allowed_command(allowed_dir=workspace, command=command, args=cmd_args)

    return {"ok": False, "error": f"unknown tool: {tool}"}
