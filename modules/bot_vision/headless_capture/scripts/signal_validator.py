#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
DC_VISION_ANALYSIS_DIR = REPO_ROOT / "data" / "data_center" / "views" / "vision_analysis"
DC_VISION_BY_SYMBOL_DIR = DC_VISION_ANALYSIS_DIR / "by_symbol"

TF_ORDER = {"15m": 0, "30m": 1, "1h": 2, "4h": 3, "1d": 4, "1w": 5}
TF_WEIGHTS = {"15m": 0.5, "30m": 0.6, "1h": 0.8, "4h": 1.0, "1d": 1.2, "1w": 1.5}

CONFIRMATION_BOOST = 0.15
HIGHER_TF_BOOST = 0.25
CONTRADICTION_PENALTY = 0.20
SAME_VALUE_TOLERANCE_PCT = 0.02


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_analysis_for_symbol(symbol: str) -> list[dict[str, Any]]:
    sym_path = DC_VISION_BY_SYMBOL_DIR / f"{symbol}.json"
    if not sym_path.exists():
        return []
    try:
        data = json.loads(sym_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        return [data]
    except Exception:
        return []


def load_all_timeframes(symbol: str) -> dict[str, list[dict[str, Any]]]:
    analyses = load_analysis_for_symbol(symbol)
    by_tf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for analysis in analyses:
        tf = str(analysis.get("timeframe", "1h"))
        signals = analysis.get("signals", [])
        if isinstance(signals, list):
            by_tf[tf].extend(signals)
    return dict(by_tf)


def _values_close(a: float, b: float, tolerance: float = SAME_VALUE_TOLERANCE_PCT) -> bool:
    if a == 0 and b == 0:
        return True
    if a == 0 or b == 0:
        return abs(a - b) < tolerance
    return abs(a - b) / max(abs(a), abs(b)) < tolerance


def _tf_weight(timeframe: str) -> float:
    return TF_WEIGHTS.get(timeframe, 0.8)


def _tf_order(timeframe: str) -> int:
    return TF_ORDER.get(timeframe, 99)


def _signal_key(sig: dict[str, Any]) -> str:
    t = sig.get("type", "unknown")
    v = sig.get("value", "")
    return f"{t}:{v}"


def cross_validate(
    by_tf: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    if not by_tf:
        return {
            "validated_at": _utc_now_iso(),
            "symbol": "unknown",
            "timeframes_checked": [],
            "raw_signal_count": 0,
            "validated_signal_count": 0,
            "validated_signals": [],
            "deduped_count": 0,
            "confirmed_count": 0,
            "summary": "No data available",
        }

    symbol = "unknown"
    all_signals_flat: list[dict[str, Any]] = []
    tf_order = sorted(by_tf.keys(), key=lambda tf: _tf_order(tf))
    total_raw = 0
    total_deduped = 0
    total_confirmed = 0
    validated: list[dict[str, Any]] = []

    seen: set[str] = set()
    signal_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for tf in tf_order:
        signals = by_tf[tf]
        total_raw += len(signals)
        for sig in signals:
            key = _signal_key(sig)
            val = sig.get("value", "")
            if isinstance(val, (int, float)):
                grouped = False
                for existing_key in list(signal_groups.keys()):
                    existing_sig = signal_groups[existing_key][0]
                    if (sig.get("type") == existing_sig.get("type") and
                            isinstance(existing_sig.get("value"), (int, float)) and
                            _values_close(float(val), float(existing_sig["value"]))):
                        signal_groups[existing_key].append({**sig, "_timeframe": tf, "_tf_weight": _tf_weight(tf)})
                        grouped = True
                        break
                if not grouped:
                    new_key = key
                    signal_groups[new_key] = [{**sig, "_timeframe": tf, "_tf_weight": _tf_weight(tf)}]
            else:
                if key not in seen:
                    seen.add(key)
                    signal_groups[key] = [{**sig, "_timeframe": tf, "_tf_weight": _tf_weight(tf)}]
                else:
                    for existing_key in list(signal_groups.keys()):
                        if existing_key == key:
                            signal_groups[key].append({**sig, "_timeframe": tf, "_tf_weight": _tf_weight(tf)})
                            break

    deduped_count = total_raw - len(signal_groups)

    for group_key, group_signals in signal_groups.items():
        base = dict(group_signals[0])
        base.pop("_timeframe", None)
        base.pop("_tf_weight", None)

        num_occurrences = len(group_signals)
        timeframes_present = sorted(set(s.get("_timeframe", "?") for s in group_signals), key=_tf_order)
        tf_weights_present = [s.get("_tf_weight", 0.8) for s in group_signals]
        max_weight = max(tf_weights_present)
        avg_weight = sum(tf_weights_present) / len(tf_weights_present)

        base_confidence = float(base.get("confidence", 0.50))

        if num_occurrences >= 2:
            confirmed_confidence = base_confidence + CONFIRMATION_BOOST * (num_occurrences - 1) + (max_weight - 0.8)
            base["confidence"] = round(min(confirmed_confidence, 0.98), 3)
            base["cross_validated"] = True
            base["confirmed_by_timeframes"] = timeframes_present
            base["num_confirmations"] = num_occurrences
            total_confirmed += 1
        else:
            base["cross_validated"] = False
            base["confirmed_by_timeframes"] = timeframes_present
            base["num_confirmations"] = 1
            if avg_weight < 1.0:
                base["confidence"] = round(base_confidence * (0.8 + 0.2 * avg_weight), 3)

        base.pop("_timeframe", None)
        base.pop("_tf_weight", None)
        validated.append(base)

    validated_sorted = sorted(validated, key=lambda s: s.get("confidence", 0), reverse=True)

    if symbol == "unknown" and tf_order:
        first_sig = all_signals_flat[0] if all_signals_flat else None
        if first_sig:
            symbol = str(first_sig.get("symbol", "unknown"))

    summary_parts = []
    if total_confirmed > 0:
        summary_parts.append(f"{total_confirmed} confirmed across timeframes")
    if deduped_count > 0:
        summary_parts.append(f"{deduped_count} deduplicated")

    return {
        "validated_at": _utc_now_iso(),
        "symbol": symbol,
        "timeframes_checked": tf_order,
        "raw_signal_count": total_raw,
        "validated_signal_count": len(validated),
        "deduped_count": deduped_count,
        "confirmed_count": total_confirmed,
        "validated_signals": validated_sorted,
        "summary": "; ".join(summary_parts) if summary_parts else "No cross-validation opportunities found",
    }


def validate_latest_or_stdin(symbol: str | None = None) -> int:
    data: dict[str, Any] | None = None

    if symbol:
        by_tf = load_all_timeframes(symbol)
        data = cross_validate(by_tf)
    else:
        try:
            stdin_data = json.loads(sys.stdin.read())
            if isinstance(stdin_data, dict) and "signals" in stdin_data:
                by_tf = {stdin_data.get("timeframe", "1h"): stdin_data.get("signals", [])}
                data = cross_validate(by_tf)
                data["symbol"] = stdin_data.get("symbol", "unknown")
        except (json.JSONDecodeError, EOFError):
            print("ERROR: provide --symbol or pipe a vision_analysis JSON to stdin", file=sys.stderr)
            return 1

    if data is None:
        print("ERROR: no data to validate", file=sys.stderr)
        return 1

    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Cross-validate signals across timeframes and deduplicate")
    ap.add_argument("--symbol", help="Symbol to validate (reads from Data Center by_symbol)")
    ap.add_argument("--stdin", action="store_true", help="Read single vision_analysis from stdin")
    args = ap.parse_args()

    if args.stdin or (not args.symbol and not sys.stdin.isatty()):
        return validate_latest_or_stdin()
    elif args.symbol:
        return validate_latest_or_stdin(symbol=args.symbol)
    else:
        print("ERROR: provide --symbol or pipe data to stdin", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
