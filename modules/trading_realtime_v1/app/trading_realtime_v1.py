#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
PROFILE_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "xauusd_dual_stack_v1.profile.yaml"
EVENT_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_event_v1.schema.json"
TRADE_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_trade_v1.schema.json"
LIVE_SOURCE_PATH = REPO_ROOT / "modules" / "trading_lab_v1" / "data" / "sample_live_reference_v1.jsonl"
STATE_DIR = REPO_ROOT / "state" / "trading_realtime_v1"
RUNTIME_OBSERVATIONS_JSONL = STATE_DIR / "runtime_observations_v1.jsonl"
RUNTIME_RUNS_JSONL = STATE_DIR / "runtime_runs_v1.jsonl"
TIMEZONE = "America/Montreal"


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


def runtime_status(_: list[str]) -> int:
    payload = {
        "runtime_observations_jsonl": str(RUNTIME_OBSERVATIONS_JSONL),
        "runtime_runs_jsonl": str(RUNTIME_RUNS_JSONL),
        "runtime_observations_count": len(load_jsonl(RUNTIME_OBSERVATIONS_JSONL)),
        "runtime_runs_count": len(load_jsonl(RUNTIME_RUNS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def status(_: list[str]) -> int:
    payload = {
        "module": "trading_realtime_v1",
        "base": str(BASE),
        "repo_root": str(REPO_ROOT),
        "profile_exists": PROFILE_PATH.exists(),
        "event_schema_exists": EVENT_SCHEMA_PATH.exists(),
        "trade_schema_exists": TRADE_SCHEMA_PATH.exists(),
        "live_source_exists": LIVE_SOURCE_PATH.exists(),
        "state_dir": str(STATE_DIR),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_profile(_: list[str]) -> int:
    print(str(PROFILE_PATH))
    return 0


def show_schemas(_: list[str]) -> int:
    print(str(EVENT_SCHEMA_PATH))
    print(str(TRADE_SCHEMA_PATH))
    return 0


def show_live_source(_: list[str]) -> int:
    print(str(LIVE_SOURCE_PATH))
    return 0


def observe_once(args: list[str]) -> int:
    live_path = Path(args[0]).expanduser() if args and args[0] else LIVE_SOURCE_PATH
    record = latest_live_record(live_path)
    if record is None:
        print(json.dumps({"message": "no live record found", "source": str(live_path)}, indent=2, ensure_ascii=False))
        return 0

    observation = {
        "observation_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(live_path),
        "record_ts": record.get("record_ts") or record.get("live_ts"),
        "local_date": record.get("local_date"),
        "session_name": record.get("session_name") or record.get("session_id"),
        "variant_id": record.get("variant_id"),
        "direction": record.get("direction"),
        "entry": record.get("entry"),
        "sl": record.get("sl"),
        "rr_planned": record.get("rr_planned"),
        "runtime_mode": "observation_only",
        "runtime_status": "observed",
    }
    append_jsonl(RUNTIME_OBSERVATIONS_JSONL, observation)

    run_payload = {
        "run_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(live_path),
        "record_ts": observation.get("record_ts"),
        "local_date": observation.get("local_date"),
        "session_name": observation.get("session_name"),
        "variant_id": observation.get("variant_id"),
        "direction": observation.get("direction"),
        "observation_written": str(RUNTIME_OBSERVATIONS_JSONL),
    }
    append_jsonl(RUNTIME_RUNS_JSONL, run_payload)
    print(json.dumps(run_payload, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-profile": show_profile,
    "show-schemas": show_schemas,
    "show-live-source": show_live_source,
    "observe-once": observe_once,
    "runtime-status": runtime_status,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: trading_realtime_v1.py status|show-profile|show-schemas|show-live-source|observe-once [live_jsonl_path]|runtime-status", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
