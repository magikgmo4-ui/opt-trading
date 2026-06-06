"""Registry cache — loads compiled indexes into memory, provides O(1) lookups.

Hot path: get_cache() returns the active cache dict (never None after init).
Cold path: rebuild_cache() reloads from compiled JSON files.

Rules:
  - No JSON file reads in hot path (load_cache or rebuild_cache only)
  - Atomic pointer swap (threading.Lock)
  - If compiled indexes missing, rebuild them first
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import threading
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

COMPILED_DIR = REPO_ROOT / "data" / "data_center" / "_registry" / "compiled"

_cache: Dict[str, Any] | None = None
_cache_lock = threading.Lock()


# --- Hot path ---

def get_cache() -> Dict[str, Any]:
    """Return the active in-memory cache. Loads if not yet initialized."""
    global _cache
    if _cache is not None:
        return _cache
    with _cache_lock:
        if _cache is None:
            _cache = _load_all()
    return _cache


def invalidate_cache() -> None:
    """Force reload on next access."""
    global _cache
    with _cache_lock:
        _cache = None


def rebuild_cache() -> Dict[str, Any]:
    """Rebuild compiled indexes and reload cache. Atomic swap."""
    from modules.data_center.registry_index_builder import rebuild_all
    rebuild_all()
    new_cache = _load_all()
    global _cache
    with _cache_lock:
        _cache = new_cache
    return _cache


# --- Lookup helpers (hot path safe) ---

def get_by_contract_class(contract_class: str) -> Optional[Dict]:
    cache = get_cache()
    return cache.get("by_contract_class", {}).get(contract_class)


def get_by_data_key(data_key: str) -> Optional[Dict]:
    cache = get_cache()
    return cache.get("by_data_key", {}).get(data_key)


def get_candidates(contract_class: str, data_key: str, symbol: str | None = None) -> Dict[str, Any]:
    """Return candidate information for a data_key in a contract_class.
    
    Returns dict with: producers (list of producer_ids eligible),
    sources (all candidate source_ids), P_class, criticality.
    """
    info = get_by_data_key(data_key)
    if not info:
        return {"producers": [], "sources": [], "P_class": [], "criticality": 99}
    if info.get("contract_class") != contract_class:
        return {"producers": [], "sources": [], "P_class": info.get("P_class", []), "criticality": info.get("criticality", 99)}
    return {
        "producers": info.get("producers", []),
        "sources": info.get("sources", []),
        "P_class": info.get("P_class", []),
        "criticality": info.get("criticality", 99),
    }


def get_by_source(producer_id: str) -> Optional[Dict]:
    cache = get_cache()
    return cache.get("by_source", {}).get(producer_id)


def get_by_priority(priority_class: str) -> Optional[Dict]:
    cache = get_cache()
    return cache.get("by_priority", {}).get(priority_class)


def get_by_symbol(symbol: str) -> Optional[Dict]:
    cache = get_cache()
    return cache.get("by_symbol", {}).get(symbol)


# --- Internal ---

def _load_all() -> Dict[str, Any]:
    """Load all compiled JSON indexes into a dict. Called once at init or rebuild."""
    if not (COMPILED_DIR / "_compiled.json").exists():
        from modules.data_center.registry_index_builder import rebuild_all
        rebuild_all()

    cache: Dict[str, Any] = {}
    for name in ("by_contract_class", "by_data_key", "by_source", "by_priority", "by_symbol"):
        path = COMPILED_DIR / f"{name}.json"
        if path.exists():
            cache[name] = json.loads(path.read_text(encoding="utf-8"))
        else:
            cache[name] = {}

    meta_path = COMPILED_DIR / "_compiled.json"
    if meta_path.exists():
        cache["_meta"] = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        cache["_meta"] = {}

    return cache
