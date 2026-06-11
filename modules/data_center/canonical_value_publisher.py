"""
canonical_value_publisher — resolve best source, extract real value, publish to DC views.

Wires together:
    source_selector.resolve() → producer_payload_reader.extract_value() → write DC views

Usage:
    from modules.data_center.canonical_value_publisher import resolve_and_publish

    result = resolve_and_publish("vision_context.coinglass.v1", "BTCUSDT", "open_interest")
    # Writes:
    #   data/data_center/views/vision_context.coinglass.v1/by_symbol/BTCUSDT.json
    #   data/data_center/views/vision_context.coinglass.v1/latest.json
    #   data/data_center/resolver/vision_context.coinglass.v1/BTCUSDT/open_interest.json
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_RESOLVER_DIR = _PROJECT_ROOT / "data" / "data_center" / "resolver"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)

# Imported at module level so tests can patch them
import modules.data_center.source_selector as _source_selector  # noqa: E402
import modules.data_center.producer_payload_reader as _payload_reader  # noqa: E402
import modules.data_center.runtime_registry as _runtime_registry  # noqa: E402


def resolve_and_publish(
    contract_class: str,
    symbol: str,
    data_key: str,
    mode: str = "best_candidate",
) -> dict[str, Any]:
    """Resolve best source, extract real value, publish to data_center views.

    Args:
        contract_class: e.g. "vision_context.coinglass.v1"
        symbol: e.g. "BTCUSDT"
        data_key: e.g. "open_interest"
        mode: selection mode for source_selector

    Returns:
        dict with resolver_decision + canonical_value + actual extracted value
    """
    # Step 1: resolve best source
    result = _source_selector.resolve(contract_class, symbol, data_key, mode=mode)

    # Step 2: read actual payload from winning producer
    winner_id = result["canonical_value"]["winning_producer_id"]
    extracted = None
    payload_ok = True
    payload_errors: list[str] = []

    if winner_id:
        payload = _payload_reader.read_latest_payload(winner_id, contract_class)
        if payload:
            payload_ok, payload_errors = _payload_reader.validate_payload_shape(payload, contract_class)
            if payload_ok:
                extracted = _payload_reader.extract_value(payload, contract_class, symbol, data_key)

    # Step 3: populate canonical_value with real value
    cv = result["canonical_value"]
    cv["canonical_value"] = extracted
    cv["extraction_method"] = "producer_payload_reader"
    cv["payload_ok"] = payload_ok
    if payload_errors:
        cv["payload_warnings"] = payload_errors

    if extracted is None:
        cv["stale"] = True
        if not payload_ok:
            cv["stale_reason"] = "payload_invalid"
        elif winner_id:
            cv["stale_reason"] = "value_not_found_in_payload"
        else:
            cv["stale_reason"] = "no_winning_producer"

    # Step 4: publish resolver_decision
    rd = result["resolver_decision"]
    rd_path = _RESOLVER_DIR / contract_class / symbol / f"{data_key}.json"
    _atomic_write(rd_path, rd)

    # Step 5: publish canonical_value view (by_symbol)
    cv_path = _VIEWS_DIR / contract_class / "by_symbol" / f"{symbol}.json"
    existing = {}
    if cv_path.exists():
        try:
            existing = json.loads(cv_path.read_text(encoding="utf-8"))
        except Exception:
            existing = {}
    if not isinstance(existing, dict):
        existing = {}

    # Merge: keep existing data_keys, update this one
    values = existing.get("values", {})
    values[data_key] = {
        "value": extracted,
        "resolved_at": cv["resolved_at"],
        "resolver_decision_ref": cv["resolver_decision_ref"],
        "winning_producer_id": cv["winning_producer_id"],
        "winning_score": cv["winning_score"],
        "stale": cv.get("stale", False),
    }
    existing.update({
        "input_class": contract_class,
        "symbol": symbol,
        "produced_at": datetime.now(timezone.utc).isoformat(),
        "values": values,
    })
    _atomic_write(cv_path, existing)

    # Step 6: update latest.json view
    latest_path = _VIEWS_DIR / contract_class / "latest.json"
    latest = {}
    if latest_path.exists():
        try:
            latest = json.loads(latest_path.read_text(encoding="utf-8"))
        except Exception:
            latest = {}
    if not isinstance(latest, dict):
        latest = {}

    latest.update({
        "input_class": contract_class,
        "last_resolved_symbol": symbol,
        "last_resolved_key": data_key,
        "last_resolved_at": cv["resolved_at"],
        "last_resolver_decision_ref": cv["resolver_decision_ref"],
        "last_value": extracted,
        "all_symbols": list(_list_resolved_symbols(contract_class)),
    })
    _atomic_write(latest_path, latest)

    # Step 7: update runtime registry
    _runtime_registry.update_producer_last_write(
        producer_id=f"canonical_publisher_{contract_class}",
        contract_class=contract_class,
        output_path=str(cv_path),
        status="ok" if not cv.get("stale") else "stale",
        evidence={"symbol": symbol, "data_key": data_key, "value": str(extracted)[:200]},
    )

    return result


def _list_resolved_symbols(contract_class: str) -> set[str]:
    """List all symbols that have been resolved for a contract_class."""
    symbols_dir = _VIEWS_DIR / contract_class / "by_symbol"
    if not symbols_dir.exists():
        return set()
    return {f.stem for f in symbols_dir.glob("*.json") if f.is_file()}


def publish_batch(
    contract_class: str,
    symbol_data_keys: list[tuple[str, str]],
    mode: str = "best_candidate",
) -> list[dict[str, Any]]:
    """Resolve and publish multiple (symbol, data_key) pairs.

    Args:
        contract_class: e.g. "vision_context.coinglass.v1"
        symbol_data_keys: list of (symbol, data_key) tuples
        mode: selection mode

    Returns:
        list of result dicts
    """
    results = []
    for symbol, data_key in symbol_data_keys:
        try:
            result = resolve_and_publish(contract_class, symbol, data_key, mode=mode)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "symbol": symbol, "data_key": data_key})
    return results
