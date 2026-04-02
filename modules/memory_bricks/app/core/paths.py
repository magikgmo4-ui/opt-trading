from __future__ import annotations

import os
from pathlib import Path

from app.core.constants import DEFAULT_STATE_ROOT


def get_state_root() -> Path:
    return Path(os.environ.get("MEMORY_BRICKS_STATE_ROOT", str(DEFAULT_STATE_ROOT))).expanduser()

def get_bricks_dir() -> Path:
    return get_state_root() / "bricks"

def get_index_dir() -> Path:
    return get_state_root() / "index"

def get_exports_dir() -> Path:
    return get_state_root() / "exports"

def get_handoffs_dir() -> Path:
    return get_state_root() / "handoffs"

def get_meta_dir() -> Path:
    return get_state_root() / "meta"

def get_tmp_dir() -> Path:
    return get_state_root() / "tmp"

def get_sequence_path() -> Path:
    return get_meta_dir() / "sequence.json"

def ensure_state_dirs() -> None:
    for path in [
        get_bricks_dir(),
        get_index_dir(),
        get_index_dir() / "by_project",
        get_index_dir() / "by_module",
        get_index_dir() / "by_machine",
        get_index_dir() / "by_ia",
        get_exports_dir(),
        get_handoffs_dir(),
        get_meta_dir(),
        get_tmp_dir(),
    ]:
        path.mkdir(parents=True, exist_ok=True)
