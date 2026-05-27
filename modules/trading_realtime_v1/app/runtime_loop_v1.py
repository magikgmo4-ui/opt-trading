#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
TIMEZONE = "America/Montreal"
PROFILE_ID = "xauusd_dual_stack_v1"
STRATEGY_ID = "xau_session_open_v1"

if not validate_strategy_id(STRATEGY_ID):
    log_unknown_strategy_id_warning(STRATEGY_ID, "trading_realtime_v1.runtime_loop_v1")
SYMBOL = "XAUUSD"
LIVE_SOURCE_PATH = REPO_ROOT / "modules" / "trading_lab_v1" / "data" / "sample_live_reference_v1.jsonl"
STATE_DIR = REPO_ROOT / "state" / "trading_realtime_v1"
RUNTIME_OBSERVATIONS_JSONL = STATE_DIR / "runtime_observations_v1.jsonl"
RUNTIME_RUNS_JSONL = STATE_DIR / "runtime_runs_v1.jsonl"
RUNTIME_EVENTS_JSONL = STATE_DIR / "runtime_events_v1.jsonl"
RUNTIME_BRIDGE_RUNS_JSONL = STATE_DIR / "runtime_bridge_runs_v1.jsonl"
RUNTIME_REPORTS_JSONL = STATE_DIR / "runtime_reports_v1.jsonl"
RUNTIME_LOOP_RUNS_JSONL = STATE_DIR / "runtime_loop_runs_v1.jsonl"


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


def latest_live_record(path: Path) -> dict | None:
    rows = load_jsonl(path)
    if not rows:
        return None
    return rows[-1]


def normalize_record(source_path: Path, rec: dict) -> dict:
    return {
        "observation_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(source_path),
        "record_ts": rec.get("record_ts") or rec.get("live_ts"),
        "local_date": rec.get("local_date"),
        "session_name": rec.get("session_name") or rec.get("session_id"),
        "variant_id": rec.get("variant_id"),
        "direction": rec.get("direction"),
        "entry": rec.get("entry"),
        "sl": rec.get("sl"),
        "rr_planned": rec.get("rr_planned"),
        "source": rec.get("source") or rec.get("source_csv") or "live_source",
        "runtime_mode": "observation_only",
        "runtime_status": "observed"
    }


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
            "bridge": "runtime_loop_v1",
            "source_path": observation.get("source_path")
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
        "notes": "realtime_runtime_loop_v1"
    }


def filter_records(records: list[dict], session_id: str | None, start_date: str | None, end_date: str | None) -> list[dict]:
    out = []
    for rec in records:
        rec_session = rec.get("session_name") or rec.get("session_id")
        rec_date = rec.get("local_date")
        if session_id and rec_session != session_id:
            continue
        if start_date and rec_date and rec_date < start_date:
            continue
        if end_date and rec_date and rec_date > end_date:
            continue
        out.append(rec)
    return out


def avg(values: list):
    nums = [float(v) for v in values if v is not None]
    return round(mean(nums), 4) if nums else None


def counts_by(records: list[dict], key: str) -> dict:
    out = {}
    for rec in records:
        value = rec.get(key)
        tag = str(value) if value is not None else "none"
        out[tag] = out.get(tag, 0) + 1
    return out


def build_report(session_id: str | None, start_date: str | None, end_date: str | None) -> dict:
    observations = filter_records(load_jsonl(RUNTIME_OBSERVATIONS_JSONL), session_id, start_date, end_date)
    runs = filter_records(load_jsonl(RUNTIME_RUNS_JSONL), session_id, start_date, end_date)
    events = filter_records(load_jsonl(RUNTIME_EVENTS_JSONL), session_id, start_date, end_date)
    bridge_runs = filter_records(load_jsonl(RUNTIME_BRIDGE_RUNS_JSONL), session_id, start_date, end_date)
    return {
        "report_ts": now_local().isoformat(timespec="seconds"),
        "session_id": session_id,
        "start_date": start_date,
        "end_date": end_date,
        "runtime_observations_count": len(observations),
        "runtime_runs_count": len(runs),
        "runtime_events_count": len(events),
        "runtime_bridge_runs_count": len(bridge_runs),
        "dates": sorted({rec.get("local_date") for rec in observations if rec.get("local_date")}),
        "sessions": counts_by(observations, "session_name"),
        "variants": counts_by(events, "variant_id"),
        "directions": counts_by(events, "direction"),
        "event_types": counts_by(events, "event_type"),
        "avg_entry": avg([rec.get("entry") for rec in observations]),
        "avg_sl": avg([rec.get("sl") for rec in observations]),
        "avg_rr_planned": avg([rec.get("rr_planned") for rec in observations])
    }


def status(_: list[str]) -> int:
    payload = {
        "live_source_path": str(LIVE_SOURCE_PATH),
        "runtime_loop_runs_jsonl": str(RUNTIME_LOOP_RUNS_JSONL),
        "runtime_loop_runs_count": len(load_jsonl(RUNTIME_LOOP_RUNS_JSONL)),
        "runtime_observations_count": len(load_jsonl(RUNTIME_OBSERVATIONS_JSONL)),
        "runtime_events_count": len(load_jsonl(RUNTIME_EVENTS_JSONL)),
        "runtime_reports_count": len(load_jsonl(RUNTIME_REPORTS_JSONL))
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def run_once(args: list[str]) -> int:
    live_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else LIVE_SOURCE_PATH
    record = latest_live_record(live_path)
    if record is None:
        print(json.dumps({"message": "no live record found", "source": str(live_path)}, indent=2, ensure_ascii=False))
        return 0

    observation = normalize_record(live_path, record)
    append_jsonl(RUNTIME_OBSERVATIONS_JSONL, observation)

    run_payload = {
        "run_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(live_path),
        "record_ts": observation.get("record_ts"),
        "local_date": observation.get("local_date"),
        "session_name": observation.get("session_name"),
        "variant_id": observation.get("variant_id"),
        "direction": observation.get("direction"),
        "observation_written": str(RUNTIME_OBSERVATIONS_JSONL)
    }
    append_jsonl(RUNTIME_RUNS_JSONL, run_payload)

    event = build_event(observation)
    append_jsonl(RUNTIME_EVENTS_JSONL, event)

    bridge_payload = {
        "bridge_ts": now_local().isoformat(timespec="seconds"),
        "event_id": event.get("event_id"),
        "source_observation_ts": observation.get("observation_ts"),
        "local_date": observation.get("local_date"),
        "session_name": observation.get("session_name"),
        "runtime_event_written": str(RUNTIME_EVENTS_JSONL)
    }
    append_jsonl(RUNTIME_BRIDGE_RUNS_JSONL, bridge_payload)

    report = build_report(observation.get("session_name"), observation.get("local_date"), observation.get("local_date"))
    append_jsonl(RUNTIME_REPORTS_JSONL, report)

    loop_payload = {
        "loop_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(live_path),
        "record_ts": observation.get("record_ts"),
        "local_date": observation.get("local_date"),
        "session_name": observation.get("session_name"),
        "variant_id": observation.get("variant_id"),
        "direction": observation.get("direction"),
        "observation_written": str(RUNTIME_OBSERVATIONS_JSONL),
        "event_written": str(RUNTIME_EVENTS_JSONL),
        "report_written": str(RUNTIME_REPORTS_JSONL)
    }
    append_jsonl(RUNTIME_LOOP_RUNS_JSONL, loop_payload)
    print(json.dumps(loop_payload, indent=2, ensure_ascii=False))
    return 0


def show_last_run(_: list[str]) -> int:
    runs = load_jsonl(RUNTIME_LOOP_RUNS_JSONL)
    if not runs:
        print(json.dumps({"message": "no runtime loop run yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(runs[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "run-once": run_once,
    "show-last-run": show_last_run
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: runtime_loop_v1.py status|run-once [live_jsonl_path]|show-last-run", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
