#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"
LIVE_OBSERVATIONS_JSONL = STATE_DIR / "live_observations_v1.jsonl"
LIVE_OBSERVATION_RUNS_JSONL = STATE_DIR / "live_observation_runs_v1.jsonl"
LIVE_EXPORTS_DIR = STATE_DIR / "live_exports"
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


def normalize_live_record(source_path: Path, rec: dict) -> dict:
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


def render_markdown(observations: list[dict], scope: dict) -> str:
    lines = []
    lines.append("# Trading LIVE Observation Export")
    lines.append("")
    lines.append(f"Generated: {scope.get('export_ts')}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Source: {scope.get('source_path')}")
    lines.append(f"- Session: {scope.get('session_id') or 'all'}")
    lines.append(f"- Start date: {scope.get('start_date') or 'none'}")
    lines.append(f"- End date: {scope.get('end_date') or 'none'}")
    lines.append(f"- Observation count: {scope.get('observation_count')}")
    lines.append("")
    lines.append("## Observations")
    lines.append("")
    if not observations:
        lines.append("- none")
        lines.append("")
        return "\n".join(lines)
    for obs in observations:
        lines.append(f"- {obs.get('local_date')} | {obs.get('session_name')} | {obs.get('variant_id')} | {obs.get('direction')} | entry={obs.get('entry')} | sl={obs.get('sl')} | rr={obs.get('rr_planned')}")
    lines.append("")
    return "\n".join(lines)


def safe_tag(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return cleaned or fallback


def write_exports(prefix: str, payload: dict, markdown_text: str) -> dict:
    LIVE_EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now_local().strftime("%Y%m%d_%H%M%S")
    json_path = LIVE_EXPORTS_DIR / f"{prefix}_{stamp}.json"
    md_path = LIVE_EXPORTS_DIR / f"{prefix}_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(markdown_text, encoding="utf-8")
    return {
        "export_ts": payload.get("export_ts"),
        "json_export": str(json_path),
        "markdown_export": str(md_path),
    }


def status(_: list[str]) -> int:
    payload = {
        "sample_live_jsonl": str(SAMPLE_LIVE_JSONL),
        "live_observations_jsonl": str(LIVE_OBSERVATIONS_JSONL),
        "live_observation_runs_jsonl": str(LIVE_OBSERVATION_RUNS_JSONL),
        "live_exports_dir": str(LIVE_EXPORTS_DIR),
        "live_observations_count": len(load_jsonl(LIVE_OBSERVATIONS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def export_last(_: list[str]) -> int:
    runs = load_jsonl(LIVE_OBSERVATION_RUNS_JSONL)
    observations = load_jsonl(LIVE_OBSERVATIONS_JSONL)
    if not runs:
        print(json.dumps({"message": "no live observation run to export"}, indent=2, ensure_ascii=False))
        return 0
    last = runs[-1]
    filtered = filter_records(observations, last.get("session_id"), last.get("start_date"), last.get("end_date"))
    payload = {
        "export_ts": now_local().isoformat(timespec="seconds"),
        "source_path": last.get("source_path"),
        "session_id": last.get("session_id"),
        "start_date": last.get("start_date"),
        "end_date": last.get("end_date"),
        "observation_count": len(filtered),
        "observations": filtered,
    }
    result = write_exports("live_observation_export_last", payload, render_markdown(filtered, payload))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def export_new(args: list[str]) -> int:
    source_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_LIVE_JSONL
    session_id = args[1] if len(args) >= 2 and args[1] else None
    start_date = args[2] if len(args) >= 3 and args[2] else None
    end_date = args[3] if len(args) >= 4 and args[3] else None
    source_records = load_jsonl(source_path)
    filtered_source = filter_records(source_records, session_id, start_date, end_date)
    normalized = [normalize_live_record(source_path, rec) for rec in filtered_source]
    payload = {
        "export_ts": now_local().isoformat(timespec="seconds"),
        "source_path": str(source_path),
        "session_id": session_id,
        "start_date": start_date,
        "end_date": end_date,
        "observation_count": len(normalized),
        "observations": normalized,
    }
    prefix = "live_observation_export"
    if session_id:
        prefix += "_" + safe_tag(session_id, "session")
    result = write_exports(prefix, payload, render_markdown(normalized, payload))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "export-last": export_last,
    "export-new": export_new,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: live_export_v1.py status|export-last|export-new [live_jsonl_path] [session_id] [start_date] [end_date]", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
