from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .types import StrategyRegistryEntry
from .registry import load_strategy_registry

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REGISTRY_PATH = (
    _REPO_ROOT
    / "docs"
    / "chantiers"
    / "GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01"
    / "95_STRATEGY_REGISTRY.md"
)

_registry_cache: list[StrategyRegistryEntry] | None = None


def _ensure_registry() -> list[StrategyRegistryEntry]:
    global _registry_cache
    if _registry_cache is None:
        _registry_cache = load_strategy_registry(_REGISTRY_PATH)
    return _registry_cache


def validate_strategy_id(strategy_id: str) -> bool:
    entries = _ensure_registry()
    return any(entry.strategy_id == strategy_id for entry in entries)


def get_known_ids() -> set[str]:
    entries = _ensure_registry()
    return {entry.strategy_id for entry in entries}


def lookup_strategy(strategy_id: str) -> StrategyRegistryEntry | None:
    entries = _ensure_registry()
    for entry in entries:
        if entry.strategy_id == strategy_id:
            return entry
    return None


def get_all_entries() -> list[StrategyRegistryEntry]:
    return list(_ensure_registry())
