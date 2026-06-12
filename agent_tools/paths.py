from pathlib import Path

from agent_tools.workspace import ALLOWED_DIRS


def is_path_in_allowlist(file_path: Path) -> bool:
    for allowed_dir in ALLOWED_DIRS:
        if file_path.is_relative_to(allowed_dir):
            return True
    return False


def resolve_allowed_path(*, allowed_dir: Path, path: str, allowlist_error: str) -> tuple[Path | None, dict | None]:
    if ".." in path or path != Path(path).name:
        return None, {"ok": False, "error": "path not allowed", "requested": path}

    file_path = (allowed_dir / path).resolve()
    if not is_path_in_allowlist(file_path):
        return None, {
            "ok": False,
            "error": allowlist_error,
            "requested": path,
            "path": str(file_path),
        }
    return file_path, None
