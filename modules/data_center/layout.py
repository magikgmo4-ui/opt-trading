from __future__ import annotations

import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

_PRODUCER_FAMILIES: dict[str, list[str]] = {
    "derivatives": [
        "derivatives_collector__bitget",
        "derivatives_collector__binance",
    ],
    "spot": [
        "collector_binance_spot",
    ],
}

_SUBDIRS = ("raw", "normalized", "cache/by_symbol")
_APPEND_FILES = ("events.jsonl", "errors.jsonl")

_REGISTRY_DIR = Path(__file__).parent / "registry"


def ensure_data_center_dirs(root: Path | None = None) -> Path:
    """Create data/data_center/ tree for all declared producers.

    Returns the data/data_center/ base path. Idempotent.
    data/ is gitignored — this layout exists only at runtime.
    """
    root = root if root is not None else _PROJECT_ROOT
    base = root / "data" / "data_center"

    for family, producers in _PRODUCER_FAMILIES.items():
        for producer_id in producers:
            prod_dir = base / family / producer_id
            for subdir in _SUBDIRS:
                (prod_dir / subdir).mkdir(parents=True, exist_ok=True)
            for fname in _APPEND_FILES:
                f = prod_dir / fname
                if not f.exists():
                    f.touch()

    (base / "_registry").mkdir(parents=True, exist_ok=True)
    return base


def get_producer_dir(family: str, producer_id: str, root: Path | None = None) -> Path:
    """Return the Data Center directory path for a given producer."""
    root = root if root is not None else _PROJECT_ROOT
    return root / "data" / "data_center" / family / producer_id


def load_producers_registry() -> dict:
    """Load the canonical producers registry from modules/data_center/registry/."""
    return json.loads((_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))


def load_consumers_registry() -> dict:
    """Load the canonical consumers registry from modules/data_center/registry/."""
    return json.loads((_REGISTRY_DIR / "consumers.json").read_text(encoding="utf-8"))
