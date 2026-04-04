#!/usr/bin/env python3
import json
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
COMPARATOR_REPORTS_JSONL = STATE_DIR / "comparator_reports_v1.jsonl"
COMPARATOR_PAIRS_JSONL = STATE_DIR / "comparator_pairs_v1.jsonl"
SAMPLE_LIVE_JSONL = BASE / "data" / "sample_live_reference_v1.jsonl"
TIMEZONE = "America/Montreal"


def now_local() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    items: list[dict] = []
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


def reduce_latest_by_key(records: list[dict], key_fields: tuple[str, ...], ts_candidates: tuple[str, ...]) -> dict[tuple, dict]:
    chosen: dict[tuple, dict] = {}
    for rec in records:
        key = tuple(rec.get(field) for field in key_fields)
        rec_ts = None
        for field in ts_candidates:
            value = rec.get(field)
            if value:
                rec_ts = value
                break
        prev = chosen.get(key)
        if prev is None:
            chosen[key] = rec
            continue
        prev_ts = None
        for field in ts_candidates:
            value = prev.get(field)
            if value:
                prev_ts = value
                break
        if rec_ts and prev_ts:
            if rec_ts >= prev_ts:
                chosen[key] = rec
        else:
            chosen[key] = rec
    return chosen


def avg(values: list[float | int | None]):
    nums = [float(v) for v in values if v is not None]
    return round(mean(nums), 4) if nums else None


def abs_delta(a, b):
    if a is None or b is None:
        return None
    return round(abs(float(a) - float(b)), 4)


def build_pair_payload(lab: dict | None, live: dict | None, key: tuple) -> dict:
    local_date, session_name = key
    if lab and live:
        pair_status = "matched"
        lab_direction = lab.get("first5_direction")
        live_direction = live.get("direction")
        payload = {
            "compare_ts": now_local().isoformat(timespec="seconds"),
            "local_date": local_date,
            "session_name": session_name,
            "pair_status": pair_status,
            "lab_feature_id": lab.get("feature_id"),
            "live_record_ts": live.get("record_ts") or live.get("live_ts"),
            "lab_variant_id": lab.get("variant_id"),
            "live_variant_id": live.get("variant_id"),
            "variant_match": lab.get("variant_id") == live.get("variant_id"),
            "lab_direction": lab_direction,
            "live_direction": live_direction,
            "direction_match": lab_direction == live_direction,
            "entry_delta_points": abs_delta(lab.get("entry"), live.get("entry")),
            "sl_delta_points": abs_delta(lab.get("sl"), live.get("sl")),
            "rr_delta": abs_delta(lab.get("rr_planned"), live.get("rr_planned")),
            "lab_source": lab.get("source_csv"),
            "live_source": live.get("source") or live.get("source_csv"),
        }
        return payload

    if lab and not live:
        return {
            "compare_ts": now_local().isoformat(timespec="seconds"),
            "local_date": local_date,
            "session_name": session_name,
            "pair_status": "lab_only",
            "lab_feature_id": lab.get("feature_id"),
            "live_record_ts": None,
            "lab_variant_id": lab.get("variant_id"),
            "live_variant_id": None,
            "variant_match": False,
            "lab_direction": lab.get("first5_direction"),
            "live_direction": None,
            "direction_match": False,
            "entry_delta_points": None,
            "sl_delta_points": None,
            "rr_delta": None,
            "lab_source": lab.get("source_csv"),
            "live_source": None,
        }

    return {
        "compare_ts": now_local().isoformat(timespec="seconds"),
        "local_date": local_date,
        "session_name": session_name,
        "pair_status": "live_only",
        "lab_feature_id": None,
        "live_record_ts": (live or {}).get("record_ts") or (live or {}).get("live_ts"),
        "lab_variant_id": None,
        "live_variant_id": (live or {}).get("variant_id"),
        "variant_match": False,
        "lab_direction": None,
        "live_direction": (live or {}).get("direction"),
        "direction_match": False,
        "entry_delta_points": None,
        "sl_delta_points": None,
        "rr_delta": None,
        "lab_source": None,
        "live_source": (live or {}).get("source") or (live or {}).get("source_csv"),
    }


def compare(session_id: str | None, start_date: str | None, end_date: str | None, live_path: Path) -> dict:
    lab_features_all = filter_records(load_jsonl(FEATURES_JSONL), session_id, start_date, end_date)
    live_records_all = filter_records(load_jsonl(live_path), session_id, start_date, end_date)

    lab_by_key = reduce_latest_by_key(lab_features_all, ("local_date", "session_name"), ("feature_ts",))
    live_by_key = reduce_latest_by_key(live_records_all, ("local_date", "session_name"), ("record_ts", "live_ts"))

    keys = sorted(set(lab_by_key.keys()) | set(live_by_key.keys()))
    pairs = []
    for key in keys:
        pair = build_pair_payload(lab_by_key.get(key), live_by_key.get(key), key)
        pairs.append(pair)
        append_jsonl(COMPARATOR_PAIRS_JSONL, pair)

    matched = [p for p in pairs if p.get("pair_status") == "matched"]
    lab_only = [p for p in pairs if p.get("pair_status") == "lab_only"]
    live_only = [p for p in pairs if p.get("pair_status") == "live_only"]

    report = {
        "compare_ts": now_local().isoformat(timespec="seconds"),
        "session_id": session_id,
        "start_date": start_date,
        "end_date": end_date,
        "live_reference": str(live_path),
        "lab_feature_count": len(lab_features_all),
        "live_record_count": len(live_records_all),
        "matched_count": len(matched),
        "lab_only_count": len(lab_only),
        "live_only_count": len(live_only),
        "variant_match_count": sum(1 for p in matched if p.get("variant_match")),
        "variant_mismatch_count": sum(1 for p in matched if not p.get("variant_match")),
        "direction_match_count": sum(1 for p in matched if p.get("direction_match")),
        "direction_mismatch_count": sum(1 for p in matched if not p.get("direction_match")),
        "avg_entry_delta_points": avg([p.get("entry_delta_points") for p in matched]),
        "avg_sl_delta_points": avg([p.get("sl_delta_points") for p in matched]),
        "avg_rr_delta": avg([p.get("rr_delta") for p in matched]),
        "matched_dates": sorted({p.get("local_date") for p in matched if p.get("local_date")}),
    }
    append_jsonl(COMPARATOR_REPORTS_JSONL, report)
    return report


def status(_: list[str]) -> int:
    payload = {
        "features_jsonl": str(FEATURES_JSONL),
        "trades_jsonl": str(TRADES_JSONL),
        "comparator_reports_jsonl": str(COMPARATOR_REPORTS_JSONL),
        "comparator_pairs_jsonl": str(COMPARATOR_PAIRS_JSONL),
        "sample_live_jsonl": str(SAMPLE_LIVE_JSONL),
        "comparator_reports_count": len(load_jsonl(COMPARATOR_REPORTS_JSONL)),
        "comparator_pairs_count": len(load_jsonl(COMPARATOR_PAIRS_JSONL)),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_live_source(_: list[str]) -> int:
    print(str(SAMPLE_LIVE_JSONL))
    return 0


def compare_live(args: list[str]) -> int:
    live_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_LIVE_JSONL
    session_id = args[1] if len(args) >= 2 and args[1] else None
    start_date = args[2] if len(args) >= 3 and args[2] else None
    end_date = args[3] if len(args) >= 4 and args[3] else None
    report = compare(session_id, start_date, end_date, live_path)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def show_last_report(_: list[str]) -> int:
    reports = load_jsonl(COMPARATOR_REPORTS_JSONL)
    if not reports:
        print(json.dumps({"message": "no comparator report yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(reports[-1], indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-live-source": show_live_source,
    "compare-live": compare_live,
    "show-last-report": show_last_report,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print("Usage: comparator_v1.py status|show-live-source|compare-live [live_jsonl_path] [session_id] [start_date] [end_date]|show-last-report", file=sys.stderr)
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
