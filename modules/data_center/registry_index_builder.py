"""Compiled index builder — generates 5 index files from canonical JSON registries.

Output:
  data/data_center/_registry/compiled/
      by_contract_class.json
      by_data_key.json
      by_source.json
      by_priority.json
      by_symbol.json
      _compiled.json

Rules:
  - atomic write: write temp + fsync + rename
  - adds metadata: version, hash, build_ts
  - score=0 + status=candidate sources are NOT included as selectable
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json
import hashlib
import time
import os
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import registry_validation as rv

INVENTORY_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "pro_desk_data_inventory.json"
CANDIDATES_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "source_candidates.json"
PRODUCERS_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "producers.json"
COMPILED_DIR = REPO_ROOT / "data" / "data_center" / "_registry" / "compiled"


def _atomic_write(path: Path, data: dict) -> None:
    """Write JSON atomically: temp file + fsync + rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    content = json.dumps(data, indent=2, ensure_ascii=False, default=str)
    tmp.write_text(content, encoding="utf-8")
    with open(tmp, "r") as f:
        os.fsync(f.fileno())
    tmp.rename(path)


def _hash_files() -> str:
    """Compute SHA256 of the 3 source registry files."""
    h = hashlib.sha256()
    for p in (INVENTORY_PATH, CANDIDATES_PATH, PRODUCERS_PATH):
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()


def build_by_contract_class(inventory: dict, candidates: dict) -> Dict[str, Any]:
    """contract_class -> data_keys, producers, priority_class, criticality."""
    idx: Dict[str, Any] = {}
    for item in inventory["data_items"]:
        pc = item["priority_class"]
        crit = item["criticality"]
        for f in item["fields"]:
            dk = f["data_key"]
            # Find contract class from source candidates
            cc = _find_contract_class(dk, candidates)
            if cc:
                if cc not in idx:
                    idx[cc] = {"data_keys": [], "producers": set(), "priority_class": set()}
                idx[cc]["data_keys"].append(dk)
                idx[cc]["priority_class"].add(pc)
                if "criticality" not in idx[cc] or crit < idx[cc]["criticality"]:
                    idx[cc]["criticality"] = crit
                for src in _get_existing_sources(pc, candidates):
                    idx[cc]["producers"].add(src["source_id"])

    for cc in idx:
        idx[cc]["producers"] = sorted(idx[cc]["producers"])
        idx[cc]["priority_class"] = sorted(idx[cc]["priority_class"])
        idx[cc]["data_keys"] = sorted(set(idx[cc]["data_keys"]))
    return idx


def build_by_data_key(inventory: dict, candidates: dict) -> Dict[str, Any]:
    """data_key -> contract_class, producers, sources, P_class, criticality, unit, description."""
    idx: Dict[str, Any] = {}
    for item in inventory["data_items"]:
        pc = item["priority_class"]
        crit = item["criticality"]
        for f in item["fields"]:
            dk = f["data_key"]
            cc = _find_contract_class(dk, candidates)
            idx[dk] = {
                "contract_class": cc,
                "producers": _get_existing_producer_ids(pc, candidates),
                "sources": _get_candidate_source_ids(pc, candidates),
                "P_class": [pc],
                "criticality": crit,
                "unit": f.get("unit", ""),
                "description": f["description"],
            }
    return idx


def build_by_source(producers: dict, inventory: dict, candidates: dict) -> Dict[str, Any]:
    """producer_id -> contract_class, data_keys, family, output_path, score_components, last_write."""
    idx: Dict[str, Any] = {}
    for p in producers.get("producers", []):
        pid = p["producer_id"]
        cc = p.get("contract_class")
        idx[pid] = {
            "contract_class": cc,
            "data_keys": p.get("collectable_metrics", []),
            "family": p.get("family"),
            "output_path": p.get("output_path_root"),
            "score_components": {
                "source_reliability": 0.5 if p.get("last_write") is None else 0.8,
                "freshness": 0.0,
                "completeness": 0.0,
            },
            "last_write": p.get("last_write"),
        }
    return idx


def build_by_priority(inventory: dict) -> Dict[str, Any]:
    """P0..P21 -> label, criticality, data_keys, covered, missing, coverage_pct."""
    idx: Dict[str, Any] = {}
    for item in inventory["data_items"]:
        pc = item["priority_class"]
        idx[pc] = {
            "label": item["label"],
            "criticality": item["criticality"],
            "data_keys": [f["data_key"] for f in item["fields"]],
            "covered": [],
            "missing": [f["data_key"] for f in item["fields"]],
            "coverage_pct": 0,
        }
    return idx


def build_by_symbol(producers: dict) -> Dict[str, Any]:
    """symbol -> available data_keys with per-producer status."""
    idx: Dict[str, Any] = {}
    for p in producers.get("producers", []):
        pid = p["producer_id"]
        last_write = p.get("last_write")
        for dk in p.get("collectable_metrics", []):
            # Infer symbol from producer (simplified: global, not per-symbol yet)
            symbol = "BTCUSDT"
            if symbol not in idx:
                idx[symbol] = {"available_data_keys": {}}
            if dk not in idx[symbol]["available_data_keys"]:
                idx[symbol]["available_data_keys"][dk] = {"producers": {}, "best_value": None, "stale": True}
            idx[symbol]["available_data_keys"][dk]["producers"][pid] = {
                "last_write": last_write,
                "value": None,
            }
    return idx


def _find_contract_class(data_key: str, candidates: dict) -> str | None:
    # First check source_candidates existing sources coverage
    for pc_class, pc_data in candidates.get("source_candidates", {}).items():
        for src in pc_data.get("sources", {}).get("existing", []):
            if data_key in src.get("coverage", []):
                return src.get("contract_class")
    # Fallback: try variant names (inventory uses canonical names,
    # source_candidates uses producer-specific names)
    variants = {
        "open_interest": ["futures_open_interest", "open_interest_per_venue"],
        "funding_rate": ["funding_rate_crypto", "funding_rate"],
        "volume_24h": ["futures_volume"],
        "liquidations_long": ["liquidation_data", "crypto_liquidation_data"],
        "liquidations_short": ["liquidation_data", "crypto_liquidation_data"],
        "long_short_ratio": ["long_short_ratio"],
        "last_price": ["last_price", "spot_price_per_exchange"],
        "open": ["open_price_24h"],
        "high": ["high_price_24h"],
        "low": ["low_price_24h"],
        "close": ["close"],
    }
    for variant in variants.get(data_key, []):
        for pc_class, pc_data in candidates.get("source_candidates", {}).items():
            for src in pc_data.get("sources", {}).get("existing", []):
                if variant in src.get("coverage", []):
                    return src.get("contract_class")
    return None


def _get_existing_sources(pc_class: str, candidates: dict) -> list:
    pc_data = candidates.get("source_candidates", {}).get(pc_class, {})
    sources = pc_data.get("sources", {}).get("existing", [])
    return [s for s in sources if rv.is_source_selectable(s)]


def _get_existing_producer_ids(pc_class: str, candidates: dict) -> list:
    return sorted(set(s["source_id"] for s in _get_existing_sources(pc_class, candidates)))


def _get_candidate_source_ids(pc_class: str, candidates: dict) -> list:
    pc_data = candidates.get("source_candidates", {}).get(pc_class, {})
    all_sources = pc_data.get("sources", {}).get("candidates", [])
    return sorted(set(s["source_id"] for s in all_sources))


# --- Public API ---

def rebuild_all() -> str:
    """Rebuild all compiled indexes. Returns the version hash."""
    inventory = rv.load_inventory()
    candidates = rv.load_source_candidates()
    producers = rv.load_producers()

    version = _hash_files()
    build_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    indexes = {
        "by_contract_class": build_by_contract_class(inventory, candidates),
        "by_data_key": build_by_data_key(inventory, candidates),
        "by_source": build_by_source(producers, inventory, candidates),
        "by_priority": build_by_priority(inventory),
        "by_symbol": build_by_symbol(producers),
    }

    for name, idx in indexes.items():
        _atomic_write(COMPILED_DIR / f"{name}.json", idx)

    meta = {
        "version": version,
        "build_ts": build_ts,
        "source_hash": version,
        "total_contracts": len(indexes["by_contract_class"]),
        "total_data_keys": len(indexes["by_data_key"]),
        "total_producers": len(indexes["by_source"]),
    }
    _atomic_write(COMPILED_DIR / "_compiled.json", meta)

    return version


if __name__ == "__main__":
    v = rebuild_all()
    print(f"Compiled indexes rebuilt — version {v[:12]}")
    for f in sorted(COMPILED_DIR.glob("*.json")):
        print(f"  {f.name} ({f.stat().st_size} bytes)")
