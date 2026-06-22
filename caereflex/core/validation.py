from __future__ import annotations
from pathlib import Path
from .errors import PathSafetyError


def is_path_within(path: Path, workspace: Path) -> bool:
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def assert_safe_workspace_path(path: Path, workspace: Path) -> Path:
    resolved = path.resolve()
    if not is_path_within(resolved, workspace):
        raise PathSafetyError(f"Path is outside configured workspace: {path}")
    return resolved


def safe_display_path(path: Path, workspace: Path | None = None) -> str:
    p = Path(path)
    if workspace is not None:
        try:
            return str(p.resolve().relative_to(workspace.resolve())).replace('\\', '/')
        except Exception:
            pass
    return p.name
