#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
PROFILE_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "xauusd_dual_stack_v1.profile.yaml"
EVENT_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_event_v1.schema.json"
TRADE_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_trade_v1.schema.json"
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sample_event() -> dict:
    return {
        "event_id": "evt_sample_xau_001",
        "event_ts": iso_now(),
        "profile_id": "xauusd_dual_stack_v1",
        "mode": "observation",
        "symbol": "XAUUSD",
        "timeframe_context": {
            "trigger_tf": "M1",
            "context_tf": "M5"
        },
        "session_name": "gold_open_18h",
        "local_date": datetime.now().date().isoformat(),
        "timezone": "America/Montreal",
        "strategy_id": "xau_session_open_v1",
        "variant_id": "xau_open_sweep_fvg",
        "setup_instance_id": "setup_sample_xau_001",
        "event_type": "setup_classified",
        "decision_state": "observed",
        "direction": "bullish",
        "signal_ts": iso_now(),
        "filters_state": {
            "require_session_window": True,
            "require_complete_open_sequence": True
        },
        "frame_state": {
            "session_allowed": True,
            "max_trades_per_day_ok": True,
            "cooldown_ok": True
        },
        "raw_features": {
            "sweep_detected": True,
            "fvg_detected": True,
            "m5_open_candle_captured": True,
            "m1_first_5_complete": True
        },
        "notes": None
    }


def sample_trade() -> dict:
    return {
        "trade_id": "trd_sample_xau_001",
        "event_id_origin": "evt_sample_xau_001",
        "profile_id": "xauusd_dual_stack_v1",
        "mode": "observation",
        "symbol": "XAUUSD",
        "strategy_id": "xau_session_open_v1",
        "variant_id": "xau_open_sweep_fvg",
        "setup_instance_id": "setup_sample_xau_001",
        "session_name": "gold_open_18h",
        "local_date": datetime.now().date().isoformat(),
        "timezone": "America/Montreal",
        "direction": "bullish",
        "entry_ts": iso_now(),
        "exit_ts": None,
        "entry": 3200.0,
        "sl": 3195.0,
        "tp_plan": {
            "type": "rr_multiple",
            "rr_target": 2.0
        },
        "risk_pct": 1.0,
        "rr_planned": 2.0,
        "result": "open",
        "r_realized": None,
        "mfe": None,
        "mae": None,
        "time_in_trade_seconds": None,
        "execution_state": "virtual_open",
        "exit_reason": None,
        "slippage_points": 0.0
    }


def status() -> int:
    payload = {
        "module": "trading_lab_v1",
        "base": str(BASE),
        "repo_root": str(REPO_ROOT),
        "profile_exists": PROFILE_PATH.exists(),
        "event_schema_exists": EVENT_SCHEMA_PATH.exists(),
        "trade_schema_exists": TRADE_SCHEMA_PATH.exists(),
        "state_dir": str(STATE_DIR),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_profile() -> int:
    print(str(PROFILE_PATH))
    return 0


def show_schemas() -> int:
    print(str(EVENT_SCHEMA_PATH))
    print(str(TRADE_SCHEMA_PATH))
    return 0


def emit_sample_event() -> int:
    print(json.dumps(sample_event(), indent=2, ensure_ascii=False))
    return 0


def emit_sample_trade() -> int:
    print(json.dumps(sample_trade(), indent=2, ensure_ascii=False))
    return 0


def materialize_samples() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    event_path = STATE_DIR / "sample_event_v1.json"
    trade_path = STATE_DIR / "sample_trade_v1.json"
    event_path.write_text(json.dumps(sample_event(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    trade_path.write_text(json.dumps(sample_trade(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "event_sample": str(event_path),
        "trade_sample": str(trade_path)
    }, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-profile": show_profile,
    "show-schemas": show_schemas,
    "sample-event": emit_sample_event,
    "sample-trade": emit_sample_trade,
    "materialize-samples": materialize_samples,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: trading_lab_v1.py status|show-profile|show-schemas|sample-event|sample-trade|materialize-samples", file=sys.stderr)
        return 1
    return fn()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
