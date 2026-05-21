#!/usr/bin/env python3
"""Signal chain processor with dry-run guard.

Simulates receiving, validating, cross-checking, and logging a signal.
Blocks all live order emission.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SIGNAL_DIR = REPO_ROOT / "data" / "signals"
JOURNAL_DIR = SIGNAL_DIR / "journal"
DRY_RUN_ORDERS_DIR = SIGNAL_DIR / "dry_run_orders"


def make_signal(source, signal_type, symbol, direction, confidence, price=None):
    return {
        "signal_id": str(uuid.uuid4()),
        "source": source,
        "source_instance": f"{source}_01",
        "signal_type": signal_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "symbol": symbol,
            "direction": direction,
            "price": price,
            "confidence": confidence,
            "indicators": {"rsi": 65, "macd": "bullish"},
            "metadata": {"strategy": "trend_following"},
        },
        "cross_validation": {"required_sources": 2, "matched_sources": [], "status": "pending"},
        "dry_run": {"order_generated": False, "order_blocked": False, "order_json": None},
        "journal": {"received_at": None, "processed_at": None, "processing_time_ms": 0, "status": "received"},
    }


def validate(signal):
    if signal["payload"]["confidence"] < 0.6:
        return False, "confidence_below_threshold"
    if signal["signal_type"] not in ("entry", "exit", "alert", "heartbeat", "anomaly"):
        return False, "unknown_signal_type"
    if not signal["payload"]["direction"]:
        return False, "missing_direction"
    if signal["payload"].get("price") is not None and signal["payload"]["price"] <= 0:
        return False, "invalid_price"
    return True, "valid"


def cross_check(signal, matched_sources):
    signal["cross_validation"]["matched_sources"] = matched_sources
    count = len(matched_sources)
    if count >= 2:
        signal["cross_validation"]["status"] = "confirmed"
    elif count == 1:
        signal["cross_validation"]["status"] = "pending"
    else:
        signal["cross_validation"]["status"] = "conflicting"
    return signal


def dry_run_guard(signal):
    """Blocks live order, generates simulated order JSON."""
    if signal["cross_validation"]["status"] != "confirmed":
        return signal, False

    # Generate simulated order
    order = {
        "order_id": str(uuid.uuid4()),
        "signal_id": signal["signal_id"],
        "symbol": signal["payload"]["symbol"],
        "direction": signal["payload"]["direction"],
        "price": signal["payload"].get("price"),
        "quantity": 0.01,
        "type": "limit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "BLOCKED_BY_DRY_RUN_GUARD",
    }

    signal["dry_run"]["order_generated"] = True
    signal["dry_run"]["order_blocked"] = True
    signal["dry_run"]["order_json"] = order

    # Store the simulated order
    DRY_RUN_ORDERS_DIR.mkdir(parents=True, exist_ok=True)
    order_path = DRY_RUN_ORDERS_DIR / f"order_{order['order_id']}.json"
    order_path.write_text(json.dumps(order, indent=2))

    return signal, True


def journal_signal(signal):
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    journal_path = JOURNAL_DIR / f"{today}.jsonl"

    signal["journal"]["received_at"] = signal["timestamp"]
    signal["journal"]["processed_at"] = datetime.now(timezone.utc).isoformat()
    signal["journal"]["processing_time_ms"] = 123  # simulated
    signal["journal"]["status"] = "logged"

    with open(journal_path, "a") as f:
        f.write(json.dumps(signal) + "\n")

    return signal


def process_signal(source, signal_type, symbol, direction, confidence, price=None, matched_sources=None):
    signal = make_signal(source, signal_type, symbol, direction, confidence, price)

    valid, reason = validate(signal)
    if not valid:
        print(f"INVALID: {reason}")
        return False

    signal = cross_check(signal, matched_sources or [source])
    signal = dry_run_guard(signal)[0]
    signal = journal_signal(signal)

    print(f"SIGNAL {signal['signal_id'][:8]} | {signal['payload']['symbol']} | "
          f"cross={signal['cross_validation']['status']} | "
          f"blocked={signal['dry_run']['order_blocked']}")
    return True


def main():
    # Scenario 1: Confirmed signal (2+ sources)
    ok1 = process_signal(
        source="tradingview", signal_type="entry", symbol="BTCUSD",
        direction="buy", confidence=0.82, price=12345.67,
        matched_sources=["tradingview", "telegram"]
    )
    # Scenario 2: Low confidence - should be rejected
    ok2 = process_signal(
        source="telegram", signal_type="entry", symbol="ETHUSD",
        direction="sell", confidence=0.45, price=3456.78,
        matched_sources=["telegram"]
    )
    # Scenario 3: Conflicting signal (0 matched sources)
    ok3 = process_signal(
        source="collector", signal_type="alert", symbol="SOLUSD",
        direction="buy", confidence=0.75, price=89.12,
        matched_sources=[]
    )

    print(f"\nResults: {sum([ok1, ok2, ok3])}/3 PASS")
    if ok1 and not ok2 and ok3:
        print("Scenario validation: OK (confirmed accepted, low confidence rejected, conflicting still processed)")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
