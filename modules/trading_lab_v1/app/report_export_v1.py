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
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"
FEATURES_JSONL = STATE_DIR / "features_v1.jsonl"
TRADES_JSONL = STATE_DIR / "trades_v1.jsonl"
MARKET_RUNS_JSONL = STATE_DIR / "market_runs_v1.jsonl"
BATCH_RUNS_JSONL = STATE_DIR / "batch_runs_v1.jsonl"
BATCH_REPORTS_JSONL = STATE_DIR / "batch_reports_v1.jsonl"
EXPORTS_DIR = STATE_DIR / "exports"
TIMEZONE = "America/Montreal"


def now_local() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    items = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def filter_records(records: list[dict], session_id: str | None, start_date: str | None, end_date: str | None) -> list[dict]:
    filtered = []
    for rec in records:
        rec_session = rec.get("session_name") or rec.get("session_id")
        rec_date = rec.get("local_date") or rec.get("analysis_date")
        if session_id and rec_session != session_id:
            continue
        if start_date and rec_date and rec_date < start_date:
            continue
        if end_date and rec_date and rec_date > end_date:
            continue
        filtered.append(rec)
    return filtered


def avg(values: list[float | int | None]):
    nums = [float(v) for v in values if v is not None]
    return round(mean(nums), 4) if nums else None


def counts_by(records: list[dict], key: str) -> dict:
    out: dict[str, int] = {}
    for rec in records:
        value = rec.get(key)
        tag = str(value) if value is not None else "none"
        out[tag] = out.get(tag, 0) + 1
    return out


def build_report(session_id: str | None, start_date: str | None, end_date: str | None) -> dict:
    features = filter_records(load_jsonl(FEATURES_JSONL), session_id, start_date, end_date)
    trades = filter_records(load_jsonl(TRADES_JSONL), session_id, start_date, end_date)
    market_runs = filter_records(load_jsonl(MARKET_RUNS_JSONL), session_id, start_date, end_date)
    batch_runs = filter_records(load_jsonl(BATCH_RUNS_JSONL), session_id, start_date, end_date)

    report = {
        "report_ts": now_local().isoformat(timespec="seconds"),
        "session_id": session_id,
        "start_date": start_date,
        "end_date": end_date,
        "features_count": len(features),
        "trades_count": len(trades),
        "market_runs_count": len(market_runs),
        "batch_runs_count": len(batch_runs),
        "sequence_complete_count": sum(1 for f in features if f.get("sequence_complete")),
        "dates": sorted({f.get("local_date") for f in features if f.get("local_date")}),
        "variants": counts_by(features, "variant_id"),
        "directions": counts_by(features, "first5_direction"),
        "avg_open_range_points": avg([((f.get("open_candle") or {}).get("range_points")) for f in features]),
        "avg_open_body_points": avg([((f.get("open_candle") or {}).get("body_points")) for f in features]),
        "avg_first5_range_points": avg([f.get("first5_range_points") for f in features]),
        "avg_first5_body_delta": avg([f.get("first5_body_delta") for f in features]),
        "avg_fvg_gap_points": avg([f.get("fvg_gap_points") for f in features]),
        "avg_rr_planned": avg([f.get("rr_planned") for f in features]),
        "trade_results": counts_by(trades, "result"),
    }
    return report


def render_markdown(report: dict) -> str:
    lines = []
    lines.append("# Trading LAB V1 — Batch Report Export")
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
    lines.append(f"- Features: {report.get('features_count')}")
    lines.append(f"- Trades: {report.get('trades_count')}")
    lines.append(f"- Market runs: {report.get('market_runs_count')}")
    lines.append(f"- Batch runs: {report.get('batch_runs_count')}")
    lines.append(f"- Sequence complete: {report.get('sequence_complete_count')}")
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
    lines.append("## Averages")
    lines.append("")
    lines.append(f"- Avg open range points: {report.get('avg_open_range_points')}")
    lines.append(f"- Avg open body points: {report.get('avg_open_body_points')}")
    lines.append(f"- Avg first5 range points: {report.get('avg_first5_range_points')}")
    lines.append(f"- Avg first5 body delta: {report.get('avg_first5_body_delta')}")
    lines.append(f"- Avg FVG gap points: {report.get('avg_fvg_gap_points')}")
    lines.append(f"- Avg RR planned: {report.get('avg_rr_planned')}")
    lines.append("")
    lines.append("## Trade results")
    lines.append("")
    results = report.get("trade_results") or {}
    if results:
        for key, value in results.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def safe_tag(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return cleaned or fallback


def export_report(report: dict, prefix: str) -> dict:
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now_local().strftime("%Y%m%d_%H%M%S")
    json_path = EXPORTS_DIR / f"{prefix}_{stamp}.json"
    md_path = EXPORTS_DIR / f"{prefix}_{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    payload = {
        "report_ts": report.get("report_ts"),
        "json_export": str(json_path),
        "markdown_export": str(md_path),
    }
    return payload


def export_last(_: list[str]) -> int:
    reports = load_jsonl(BATCH_REPORTS_JSONL)
    if not reports:
        print(json.dumps({"message": "no batch report to export"}, indent=2, ensure_ascii=False))
        return 0
    latest = reports[-1]
    payload = export_report(latest, "latest_batch_report")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def export_new(args: list[str]) -> int:
    session_id = args[0] if len(args) >= 1 and args[0] else None
    start_date = args[1] if len(args) >= 2 and args[1] else None
    end_date = args[2] if len(args) >= 3 and args[2] else None
    report = build_report(session_id, start_date, end_date)
    append_jsonl(BATCH_REPORTS_JSONL, report)
    prefix = "batch_report_export"
    if session_id:
        prefix += "_" + safe_tag(session_id, "session")
    payload = export_report(report, prefix)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def status(_: list[str]) -> int:
    payload = {
        "batch_reports_jsonl": str(BATCH_REPORTS_JSONL),
        "exports_dir": str(EXPORTS_DIR),
        "batch_reports_count": len(load_jsonl(BATCH_REPORTS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
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
        print("Usage: report_export_v1.py status|export-last|export-new [session_id] [start_date] [end_date]", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
