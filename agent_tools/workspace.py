from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "lab" / "workspace"
ALLOWED_DIRS = [WORKSPACE.resolve()]
