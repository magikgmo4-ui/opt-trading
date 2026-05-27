#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
PROFILE_ID = "xauusd_dual_stack_v1"
STRATEGY_ID = "xau_session_open_v1"

if not validate_strategy_id(STRATEGY_ID):
    log_unknown_strategy_id_warning(STRATEGY_ID, "trading_realtime_v1.event_bridge_v1")
SYMBOL = "XAUUSD"
TIMEZONE = "America/Montreal"
STATE_DIR = REPO_ROOT / "state" / "trading_realtime_v1"
RUNTIME_OBSERVATIONS_JSONL = STATE_DIR / "runtime_observations_v1.jsonl"
RUNTIME_EVENTS_JSONL = STATE_DIR / "runtime_events_v1.jsonl"
RUNTIME_BRIDGE_RUNS_JSONL = STATE_DIR / "runtime_bridge_runs_v1.jsonl"
EVENT_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_event_v1.schema.json"


def now_local() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def latest_observation() -> dict | None:
    rows = load_jsonl(RUNTIME_OBSERVATIONS_JSONL)
    if not rows:
        return None
    return rows[-1]


def build_event(observation: dict) -> dict:
    stamp = now_local().strftime("%Y%m%d_%H%M%S")
    session_name = observation.get("session_name") or "unknown_session"
    event_id = f"evt_realtime_{stamp}_{session_name}"
    signal_ts = observation.get("record_ts") or observation.get("observation_ts")
    return {
        "event_id": event_id,
        "event_ts": now_local().isoformat(timespec="seconds"),
        "profile_id": PROFILE_ID,
        "mode": "observation",
        "symbol": SYMBOL,
        "timeframe_context": {
            "trigger_tf": "LIVE",
            "context_tf": "LIVE",
            "runner": "trading_realtime_v1",
            "bridge": "event_bridge_v1",
            "source_path": observation.get("source_path"),
        },
        "session_name": observation.get("session_name"),
        "local_date": observation.get("local_date"),
        "timezone": TIMEZONE,
        "strategy_id": STRATEGY_ID,
        "variant_id": observation.get("variant_id"),
        "setup_instance_id": event_id.replace("evt_", "setup_", 1),
        "event_type": "runtime_observed",
        "decision_state": "observed",
        "direction": observation.get("direction"),
        "signal_ts": signal_ts,
        "filters_state": {
            "require_runtime_source": True,
            "require_runtime_observation": True
        },
        "frame_state": {
            "runtime_mode": observation.get("runtime_mode") or "observation_only",
            "runtime_status": observation.get("runtime_status") or "observed"
        },
        "raw_features": {
            "entry": observation.get("entry"),
            "sl": observation.get("sl"),
            "rr_planned": observation.get("rr_planned"),
            "source": observation.get("source_path")
        },
        "notes": "realtime_event_bridge_v1"
    }


def status(_: list[str]) -> int:
    payload = {
        "event_schema_exists": EVENT_SCHEMA_PATH.exists(),
        "runtime_observations_jsonl": str(RUNTIME_OBSERVATIONS_JSONL),
        "runtime_events_jsonl": str(RUNTIME_EVENTS_JSONL),
        "runtime_bridge_runs_jsonl": str(RUNTIME_BRIDGE_RUNS_JSONL),
        "runtime_observations_count": len(load_jsonl(RUNTIME_OBSERVATIONS_JSONL)),
        "runtime_events_count": len(load_jsonl(RUNTIME_EVENTS_JSONL)),
        "runtime_bridge_runs_count": len(load_jsonl(RUNTIME_BRIDGE_RUNS_JSONL))
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def bridge_latest(_: list[str]) -> int:
    observation = latest_observation()
    if observation is None:
        print(json.dumps({"message": "no runtime observation found"}, indent=2, ensure_ascii=False))
        return 0

    event = build_event(observation)
    append_jsonl(RUNTIME_EVENTS_JSONL, event)
    run_payload = {
        "bridge_ts": now_local().isoformat(timespec="seconds"),
        "event_id": event.get("event_id"),
        "source_observation_ts": observation.get("observation_ts"),
        "local_date": observation.get("local_date"),
        "session_name": observation.get("session_name"),
        "runtime_event_written": str(RUNTIME_EVENTS_JSONL)
    }
    append_jsonl(RUNTIME_BRIDGE_RUNS_JSONL, run_payload)
    print(json.dumps(run_payload, indent=2, ensure_ascii=False))
    return 0


def show_last_event(_: list[str]) -> int:
    events = load_jsonl(RUNTIME_EVENTS_JSONL)
    if not events:
        print(json.dumps({"message": "no runtime event yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(events[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "bridge-latest": bridge_latest,
    "show-last-event": show_last_event
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: event_bridge_v1.py status|bridge-latest|show-last-event", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
