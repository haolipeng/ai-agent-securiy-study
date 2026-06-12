import subprocess
from pathlib import Path

ALLOWED_COMMANDS = frozenset({"echo", "ls"})
COMMAND_TIMEOUT_SECONDS = 10


def run_allowed_command(*, allowed_dir: Path, command: str, args: list) -> dict:
    if command not in ALLOWED_COMMANDS:
        return {"ok": False, "error": "command not in allowlist", "requested": command}

    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        return {"ok": False, "error": "args must be a list of strings", "requested": command}

    cwd = allowed_dir.resolve()
    try:
        completed = subprocess.run(
            [command, *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "command timed out", "command": command, "args": args}

    return {
        "ok": completed.returncode == 0,
        "command": command,
        "args": args,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "exit_code": completed.returncode,
    }
