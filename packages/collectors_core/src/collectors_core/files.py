from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_writable_directory(path: Path) -> None:
    ensure_directory(path)
    with tempfile.NamedTemporaryFile(dir=path, delete=True):
        pass


def ensure_file(path: Path) -> Path:
    ensure_directory(path.parent)
    path.touch(exist_ok=True)
    return path


def atomic_write_json(path: Path, payload: Any) -> None:
    ensure_directory(path.parent)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def append_jsonl(path: Path, payload: Any) -> None:
    ensure_directory(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=False))
        handle.write("\n")


def load_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def module_relative_path(module_dir: Path, path: Path) -> str:
    return path.relative_to(module_dir).as_posix()
