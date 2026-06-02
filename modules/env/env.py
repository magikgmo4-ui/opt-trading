from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional, Dict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]

def project_root() -> Path:
    return _PROJECT_ROOT

def ensure_dirs() -> Dict[str, Path]:
    """
    Ensure runtime dirs exist (tmp/, data/). Returns their paths.
    """
    tmp = _PROJECT_ROOT / "tmp"
    data = _PROJECT_ROOT / "data"
    tmp.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    return {"tmp": tmp, "data": data}

def load_env(dotenv_path: Optional[Path] = None) -> None:
    """
    Minimal env loader:
    - If python-dotenv exists, load .env and optional local overlays
    - Otherwise do nothing (env must be set by systemd/export)
    """
    env_paths = [dotenv_path] if dotenv_path is not None else [
        _PROJECT_ROOT / ".env",
        _PROJECT_ROOT / ".env.local",
        _PROJECT_ROOT / ".env.telegram.local",
    ]
    try:
        from dotenv import load_dotenv  # type: ignore
        for index, env_path in enumerate(env_paths):
            if env_path.exists():
                load_dotenv(env_path, override=index > 0)
    except Exception:
        # no python-dotenv installed or failure: ignore
        pass

def get_setting(name: str, default: Any = None) -> Any:
    return os.environ.get(name, default)
