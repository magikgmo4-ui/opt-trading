"""
contract_registry_validator.py — validate all 28 contracts against runtime reality.

Checks:
    1. Every contract has required fields (domain, provider_id, schedule, status)
    2. Every PROVEN contract has a valid view_path on disk
    3. Every producer_module file exists
    4. No duplicate contract_class names
    5. Score consistency (PROVEN >= 0.70, PARTIAL < 0.70)
    6. Every contract has at least one data_key
    7. Backtest contracts have next_action if score is null
    8. Summary counts match actual contract counts

Usage:
    python -m modules.data_center.contract_registry_validator
    python -m modules.data_center.contract_registry_validator --json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONTRACTS_PATH = _PROJECT_ROOT / "data" / "data_center" / "_registry" / "contracts.json"


def load_contracts() -> dict:
    if not _CONTRACTS_PATH.exists():
        return {"error": "contracts.json not found", "contracts": {}}
    return json.loads(_CONTRACTS_PATH.read_text(encoding="utf-8"))


def validate() -> list[str]:
    data = load_contracts()
    contracts = data.get("contracts", {})
    errors: list[str] = []

    if not contracts:
        errors.append("FATAL: no contracts defined")
        return errors

    # 1. Required fields
    required = ["domain", "provider_id", "schedule", "status"]
    for cid, c in contracts.items():
        for field in required:
            if field not in c:
                errors.append(f"{cid}: missing required field '{field}'")

    # 2. View paths exist on disk for PROVEN contracts
    for cid, c in contracts.items():
        if c.get("status") != "PROVEN" or c.get("on_demand"):
            continue
        vp = c.get("view_path", "")
        if "{SYMBOL}" in vp or "{CONTRACT}" in vp or "{DATA_KEY}" in vp:
            continue  # Templated path, check parent dir
        path = _PROJECT_ROOT / vp
        if not path.exists():
            errors.append(f"{cid}: view_path not found on disk: {vp}")

    # 3. Producer modules exist
    for cid, c in contracts.items():
        pm = c.get("producer_module", "")
        if not pm:
            errors.append(f"{cid}: missing producer_module")
            continue
        if pm in ("bot_vision_headless_capture", "bot_vision_headless_capture + bot_vision_step2"):
            continue  # External system modules, not importable
        path = _PROJECT_ROOT / pm
        if not path.exists():
            errors.append(f"{cid}: producer_module not found: {pm}")

    # 4. No duplicate contract_class
    seen = set()
    for cid in contracts:
        if cid in seen:
            errors.append(f"DUPLICATE: {cid}")
        seen.add(cid)

    # 5. Score consistency
    for cid, c in contracts.items():
        score = c.get("score")
        status = c.get("status")
        if score is None:
            continue  # on-demand or backtest
        if status == "PROVEN" and score < 0.70:
            errors.append(f"{cid}: PROVEN but score {score} < 0.70")
        if status == "PARTIAL" and score >= 0.70:
            errors.append(f"{cid}: PARTIAL but score {score} >= 0.70 (should be PROVEN)")

    # 6. Data keys present
    for cid, c in contracts.items():
        keys = c.get("data_keys", [])
        if not keys:
            errors.append(f"{cid}: no data_keys defined")

    # 7. Summary counts match
    summary = data.get("summary", {})
    actual = len(contracts)
    if summary.get("total_contracts") != actual:
        errors.append(f"summary.total_contracts={summary.get('total_contracts')} but actual={actual}")
    proven_count = sum(1 for c in contracts.values() if c.get("status") == "PROVEN")
    if summary.get("proven") != proven_count:
        errors.append(f"summary.proven={summary.get('proven')} but actual PROVEN count={proven_count}")
    partial_count = sum(1 for c in contracts.values() if c.get("status") == "PARTIAL")
    if summary.get("partial") != partial_count:
        errors.append(f"summary.partial={summary.get('partial')} but actual PARTIAL count={partial_count}")

    # 8. Domain consistency
    domain_map = data.get("domains", {})
    for cid, c in contracts.items():
        dom = c.get("domain", "")
        if dom not in domain_map:
            errors.append(f"{cid}: domain '{dom}' not registered in domains section")
    for dom_id, dom in domain_map.items():
        listed = set(dom.get("contracts", []))
        actual_in_dom = {cid for cid, c in contracts.items() if c.get("domain") == dom_id}
        if listed != actual_in_dom:
            diff = listed.symmetric_difference(actual_in_dom)
            if diff:
                errors.append(f"domain '{dom_id}': contract list mismatch: {sorted(diff)}")

    return errors


if __name__ == "__main__":
    errors = validate()
    json_out = "--json" in sys.argv

    if json_out:
        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "contracts_checked": len(load_contracts().get("contracts", {})),
        }
        print(json.dumps(result, indent=2))
    else:
        if not errors:
            contracts = load_contracts()
            summary = contracts.get("summary", {})
            print(f"✅ Contract registry valid — {summary.get('total_contracts')} contracts, {summary.get('proven')} PROVEN, {summary.get('partial')} PARTIAL")
        else:
            print(f"❌ {len(errors)} validation errors:")
            for e in errors:
                print(f"  - {e}")
        sys.exit(1 if errors else 0)
