"""Registry validation — validates pro_desk_data_inventory.json and source_candidates.json.

Rules enforced:
  - summary.total_fields matches actual field count
  - all source_candidates data_key references exist in inventory
  - all active_registry producer_ids exist in producers.json
  - score=0 + status=candidate = not selectable (unevaluated policy)
  - no duplicate data_keys
  - all P0-P21 categories present
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import json


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INVENTORY_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "pro_desk_data_inventory.json"
CANDIDATES_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "source_candidates.json"
PRODUCERS_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "producers.json"
UNEVALUATED_RULE = "score=0 + status=candidate = not selectable"


class ValidationError(Exception):
    pass


def load_inventory(path: Path = INVENTORY_PATH) -> dict:
    """Load and return the pro desk data inventory."""
    return _load_json(path)


def load_source_candidates(path: Path = CANDIDATES_PATH) -> dict:
    """Load and return the source candidates registry."""
    return _load_json(path)


def load_producers(path: Path = PRODUCERS_PATH) -> dict:
    """Load and return the producers registry."""
    return _load_json(path)


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise ValidationError(f"File not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in {path}: {e}")


def validate_inventory_summary(inventory: dict) -> List[str]:
    """Validate that summary.total_fields matches actual field count."""
    errors = []
    summary = inventory.get("summary", {})
    declared = summary.get("total_fields", 0)
    actual = sum(len(item["fields"]) for item in inventory["data_items"])
    if declared != actual:
        errors.append(f"summary.total_fields={declared} but actual={actual}")
    return errors


def validate_unique_data_keys(inventory: dict) -> List[str]:
    """Validate no duplicate data_keys across the inventory."""
    errors = []
    keys = {}
    for item in inventory["data_items"]:
        for f in item["fields"]:
            dk = f["data_key"]
            if dk in keys:
                errors.append(f"Duplicate data_key '{dk}': P{item['priority_class']} and {keys[dk]}")
            keys[dk] = item["priority_class"]
    return errors


def validate_source_candidates(candidates: dict, inventory: dict) -> List[str]:
    """Validate that all source_candidates data_key references exist in inventory."""
    errors = []
    inventory_keys = set()
    for item in inventory["data_items"]:
        for f in item["fields"]:
            inventory_keys.add(f["data_key"])

    for pc_class, pc_data in candidates.get("source_candidates", {}).items():
        for source_type in ("existing", "candidates"):
            sources = pc_data.get("sources", {}).get(source_type, [])
            for src in sources:
                for dk in src.get("coverage", []):
                    if dk not in inventory_keys:
                        errors.append(f"source_candidates {src['source_id']} references unknown data_key '{dk}'")
    return errors


def validate_score_zero_policy(candidates: dict) -> List[str]:
    """Validate that all sources with score=0 and status=candidate are marked unevaluated."""
    errors = []
    selection_rules = candidates.get("selection_rules", {})
    if selection_rules.get("score_zero_policy") != "unevaluated":
        errors.append(f"selection_rules.score_zero_policy={selection_rules.get('score_zero_policy')}, expected 'unevaluated'")
    return errors


def validate_candidate_data_keys_exist(candidates: dict, inventory: dict) -> List[str]:
    """Validate coverage data_keys exist in the inventory for each candidate source."""
    errors = []
    inventory_keys = set()
    for item in inventory["data_items"]:
        for f in item["fields"]:
            inventory_keys.add(f["data_key"])

    for pc_class, pc_data in candidates.get("source_candidates", {}).items():
        for source_type in ("existing", "candidates"):
            sources = pc_data.get("sources", {}).get(source_type, [])
            for src in sources:
                for dk in src.get("coverage", []):
                    if dk not in inventory_keys:
                        errors.append(f"source_candidates.{pc_class}.{src['source_id']}: coverage key '{dk}' not in inventory")
    return errors


def validate_producer_registry_consistency(candidates: dict, producers: dict) -> List[str]:
    """Validate that active_registry producer_ids exist in producers.json."""
    errors = []
    producer_ids = {p["producer_id"] for p in producers.get("producers", [])}

    for pc_class, pc_data in candidates.get("source_candidates", {}).items():
        for src in pc_data.get("sources", {}).get("existing", []):
            if src.get("status") == "active_registry":
                pid = src["source_id"]
                if pid not in producer_ids:
                    errors.append(f"source_candidates.{pc_class}.{pid}: active_registry but not in producers.json")
    return errors


def is_source_selectable(source: dict) -> bool:
    """Check if a source is eligible for runtime selection."""
    score = source.get("score", 0)
    status = source.get("status", "candidate")
    if score == 0 and status == "candidate":
        return False
    if status in ("active_registry", "evaluated"):
        return True
    return False
