#!/usr/bin/env python3
"""P6 Signal dry-run — signal → validation → journal → backtest, sans ordre live.

Usage:
  # Default: dry-run with synthetic signal
  python3 scripts/ai/workers/signal_dry_run_worker.py

  # With a specific signal file
  python3 scripts/ai/workers/signal_dry_run_worker.py --signal <path>

  # Skip backtest
  python3 scripts/ai/workers/signal_dry_run_worker.py --no-backtest
"""

import argparse
import json
import random
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "admin_trading_contract_smoke"
LEDGER_PATH = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"
OUTPUT_DIR = REPO_ROOT / "reports" / "ai" / "workers"

SYNTHETIC_SIGNAL = {
    "engine": "coinm",
    "signal": "SELL",
    "symbol": "BTCUSDT.P",
    "tf": "1h",
    "price": 67500.0,
    "tp": 65000.0,
    "sl": 69000.0,
    "reason": "P6_dry_run_synthetic_test",
    "_ts": datetime.now(timezone.utc).isoformat(),
}

MOCK_BACKTEST = {
    "direction": None,
    "entry_price": None,
    "exit_price": None,
    "pnl_pct": None,
    "pnl_usd": None,
    "bars_held": None,
    "outcome": None,
    "max_favorable_excursion": None,
    "max_adverse_excursion": None,
}


def log_ledger(event_type, actor, surface, action, status, payload=None):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event_id": uuid.uuid4().hex[:12],
        "event_type": event_type,
        "actor_id": actor,
        "surface_id": surface,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "payload": payload or {},
    }
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def normalize_v0_to_v1(raw):
    """Convert V0 webhook signal to V1 signal_event."""
    ts = raw.get("_ts", datetime.now(timezone.utc).isoformat())
    return {
        "event_type": "signal_received",
        "version": "1.0",
        "timestamp": ts,
        "source": "webhook",
        "engine": raw.get("engine", "unknown"),
        "symbol": raw.get("symbol", "UNKNOWN"),
        "timeframe": raw.get("tf", raw.get("timeframe", "1h")),
        "direction": raw.get("signal", "").upper(),
        "price": float(raw.get("price", 0)),
        "tp": float(raw.get("tp", 0)) if raw.get("tp") else None,
        "sl": float(raw.get("sl", 0)) if raw.get("sl") else None,
        "reason": raw.get("reason", ""),
        "status": "accepted",
        "payload_hash": uuid.uuid4().hex[:16],
    }


def validate_v1(sig):
    """Validate signal_event v1, return (is_valid, errors)."""
    errors = []
    required = ["engine", "symbol", "direction", "timeframe", "timestamp"]
    for field in required:
        if not sig.get(field):
            errors.append(f"missing required field: {field}")
    if sig.get("direction") not in ("BUY", "SELL"):
        errors.append(f"invalid direction '{sig.get('direction')}': must be BUY or SELL")
    return len(errors) == 0, errors


def run_backtest(sig):
    """Simulated backtest — never places a live order."""
    direction = sig.get("direction", "BUY")
    entry = sig.get("price", 100.0)
    direction_mult = 1 if direction == "BUY" else -1
    move_pct = random.uniform(-3.0, 5.0)
    exit_price = round(entry * (1 + move_pct / 100 * direction_mult), 2)
    pnl_pct = round((exit_price - entry) / entry * 100 * direction_mult, 2)
    pnl_usd = round(pnl_pct * 10, 2)
    bars = random.randint(1, 24)
    mfe = round(random.uniform(0.5, max(2.0, pnl_pct + 1)), 2) if pnl_pct > 0 else round(random.uniform(0.1, 1.5), 2)
    mae = round(random.uniform(0.5, abs(pnl_pct) + 1), 2) if pnl_pct < 0 else round(random.uniform(0.1, 1.0), 2)

    return {
        "direction": direction,
        "entry_price": entry,
        "exit_price": exit_price,
        "pnl_pct": pnl_pct,
        "pnl_usd": pnl_usd,
        "bars_held": bars,
        "outcome": "WIN" if pnl_pct > 0 else "LOSS",
        "max_favorable_excursion": mfe,
        "max_adverse_excursion": mae,
        "dry_run": True,
        "live_order_blocked": True,
    }


def run_signal_dry_run(signal_path=None, run_backtest_flag=True):
    cycle_id = uuid.uuid4().hex[:8]
    start = time.time()
    print(f"[{cycle_id}] Signal dry-run worker")

    # Step 1: Load signal
    if signal_path:
        p = Path(signal_path)
        if not p.exists():
            print(f"  ERROR: signal file not found: {signal_path}")
            return False
        raw = json.loads(p.read_text())
        source = str(p)
    else:
        raw = SYNTHETIC_SIGNAL.copy()
        raw["_ts"] = datetime.now(timezone.utc).isoformat()
        source = "synthetic"

    print(f"  Signal: {raw.get('engine','?')} {raw.get('signal','?')} {raw.get('symbol','?')}")
    log_ledger("signal_dry_run", "signal_dry_run_worker", raw.get("symbol", "unknown"),
               "LOAD_SIGNAL", "PASS", {"source": source, "engine": raw.get("engine")})

    # Step 2: Normalize V0 → V1
    sig_v1 = normalize_v0_to_v1(raw)
    print(f"  Normalized: V0 → V1 (direction={sig_v1['direction']}, engine={sig_v1['engine']})")
    log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
               "NORMALIZE", "PASS", {"version": "1.0", "direction": sig_v1["direction"]})

    # Step 3: Validate V1
    is_valid, errors = validate_v1(sig_v1)
    if not is_valid:
        for e in errors:
            print(f"  VALIDATION ERROR: {e}")
        log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
                   "VALIDATE", "FAIL", {"errors": errors})
        return False

    print(f"  Validated: {len(errors)} errors")
    log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
               "VALIDATE", "PASS", {"is_valid": True})

    # Step 4: Journal signal to ledger
    log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
               "SIGNAL_JOURNALED", "PASS", {
                   "direction": sig_v1["direction"],
                   "price": sig_v1["price"],
                   "engine": sig_v1["engine"],
                   "timeframe": sig_v1["timeframe"],
               })
    print(f"  Journaled: {sig_v1['symbol']} {sig_v1['direction']} @ {sig_v1['price']}")

    # Step 5: Dry-run guard enforcement (never live)
    guard = {
        "guard_active": True,
        "live_trading_blocked": True,
        "reason": "P6 dry-run guard: no live orders permitted",
    }
    log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
               "DRY_RUN_GUARD", "PASS", guard)
    print(f"  Guard: live blocked — dry-run only")

    # Step 6: Backtest (simulated)
    backtest_result = MOCK_BACKTEST.copy()
    if run_backtest_flag:
        backtest_result = run_backtest(sig_v1)
        log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
                   "BACKTEST", "PASS", {
                       "outcome": backtest_result["outcome"],
                       "pnl_pct": backtest_result["pnl_pct"],
                       "dry_run": True,
                   })
        print(f"  Backtest: {backtest_result['outcome']} ({backtest_result['pnl_pct']:+.2f}%)")
    else:
        print(f"  Backtest: skipped (--no-backtest)")

    # Step 7: Produce report
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = OUTPUT_DIR / f"signal_dry_run_{timestamp}_{cycle_id}.json"

    report = {
        "run_id": uuid.uuid4().hex,
        "cycle_id": cycle_id,
        "source": source,
        "signal_v0": raw,
        "signal_v1": sig_v1,
        "validation": {"is_valid": is_valid, "errors": errors},
        "guard": guard,
        "backtest": backtest_result,
        "live_order_placed": False,
        "elapsed_seconds": round(time.time() - start, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))

    summary = {"cycle_id": cycle_id, "symbol": sig_v1["symbol"], "direction": sig_v1["direction"],
               "backtest_outcome": backtest_result.get("outcome"),
               "live_order": False, "elapsed": report["elapsed_seconds"]}
    log_ledger("signal_dry_run", "signal_dry_run_worker", sig_v1["symbol"],
               "DRY_RUN_CYCLE_COMPLETE", "PASS", summary)

    print(f"  Report: {report_path}")
    print(f"  Result: PASS — 0 live orders (dry-run guard active)")
    return True


def main():
    parser = argparse.ArgumentParser(description="P6 Signal dry-run worker")
    parser.add_argument("--signal", help="Path to V0 signal JSON file")
    parser.add_argument("--no-backtest", action="store_true", help="Skip backtest simulation")
    args = parser.parse_args()

    ok = run_signal_dry_run(signal_path=args.signal, run_backtest_flag=not args.no_backtest)
    return 0 if ok else 1


if __name__ == "__main__":
    main()
