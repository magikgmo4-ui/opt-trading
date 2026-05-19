#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"
LIVE_OBSERVATIONS_JSONL = STATE_DIR / "live_observations_v1.jsonl"
LIVE_OBSERVATION_RUNS_JSONL = STATE_DIR / "live_observation_runs_v1.jsonl"
SAMPLE_LIVE_JSONL = BASE / "data" / "sample_live_reference_v1.jsonl"
TIMEZONE = "America/Montreal"


def now_local() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
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
        "observation_mode": "live_observation",
        "observation_status": "observed",
    }


def status(_: list[str]) -> int:
    payload = {
        "sample_live_jsonl": str(SAMPLE_LIVE_JSONL),
        "live_observations_jsonl": str(LIVE_OBSERVATIONS_JSONL),
        "live_observation_runs_jsonl": str(LIVE_OBSERVATION_RUNS_JSONL),
        "live_observations_count": len(load_jsonl(LIVE_OBSERVATIONS_JSONL)),
        "live_observation_runs_count": len(load_jsonl(LIVE_OBSERVATION_RUNS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_source(_: list[str]) -> int:
    print(str(SAMPLE_LIVE_JSONL))
    return 0


def observe_live(args: list[str]) -> int:
    source_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_LIVE_JSONL
    session_id = args[1] if len(args) >= 2 and args[1] else None
    start_date = args[2] if len(args) >= 3 and args[2] else None
    end_date = args[3] if len(args) >= 4 and args[3] else None

    source_records = load_jsonl(source_path)
    filtered = filter_records(source_records, session_id, start_date, end_date)

    observed = []
    for rec in filtered:
        normalized = normalize_record(source_path, rec)
        append_jsonl(LIVE_OBSERVATIONS_JSONL, normalized)
        observed.append(normalized)

    summary = {
        "run_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(source_path),
        "session_id": session_id,
        "start_date": start_date,
        "end_date": end_date,
        "input_count": len(source_records),
        "observed_count": len(observed),
        "dates": sorted({o.get("local_date") for o in observed if o.get("local_date")}),
        "sessions": sorted({o.get("session_name") for o in observed if o.get("session_name")}),
    }
    append_jsonl(LIVE_OBSERVATION_RUNS_JSONL, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def show_last_run(_: list[str]) -> int:
    runs = load_jsonl(LIVE_OBSERVATION_RUNS_JSONL)
    if not runs:
        print(json.dumps({"message": "no live observation run yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(runs[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-source": show_source,
    "observe-live": observe_live,
    "show-last-run": show_last_run,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: live_observation_v1.py status|show-source|observe-live [live_jsonl_path] [session_id] [start_date] [end_date]|show-last-run", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
