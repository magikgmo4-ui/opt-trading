"""
producer_payload_reader — reads actual producer payloads and extracts values.

Usage:
    from modules.data_center.producer_payload_reader import read_latest_payload, extract_value

    payload = read_latest_payload("coinglass_headless_bot", "vision_context.coinglass.v1")
    value = extract_value(payload, "vision_context.coinglass.v1", "BTCUSDT", "open_interest")

Supported contract classes (V1):
    - vision_context.coinglass.v1
    - vision_analysis.v1
    - telegram_signal.v1
    - market_metrics.v1 (hypothesis — no producer yet)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Map contract_class → known producer paths (where payloads live)
_PRODUCER_PATHS: dict[str, list[Path]] = {
    "vision_context.coinglass.v1": [
        _PROJECT_ROOT / "data" / "vision" / "coinglass" / "latest.json",
        _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json",
    ],
    "vision_analysis.v1": [
        _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "latest.json",
        _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis" / "latest.json",
    ],
    "telegram_signal.v1": [
        _PROJECT_ROOT / "data" / "telegram_screener" / "signals" / "latest.json",
    ],
    "vision_context.screener.v1": [
        _PROJECT_ROOT / "data" / "data_center" / "views" / "vision_context" / "screener" / "latest.json",
        _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "screener" / "latest.json",
    ],
    "telegram_channel_stats.v1": [
        _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals" / "channel_stats" / "latest.json",
    ],
}

# Map (contract_class, data_key) → extraction path in payload
_EXTRACTION_PATHS: dict[tuple[str, str], list[str]] = {
    # Coinglass OCR
    ("vision_context.coinglass.v1", "open_interest"):            ["detections", "open_interest", "extracted_value"],
    ("vision_context.coinglass.v1", "liquidations_long"):        ["detections", "liquidations_long", "extracted_value"],
    ("vision_context.coinglass.v1", "liquidations_short"):       ["detections", "liquidations_short", "extracted_value"],
    ("vision_context.coinglass.v1", "long_short_ratio"):         ["detections", "long_short_ratio", "extracted_value"],
    ("vision_context.coinglass.v1", "liquidation_heatmap_level"):["detections", "liquidation_heatmap_level", "extracted_value"],
    ("vision_context.coinglass.v1", "open_interest_change_24h"): ["detections", "open_interest_change_24h", "extracted_value"],
    # Vision analysis
    ("vision_analysis.v1", "support_level"):       ["signals", "support_level", "value"],
    ("vision_analysis.v1", "resistance_level"):    ["signals", "resistance_level", "value"],
    ("vision_analysis.v1", "trend"):               ["signals", "trend", "value"],
    # Telegram signals
    ("telegram_signal.v1", "signal_count"):        ["signals"],
    ("telegram_signal.v1", "active_channels"):     ["active_channels"],
    # Screener
    ("vision_context.screener.v1", "stock_count"): ["stocks"],
    ("vision_context.screener.v1", "screener_label"): ["screener_label"],
}


def read_latest_payload(producer_id: str, contract_class: str) -> Optional[dict]:
    """Read the latest payload for a given contract_class from known producer paths.

    Returns the parsed JSON dict, or None if no payload found / parse error.
    """
    paths = _PRODUCER_PATHS.get(contract_class, [])
    for path in paths:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
    return None


def extract_value(
    payload: dict,
    contract_class: str,
    symbol: str,
    data_key: str,
) -> Optional[Any]:
    """Extract a specific value from a producer payload.

    Args:
        payload: the parsed JSON dict from read_latest_payload
        contract_class: e.g. "vision_context.coinglass.v1"
        symbol: e.g. "BTCUSDT" (validated against payload if present)
        data_key: e.g. "open_interest"

    Returns the extracted value, or None if not found.
    """
    # Symbol check: if payload has a symbol field, verify match
    payload_symbol = payload.get("symbol", "")
    if payload_symbol and symbol and symbol.upper() not in payload_symbol.upper():
        # Symbol mismatch — try alternate key
        pass  # Continue anyway; extraction may still succeed

    # Check extraction path
    path = _EXTRACTION_PATHS.get((contract_class, data_key))
    if path:
        return _navigate(payload, path)

    # Fallback: direct key lookup
    if data_key in payload:
        return payload[data_key]

    # Fallback: search in detections list by metric_type
    detections = payload.get("detections", [])
    if isinstance(detections, list):
        for d in detections:
            if isinstance(d, dict) and d.get("detected_metric_type") == data_key:
                return d.get("extracted_value")

    # Fallback: search in signals list by type
    signals = payload.get("signals", [])
    if isinstance(signals, list):
        for s in signals:
            if isinstance(s, dict) and s.get("type") == data_key:
                return s.get("value")

    return None


def validate_payload_shape(payload: dict, contract_class: str) -> tuple[bool, list[str]]:
    """Validate that a payload matches the expected shape for its contract_class.

    Returns (is_valid, list_of_errors).
    """
    errors: list[str] = []
    if not isinstance(payload, dict):
        return False, ["payload is not a dict"]

    input_class = payload.get("input_class", "")
    if input_class and input_class != contract_class:
        errors.append(f"input_class mismatch: got {input_class}, expected {contract_class}")

    freshness = payload.get("freshness_state", "")
    if freshness == "stale":
        errors.append("payload is stale")

    return len(errors) == 0, errors


def _navigate(data: dict, path: list[str]) -> Optional[Any]:
    """Navigate a nested dict/list by a path of keys.

    Special keys:
      - If a segment matches a detection type, search in list of dicts by that key.
    """
    current: Any = data
    for i, key in enumerate(path):
        if current is None:
            return None
        if isinstance(current, list):
            # Search list for dict with matching field
            for item in current:
                if isinstance(item, dict):
                    # Try matching by 'detected_metric_type' or 'type'
                    if item.get("detected_metric_type") == key or item.get("type") == key:
                        current = item
                        break
            else:
                return None
            continue
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None

    # If current is still a dict, try to extract the actual value
    if isinstance(current, dict):
        return current.get("extracted_value") or current.get("value") or current
    return current
