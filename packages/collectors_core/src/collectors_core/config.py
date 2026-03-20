from __future__ import annotations

import os
import re
import tomllib
from copy import deepcopy
from pathlib import Path
from typing import Any

from .errors import ConfigurationError


def module_env_prefix(module_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", module_id).upper()
    return f"{normalized}__"


def load_config_layers(module_dir: Path, module_id: str) -> dict[str, Any]:
    config_dir = module_dir / "config"
    defaults_path = config_dir / "defaults.toml"
    local_path = config_dir / "local.toml"

    if not defaults_path.exists():
        raise ConfigurationError(f"Missing required config file: {defaults_path}")

    config = _load_toml(defaults_path)
    if local_path.exists():
        config = _deep_merge(config, _load_toml(local_path))

    return _deep_merge(config, _load_env_overrides(module_id, os.environ))


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        raise ConfigurationError(f"Config file must contain a top-level table: {path}")
    return data


def _load_env_overrides(module_id: str, env: dict[str, str] | os._Environ[str]) -> dict[str, Any]:
    prefix = module_env_prefix(module_id)
    overrides: dict[str, Any] = {}
    for key, value in env.items():
        if not key.startswith(prefix):
            continue
        suffix = key[len(prefix) :]
        if not suffix:
            continue
        path_parts = [part.strip().lower() for part in suffix.split("__") if part.strip()]
        if not path_parts:
            continue

        cursor = overrides
        for part in path_parts[:-1]:
            next_cursor = cursor.get(part)
            if not isinstance(next_cursor, dict):
                next_cursor = {}
                cursor[part] = next_cursor
            cursor = next_cursor
        cursor[path_parts[-1]] = value
    return overrides


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _deep_merge(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged
