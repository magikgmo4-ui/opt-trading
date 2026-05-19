#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
TIMEZONE = "America/Montreal"
STATE_DIR = REPO_ROOT / "state" / "trading_realtime_v1"
RUNTIME_OBSERVATIONS_JSONL = STATE_DIR / "runtime_observations_v1.jsonl"
RUNTIME_RUNS_JSONL = STATE_DIR / "runtime_runs_v1.jsonl"
RUNTIME_EVENTS_JSONL = STATE_DIR / "runtime_events_v1.jsonl"
RUNTIME_BRIDGE_RUNS_JSONL = STATE_DIR / "runtime_bridge_runs_v1.jsonl"
RUNTIME_REPORTS_JSONL = STATE_DIR / "runtime_reports_v1.jsonl"
RUNTIME_EXPORTS_DIR = STATE_DIR / "runtime_exports"


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

    report = {
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
    return report


def render_markdown(report: dict) -> str:
    lines = []
    lines.append("# Trading REALTIME V1 — Runtime Report Export")
    lines.append("")
    lines.append(f"Generated: {report.get('report_ts')}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Session: {report.get('session_id') or 'all'}")
    lines.append(f"- Start date: {report.get('start_date') or 'none'}")
    lines.append(f"- End date: {report.get('end_date') or 'none'}")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- Runtime observations: {report.get('runtime_observations_count')}")
    lines.append(f"- Runtime runs: {report.get('runtime_runs_count')}")
    lines.append(f"- Runtime events: {report.get('runtime_events_count')}")
    lines.append(f"- Runtime bridge runs: {report.get('runtime_bridge_runs_count')}")
    lines.append("")
    lines.append("## Dates")
    lines.append("")
    dates = report.get("dates") or []
    if dates:
        for d in dates:
            lines.append(f"- {d}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Sessions")
    lines.append("")
    sessions = report.get("sessions") or {}
    if sessions:
        for key, value in sessions.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Variant distribution")
    lines.append("")
    variants = report.get("variants") or {}
    if variants:
        for key, value in variants.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Direction distribution")
    lines.append("")
    directions = report.get("directions") or {}
    if directions:
        for key, value in directions.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Event types")
    lines.append("")
    event_types = report.get("event_types") or {}
    if event_types:
        for key, value in event_types.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Averages")
    lines.append("")
    lines.append(f"- Avg entry: {report.get('avg_entry')}")
    lines.append(f"- Avg sl: {report.get('avg_sl')}")
    lines.append(f"- Avg RR planned: {report.get('avg_rr_planned')}")
    lines.append("")
    return "\n".join(lines)


def safe_tag(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return cleaned or fallback


def write_exports(prefix: str, payload: dict, markdown_text: str) -> dict:
    RUNTIME_EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now_local().strftime("%Y%m%d_%H%M%S")
    json_path = RUNTIME_EXPORTS_DIR / f"{prefix}_{stamp}.json"
    md_path = RUNTIME_EXPORTS_DIR / f"{prefix}_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(markdown_text, encoding="utf-8")
    return {
        "export_ts": payload.get("report_ts") or now_local().isoformat(timespec="seconds"),
        "json_export": str(json_path),
        "markdown_export": str(md_path)
    }


def status(_: list[str]) -> int:
    payload = {
        "runtime_reports_jsonl": str(RUNTIME_REPORTS_JSONL),
        "runtime_exports_dir": str(RUNTIME_EXPORTS_DIR),
        "runtime_reports_count": len(load_jsonl(RUNTIME_REPORTS_JSONL))
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def export_last(_: list[str]) -> int:
    reports = load_jsonl(RUNTIME_REPORTS_JSONL)
    if not reports:
        print(json.dumps({"message": "no runtime report to export"}, indent=2, ensure_ascii=False))
        return 0
    latest = reports[-1]
    result = write_exports("runtime_report_export_last", latest, render_markdown(latest))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def export_new(args: list[str]) -> int:
    session_id = args[0] if len(args) >= 1 and args[0] else None
    start_date = args[1] if len(args) >= 2 and args[1] else None
    end_date = args[2] if len(args) >= 3 and args[2] else None
    report = build_report(session_id, start_date, end_date)
    append_jsonl(RUNTIME_REPORTS_JSONL, report)
    prefix = "runtime_report_export"
    if session_id:
        prefix += "_" + safe_tag(session_id, "session")
    result = write_exports(prefix, report, render_markdown(report))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "export-last": export_last,
    "export-new": export_new
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: export_v1.py status|export-last|export-new [session_id] [start_date] [end_date]", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
