from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from .types import StrategyRegistryEntry
from .registry import load_strategy_registry

_obs_log = logging.getLogger("strategy.observability")

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REGISTRY_PATH = (
    _REPO_ROOT
    / "docs"
    / "chantiers"
    / "GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01"
    / "95_STRATEGY_REGISTRY.md"
)

_registry_cache: list[StrategyRegistryEntry] | None = None
_FIXTURE_STRATEGY_IDS = {"e2e_dry_run"}


def _ensure_registry() -> list[StrategyRegistryEntry]:
    global _registry_cache
    if _registry_cache is None:
        _registry_cache = load_strategy_registry(_REGISTRY_PATH)
    return _registry_cache


def validate_strategy_id(strategy_id: str) -> bool:
    if strategy_id in _FIXTURE_STRATEGY_IDS:
        return True
    entries = _ensure_registry()
    return any(entry.strategy_id == strategy_id for entry in entries)


def get_known_ids() -> set[str]:
    entries = _ensure_registry()
    return {entry.strategy_id for entry in entries} | set(_FIXTURE_STRATEGY_IDS)


def lookup_strategy(strategy_id: str) -> StrategyRegistryEntry | None:
    entries = _ensure_registry()
    for entry in entries:
        if entry.strategy_id == strategy_id:
            return entry
    return None


def get_all_entries() -> list[StrategyRegistryEntry]:
    return list(_ensure_registry())


def build_unknown_strategy_warning_payload(strategy_id: str, source: str) -> dict:
    return {
        "event": "STRATEGY_ID_UNKNOWN",
        "metric": "strategy_id.unknown.warning",
        "strategy_id": strategy_id,
        "source": source,
        "mode": "warning_only",
        "runtime_action": "continue",
        "registry_known": False,
    }


def log_unknown_strategy_id_warning(strategy_id: str, source: str) -> None:
    _obs_log.warning(
        "event=STRATEGY_ID_UNKNOWN metric=strategy_id.unknown.warning strategy_id=%r source=%s mode=warning_only runtime_action=continue registry_known=false",
        strategy_id,
        source,
    )
