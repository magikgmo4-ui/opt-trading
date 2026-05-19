#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
TIMEZONE = "America/Montreal"
STATE_DIR = BASE.parents[1] / "state" / "trading_realtime_v1"
LOOP_APP = BASE / "app" / "runtime_loop_v1.py"
GUARD_APP = BASE / "app" / "guardrails_v1.py"
TIMER_RUNS_JSONL = STATE_DIR / "runtime_timer_runs_v1.jsonl"
DEFAULT_INTERVAL_SECONDS = 300


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


def try_parse_json(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def status(_: list[str]) -> int:
    payload = {
        "loop_app": str(LOOP_APP),
        "guard_app": str(GUARD_APP),
        "timer_runs_jsonl": str(TIMER_RUNS_JSONL),
        "default_interval_seconds": DEFAULT_INTERVAL_SECONDS,
        "timer_runs_count": len(load_jsonl(TIMER_RUNS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_plan(_: list[str]) -> int:
    payload = {
        "timer_mode": "controlled_tick_only",
        "default_interval_seconds": DEFAULT_INTERVAL_SECONDS,
        "sequence": [
            "runtime_loop_v1.py run-once",
            "guardrails_v1.py check-guardrails"
        ],
        "execution_policy": "observation_only",
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def tick_once(args: list[str]) -> int:
    live_path = args[0] if len(args) >= 1 and args[0] else ""

    loop_cmd = [sys.executable, str(LOOP_APP), "run-once"]
    if live_path:
        loop_cmd.append(live_path)
    loop_proc = subprocess.run(loop_cmd, capture_output=True, text=True)
    loop_json = try_parse_json(loop_proc.stdout)

    guard_cmd = [sys.executable, str(GUARD_APP), "check-guardrails"]
    guard_proc = subprocess.run(guard_cmd, capture_output=True, text=True)
    guard_json = try_parse_json(guard_proc.stdout)

    overall_ok = (loop_proc.returncode == 0) and (guard_proc.returncode == 0) and bool((guard_json or {}).get("overall_ok", False))
    payload = {
        "timer_ts": now_local().isoformat(timespec="seconds"),
        "live_path": live_path or None,
        "interval_seconds": DEFAULT_INTERVAL_SECONDS,
        "loop_returncode": loop_proc.returncode,
        "guard_returncode": guard_proc.returncode,
        "overall_ok": overall_ok,
        "loop_result": loop_json,
        "guardrails_result": guard_json,
    }
    append_jsonl(TIMER_RUNS_JSONL, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_last_run(_: list[str]) -> int:
    runs = load_jsonl(TIMER_RUNS_JSONL)
    if not runs:
        print(json.dumps({"message": "no runtime timer run yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(runs[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-plan": show_plan,
    "tick-once": tick_once,
    "show-last-run": show_last_run,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: timer_v1.py status|show-plan|tick-once [live_jsonl_path]|show-last-run", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
