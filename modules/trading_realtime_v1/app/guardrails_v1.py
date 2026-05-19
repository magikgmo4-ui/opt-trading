#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
TIMEZONE = "America/Montreal"
STATE_DIR = REPO_ROOT / "state" / "trading_realtime_v1"
RUNTIME_OBSERVATIONS_JSONL = STATE_DIR / "runtime_observations_v1.jsonl"
RUNTIME_EVENTS_JSONL = STATE_DIR / "runtime_events_v1.jsonl"
RUNTIME_LOOP_RUNS_JSONL = STATE_DIR / "runtime_loop_runs_v1.jsonl"
RUNTIME_GUARDRAILS_REPORTS_JSONL = STATE_DIR / "runtime_guardrails_reports_v1.jsonl"
LIVE_SOURCE_PATH = REPO_ROOT / "modules" / "trading_lab_v1" / "data" / "sample_live_reference_v1.jsonl"


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


def last_record(path: Path):
    rows = load_jsonl(path)
    return rows[-1] if rows else None


def bool_check(name: str, ok: bool, detail):
    return {"name": name, "ok": ok, "detail": detail}


def build_report() -> dict:
    observation = last_record(RUNTIME_OBSERVATIONS_JSONL)
    event = last_record(RUNTIME_EVENTS_JSONL)
    loop_run = last_record(RUNTIME_LOOP_RUNS_JSONL)

    checks = []
    checks.append(bool_check("live_source_exists", LIVE_SOURCE_PATH.exists(), str(LIVE_SOURCE_PATH)))
    checks.append(bool_check("observation_exists", observation is not None, observation.get("observation_ts") if observation else None))
    checks.append(bool_check("event_exists", event is not None, event.get("event_id") if event else None))
    checks.append(bool_check("loop_run_exists", loop_run is not None, loop_run.get("loop_ts") if loop_run else None))

    if observation is not None:
        checks.append(bool_check("observation_runtime_mode", observation.get("runtime_mode") == "observation_only", observation.get("runtime_mode")))
        checks.append(bool_check("observation_runtime_status", observation.get("runtime_status") == "observed", observation.get("runtime_status")))
        checks.append(bool_check("observation_has_no_execution_flag", observation.get("execution_enabled") is not True, observation.get("execution_enabled")))

    if event is not None:
        checks.append(bool_check("event_mode", event.get("mode") == "observation", event.get("mode")))
        checks.append(bool_check("event_decision_state", event.get("decision_state") == "observed", event.get("decision_state")))
        checks.append(bool_check("event_type", event.get("event_type") == "runtime_observed", event.get("event_type")))
        frame_state = event.get("frame_state") or {}
        checks.append(bool_check("event_runtime_mode", frame_state.get("runtime_mode") == "observation_only", frame_state.get("runtime_mode")))
        checks.append(bool_check("event_runtime_status", frame_state.get("runtime_status") == "observed", frame_state.get("runtime_status")))
        raw_features = event.get("raw_features") or {}
        checks.append(bool_check("event_has_no_broker_order_flag", raw_features.get("broker_order") is None, raw_features.get("broker_order")))

    if loop_run is not None:
        checks.append(bool_check("loop_has_observation_output", bool(loop_run.get("observation_written")), loop_run.get("observation_written")))
        checks.append(bool_check("loop_has_event_output", bool(loop_run.get("event_written")), loop_run.get("event_written")))
        checks.append(bool_check("loop_has_report_output", bool(loop_run.get("report_written")), loop_run.get("report_written")))

    ok = all(item["ok"] for item in checks)
    return {
        "guardrails_ts": now_local().isoformat(timespec="seconds"),
        "overall_ok": ok,
        "checks": checks,
        "latest_observation_ts": observation.get("observation_ts") if observation else None,
        "latest_event_id": event.get("event_id") if event else None,
        "latest_loop_ts": loop_run.get("loop_ts") if loop_run else None,
    }


def status(_: list[str]) -> int:
    payload = {
        "runtime_observations_jsonl": str(RUNTIME_OBSERVATIONS_JSONL),
        "runtime_events_jsonl": str(RUNTIME_EVENTS_JSONL),
        "runtime_loop_runs_jsonl": str(RUNTIME_LOOP_RUNS_JSONL),
        "runtime_guardrails_reports_jsonl": str(RUNTIME_GUARDRAILS_REPORTS_JSONL),
        "runtime_guardrails_reports_count": len(load_jsonl(RUNTIME_GUARDRAILS_REPORTS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def check_guardrails(_: list[str]) -> int:
    report = build_report()
    append_jsonl(RUNTIME_GUARDRAILS_REPORTS_JSONL, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def show_last_report(_: list[str]) -> int:
    reports = load_jsonl(RUNTIME_GUARDRAILS_REPORTS_JSONL)
    if not reports:
        print(json.dumps({"message": "no runtime guardrails report yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(reports[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "check-guardrails": check_guardrails,
    "show-last-report": show_last_report,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: guardrails_v1.py status|check-guardrails|show-last-report", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
