#!/usr/bin/env python3
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
PROFILE_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "xauusd_dual_stack_v1.profile.yaml"
EVENT_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_event_v1.schema.json"
TRADE_SCHEMA_PATH = REPO_ROOT / "docs" / "ot" / "trading" / "schemas" / "trading_trade_v1.schema.json"
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"
EVENTS_JSONL = STATE_DIR / "events_v1.jsonl"
TRADES_JSONL = STATE_DIR / "trades_v1.jsonl"
MARKET_RUNS_JSONL = STATE_DIR / "market_runs_v1.jsonl"
FEATURES_JSONL = STATE_DIR / "features_v1.jsonl"
BATCH_RUNS_JSONL = STATE_DIR / "batch_runs_v1.jsonl"
SAMPLE_MARKET_CSV = BASE / "data" / "sample_xauusd_m1.csv"


def parse_scalar(raw: str):
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def parse_kv(text: str):
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def load_profile() -> dict:
    text = PROFILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    data = {
        "version": None,
        "profile_id": None,
        "frame": {"timezone": None, "symbol": None, "sessions": []},
        "strategy": {"strategy_id": None, "variants": []},
    }
    section = None
    subsection = None
    current_session = None
    current_variant = None

    for raw in lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 0 and stripped.endswith(":"):
            if current_session is not None:
                data["frame"]["sessions"].append(current_session)
                current_session = None
            if current_variant is not None:
                data["strategy"]["variants"].append(current_variant)
                current_variant = None
            section = stripped[:-1]
            subsection = None
            continue

        if indent == 0 and ":" in stripped and not stripped.endswith(":"):
            key, value = parse_kv(stripped)
            if key in {"version", "profile_id"}:
                data[key] = parse_scalar(value)
            continue

        if indent == 2 and stripped.endswith(":"):
            if current_session is not None:
                data["frame"]["sessions"].append(current_session)
                current_session = None
            if current_variant is not None:
                data["strategy"]["variants"].append(current_variant)
                current_variant = None
            subsection = stripped[:-1]
            continue

        if section == "frame" and subsection is None and indent == 2 and ":" in stripped and not stripped.endswith(":"):
            key, value = parse_kv(stripped)
            if key in {"timezone", "symbol"}:
                data["frame"][key] = parse_scalar(value)
            continue

        if section == "strategy" and subsection is None and indent == 2 and ":" in stripped and not stripped.endswith(":"):
            key, value = parse_kv(stripped)
            if key == "strategy_id":
                data["strategy"][key] = parse_scalar(value)
            continue

        if section == "frame" and subsection == "sessions":
            if indent == 4 and stripped.startswith("- "):
                if current_session is not None:
                    data["frame"]["sessions"].append(current_session)
                current_session = {}
                item = stripped[2:]
                if ":" in item:
                    key, value = parse_kv(item)
                    current_session[key] = parse_scalar(value)
                continue
            if indent == 6 and current_session is not None and ":" in stripped and not stripped.endswith(":"):
                key, value = parse_kv(stripped)
                current_session[key] = parse_scalar(value)
                continue

        if section == "strategy" and subsection == "variants":
            if indent == 4 and stripped.startswith("- "):
                if current_variant is not None:
                    data["strategy"]["variants"].append(current_variant)
                current_variant = {}
                item = stripped[2:]
                if ":" in item:
                    key, value = parse_kv(item)
                    current_variant[key] = parse_scalar(value)
                continue
            if indent == 6 and current_variant is not None and ":" in stripped and not stripped.endswith(":"):
                key, value = parse_kv(stripped)
                current_variant[key] = parse_scalar(value)
                continue

    if current_session is not None:
        data["frame"]["sessions"].append(current_session)
    if current_variant is not None:
        data["strategy"]["variants"].append(current_variant)
    return data


def local_now(tz_name: str) -> datetime:
    return datetime.now(ZoneInfo(tz_name))


def to_minutes(hhmm: str) -> int:
    hh, mm = hhmm.split(":", 1)
    return int(hh) * 60 + int(mm)


def active_now(session: dict, now_dt: datetime) -> bool:
    if not session.get("enabled", False):
        return False
    current = now_dt.hour * 60 + now_dt.minute
    start = to_minutes(session.get("signal_window_start", session.get("start_local", "00:00")))
    end = to_minutes(session.get("signal_window_end", session.get("end_local", "23:59")))
    return start <= current <= end


def choose_session(profile: dict, requested: str | None) -> dict:
    enabled_sessions = [s for s in profile["frame"]["sessions"] if s.get("enabled", False)]
    if not enabled_sessions:
        raise SystemExit("No enabled sessions found in profile")
    if requested is None or requested == "":
        return enabled_sessions[0]
    for session in enabled_sessions:
        if session.get("session_id") == requested:
            return session
    raise SystemExit(f"Unknown session_id: {requested}")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for _ in fh)


def parse_csv_timestamp(raw: str, tz_name: str) -> datetime:
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(tz_name))
    return dt.astimezone(ZoneInfo(tz_name))


def load_market_csv(path: Path, tz_name: str) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(
                {
                    "ts": parse_csv_timestamp(row["timestamp"], tz_name),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row.get("volume", 0.0)),
                }
            )
    rows.sort(key=lambda x: x["ts"])
    return rows


def in_signal_window(session: dict, dt: datetime) -> bool:
    current = dt.hour * 60 + dt.minute
    start = to_minutes(session.get("signal_window_start", session.get("start_local", "00:00")))
    end = to_minutes(session.get("signal_window_end", session.get("end_local", "23:59")))
    return start <= current <= end


def available_dates_for_session(rows: list[dict], session: dict) -> list[str]:
    dates = sorted({row["ts"].date().isoformat() for row in rows if in_signal_window(session, row["ts"])})
    return dates


def select_session_rows(rows: list[dict], session: dict, target_date: str | None) -> tuple[list[dict], str | None]:
    candidates = [row for row in rows if in_signal_window(session, row["ts"])]
    if not candidates:
        return [], None
    chosen_date = target_date or candidates[0]["ts"].date().isoformat()
    selected = [row for row in candidates if row["ts"].date().isoformat() == chosen_date]
    return selected, chosen_date


def detect_fvg(first_five: list[dict]) -> dict:
    for i in range(len(first_five) - 2):
        c1 = first_five[i]
        c3 = first_five[i + 2]
        if c3["low"] > c1["high"]:
            return {
                "fvg_detected": True,
                "fvg_direction": "bullish",
                "fvg_gap_points": round(c3["low"] - c1["high"], 4),
                "fvg_window_index": i,
            }
        if c3["high"] < c1["low"]:
            return {
                "fvg_detected": True,
                "fvg_direction": "bearish",
                "fvg_gap_points": round(c1["low"] - c3["high"], 4),
                "fvg_window_index": i,
            }
    return {
        "fvg_detected": False,
        "fvg_direction": None,
        "fvg_gap_points": 0.0,
        "fvg_window_index": None,
    }


def detect_sweep(first_five: list[dict]) -> dict:
    first = first_five[0]
    sweep_above = any(c["high"] > first["high"] for c in first_five[1:])
    sweep_below = any(c["low"] < first["low"] for c in first_five[1:])
    return {
        "sweep_above": sweep_above,
        "sweep_below": sweep_below,
        "sweep_detected": sweep_above or sweep_below,
    }


def choose_variant_from_features(sweep_detected: bool, fvg_detected: bool) -> str:
    if sweep_detected and fvg_detected:
        return "xau_open_sweep_fvg"
    if (not sweep_detected) and fvg_detected:
        return "xau_open_no_sweep_fvg"
    if sweep_detected and (not fvg_detected):
        return "xau_open_sweep_no_fvg"
    return "xau_open_no_sweep_no_fvg"


def choose_direction(first_five: list[dict], fvg_direction: str | None) -> str:
    if fvg_direction in {"bullish", "bearish"}:
        return fvg_direction
    if first_five[-1]["close"] > first_five[0]["open"]:
        return "bullish"
    if first_five[-1]["close"] < first_five[0]["open"]:
        return "bearish"
    return "neutral"


def build_feature_payload(profile: dict, session: dict, rows: list[dict], analysis_date: str, source_path: Path) -> dict:
    tz_name = profile["frame"].get("timezone") or "America/Montreal"
    now_dt = local_now(tz_name)
    stamp = now_dt.strftime("%Y%m%d_%H%M%S")
    first_five = rows[:5]
    sequence_complete = len(first_five) >= 5
    session_id = session.get("session_id", "unknown_session")

    base_payload = {
        "feature_id": f"feat_{stamp}_{session_id}",
        "feature_ts": now_dt.isoformat(timespec="seconds"),
        "profile_id": profile.get("profile_id") or "xauusd_dual_stack_v1",
        "symbol": profile["frame"].get("symbol") or "XAUUSD",
        "session_name": session_id,
        "local_date": analysis_date,
        "timezone": tz_name,
        "source_csv": str(source_path),
        "sequence_complete": sequence_complete,
        "candle_count": len(rows),
    }

    if not rows:
        base_payload.update(
            {
                "open_candle": None,
                "first5_range_points": None,
                "first5_body_delta": None,
                "first5_direction": "neutral",
                "sweep_detected": False,
                "sweep_above": False,
                "sweep_below": False,
                "fvg_detected": False,
                "fvg_direction": None,
                "fvg_gap_points": 0.0,
                "variant_id": None,
                "entry": None,
                "sl": None,
                "rr_planned": 2.0,
            }
        )
        return base_payload

    first = first_five[0] if first_five else rows[0]
    open_candle = {
        "ts": first["ts"].isoformat(timespec="seconds"),
        "open": first["open"],
        "high": first["high"],
        "low": first["low"],
        "close": first["close"],
        "range_points": round(first["high"] - first["low"], 4),
        "body_points": round(abs(first["close"] - first["open"]), 4),
        "direction": "bullish" if first["close"] > first["open"] else "bearish" if first["close"] < first["open"] else "neutral",
    }

    if not sequence_complete:
        base_payload.update(
            {
                "open_candle": open_candle,
                "first5_range_points": None,
                "first5_body_delta": None,
                "first5_direction": "neutral",
                "sweep_detected": False,
                "sweep_above": False,
                "sweep_below": False,
                "fvg_detected": False,
                "fvg_direction": None,
                "fvg_gap_points": 0.0,
                "variant_id": None,
                "entry": None,
                "sl": None,
                "rr_planned": 2.0,
            }
        )
        return base_payload

    sweep = detect_sweep(first_five)
    fvg = detect_fvg(first_five)
    direction = choose_direction(first_five, fvg["fvg_direction"])
    variant_id = choose_variant_from_features(sweep["sweep_detected"], fvg["fvg_detected"])

    first5_high = max(c["high"] for c in first_five)
    first5_low = min(c["low"] for c in first_five)
    first5_range_points = round(first5_high - first5_low, 4)
    first5_body_delta = round(first_five[-1]["close"] - first_five[0]["open"], 4)

    entry = round(first_five[-1]["close"], 4)
    sl = round(first5_low if direction != "bearish" else first5_high, 4)

    base_payload.update(
        {
            "open_candle": open_candle,
            "first5_range_points": first5_range_points,
            "first5_body_delta": first5_body_delta,
            "first5_direction": direction,
            **sweep,
            **fvg,
            "variant_id": variant_id,
            "entry": entry,
            "sl": sl,
            "rr_planned": 2.0,
        }
    )
    return base_payload


def build_market_event(profile: dict, session: dict, features: dict) -> dict:
    observed = bool(features.get("sequence_complete"))
    return {
        "event_id": features["feature_id"].replace("feat_", "evt_market_", 1),
        "event_ts": features["feature_ts"],
        "profile_id": features["profile_id"],
        "mode": "observation",
        "symbol": features["symbol"],
        "timeframe_context": {
            "trigger_tf": "M1",
            "context_tf": "M5",
            "runner": "trading_lab_v1",
            "market_input_source": features["source_csv"]
        },
        "session_name": features["session_name"],
        "local_date": features["local_date"],
        "timezone": features["timezone"],
        "strategy_id": profile["strategy"].get("strategy_id") or "xau_session_open_v1",
        "variant_id": features["variant_id"],
        "setup_instance_id": features["feature_id"].replace("feat_", "setup_", 1),
        "event_type": "setup_classified" if observed else "setup_blocked",
        "decision_state": "observed" if observed else "blocked_by_filters",
        "direction": features["first5_direction"],
        "signal_ts": features["feature_ts"],
        "filters_state": {
            "require_session_window": True,
            "require_complete_open_sequence": observed
        },
        "frame_state": {
            "session_allowed": True,
            "max_trades_per_day_ok": True,
            "cooldown_ok": True,
            "session_window_start": session.get("signal_window_start"),
            "session_window_end": session.get("signal_window_end")
        },
        "raw_features": features,
        "notes": f"market_input:{Path(features['source_csv']).name}"
    }


def build_trade(event: dict) -> dict:
    trade_id = event["event_id"].replace("evt_", "trd_", 1)
    return {
        "trade_id": trade_id,
        "event_id_origin": event["event_id"],
        "profile_id": event["profile_id"],
        "mode": event["mode"],
        "symbol": event["symbol"],
        "strategy_id": event["strategy_id"],
        "variant_id": event["variant_id"] or "unknown_variant",
        "setup_instance_id": event["setup_instance_id"] or trade_id,
        "session_name": event["session_name"],
        "local_date": event["local_date"],
        "timezone": event["timezone"],
        "direction": event["direction"] or "neutral",
        "entry_ts": event["signal_ts"],
        "exit_ts": None,
        "entry": 3200.0,
        "sl": 3195.0,
        "tp_plan": {
            "type": "rr_multiple",
            "rr_target": 2.0
        },
        "risk_pct": 1.0,
        "rr_planned": 2.0,
        "result": "open",
        "r_realized": None,
        "mfe": None,
        "mae": None,
        "time_in_trade_seconds": None,
        "execution_state": "virtual_open",
        "exit_reason": None,
        "slippage_points": 0.0
    }


def build_market_trade(event: dict, features: dict) -> dict:
    trade = build_trade(event)
    trade["entry"] = features["entry"]
    trade["sl"] = features["sl"]
    trade["rr_planned"] = features["rr_planned"]
    trade["tp_plan"] = {
        "type": "rr_multiple",
        "rr_target": features["rr_planned"]
    }
    return trade


def process_market_run(profile: dict, session: dict, csv_path: Path, analysis_date: str | None) -> dict:
    tz_name = profile["frame"].get("timezone") or "America/Montreal"
    rows = load_market_csv(csv_path, tz_name)
    selected_rows, chosen_date = select_session_rows(rows, session, analysis_date)
    effective_date = chosen_date or analysis_date or local_now(tz_name).date().isoformat()
    features = build_feature_payload(profile, session, selected_rows, effective_date, csv_path)
    append_jsonl(FEATURES_JSONL, features)
    event = build_market_event(profile, session, features)
    append_jsonl(EVENTS_JSONL, event)
    trade_written = None
    trade = None
    if features["sequence_complete"]:
        trade = build_market_trade(event, features)
        append_jsonl(TRADES_JSONL, trade)
        trade_written = str(TRADES_JSONL)
    run_payload = {
        "run_ts": local_now(tz_name).isoformat(timespec="seconds"),
        "source_csv": str(csv_path),
        "session_id": session.get("session_id"),
        "analysis_date": effective_date,
        "selected_rows": len(selected_rows),
        "sequence_complete": features["sequence_complete"],
        "variant_id": features["variant_id"],
        "direction": features["first5_direction"],
        "feature_id": features["feature_id"],
        "event_id": event["event_id"],
        "trade_written": trade_written,
    }
    append_jsonl(MARKET_RUNS_JSONL, run_payload)
    return {
        "features": features,
        "event": event,
        "trade": trade,
        "run_payload": run_payload,
    }


def status(_: list[str]) -> int:
    payload = {
        "module": "trading_lab_v1",
        "base": str(BASE),
        "repo_root": str(REPO_ROOT),
        "profile_exists": PROFILE_PATH.exists(),
        "event_schema_exists": EVENT_SCHEMA_PATH.exists(),
        "trade_schema_exists": TRADE_SCHEMA_PATH.exists(),
        "sample_market_csv_exists": SAMPLE_MARKET_CSV.exists(),
        "state_dir": str(STATE_DIR),
        "events_jsonl": str(EVENTS_JSONL),
        "trades_jsonl": str(TRADES_JSONL),
        "market_runs_jsonl": str(MARKET_RUNS_JSONL),
        "features_jsonl": str(FEATURES_JSONL),
        "batch_runs_jsonl": str(BATCH_RUNS_JSONL),
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


def show_market_source(_: list[str]) -> int:
    print(str(SAMPLE_MARKET_CSV))
    return 0


def show_sessions(_: list[str]) -> int:
    profile = load_profile()
    tz_name = profile["frame"].get("timezone") or "America/Montreal"
    now_dt = local_now(tz_name)
    payload = []
    for session in profile["frame"]["sessions"]:
        payload.append({
            "session_id": session.get("session_id"),
            "enabled": session.get("enabled", False),
            "start_local": session.get("start_local"),
            "end_local": session.get("end_local"),
            "signal_window_start": session.get("signal_window_start"),
            "signal_window_end": session.get("signal_window_end"),
            "active_now": active_now(session, now_dt),
        })
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def show_batch_dates(args: list[str]) -> int:
    csv_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_MARKET_CSV
    requested_session = args[1] if len(args) >= 2 and args[1] else None
    profile = load_profile()
    session = choose_session(profile, requested_session)
    rows = load_market_csv(csv_path, profile["frame"].get("timezone") or "America/Montreal")
    payload = {
        "source_csv": str(csv_path),
        "session_id": session.get("session_id"),
        "dates": available_dates_for_session(rows, session),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def emit_sample_event(_: list[str]) -> int:
    print(json.dumps({
        "sample": "event",
        "feature_engine": "use extract-features / analyze-market-input / batch-run for market-based output"
    }, indent=2, ensure_ascii=False))
    return 0


def emit_sample_trade(_: list[str]) -> int:
    print(json.dumps({
        "sample": "trade",
        "feature_engine": "use analyze-market-input / batch-run for market-based output"
    }, indent=2, ensure_ascii=False))
    return 0


def materialize_samples(_: list[str]) -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    feature_path = STATE_DIR / "sample_features_v1.json"
    trade_path = STATE_DIR / "sample_trade_v1.json"
    profile = load_profile()
    session = choose_session(profile, None)
    result = process_market_run(profile, session, SAMPLE_MARKET_CSV, None)
    feature_path.write_text(json.dumps(result["features"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if result["trade"] is not None:
        trade_path.write_text(json.dumps(result["trade"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "feature_sample": str(feature_path),
        "trade_sample": str(trade_path)
    }, indent=2, ensure_ascii=False))
    return 0


def journal_status(_: list[str]) -> int:
    payload = {
        "events_jsonl": str(EVENTS_JSONL),
        "events_count": count_jsonl(EVENTS_JSONL),
        "trades_jsonl": str(TRADES_JSONL),
        "trades_count": count_jsonl(TRADES_JSONL),
        "market_runs_jsonl": str(MARKET_RUNS_JSONL),
        "market_runs_count": count_jsonl(MARKET_RUNS_JSONL),
        "features_jsonl": str(FEATURES_JSONL),
        "features_count": count_jsonl(FEATURES_JSONL),
        "batch_runs_jsonl": str(BATCH_RUNS_JSONL),
        "batch_runs_count": count_jsonl(BATCH_RUNS_JSONL),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def run_once(args: list[str]) -> int:
    requested_session = args[0] if args else None
    profile = load_profile()
    session = choose_session(profile, requested_session)
    result = process_market_run(profile, session, SAMPLE_MARKET_CSV, None)
    payload = {
        "profile_id": result["features"]["profile_id"],
        "session_id": session.get("session_id"),
        "feature_written": str(FEATURES_JSONL),
        "event_written": str(EVENTS_JSONL),
        "trade_written": str(TRADES_JSONL) if result["trade"] is not None else None,
        "event_decision_state": result["event"]["decision_state"],
        "event_type": result["event"]["event_type"],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def extract_features(args: list[str]) -> int:
    csv_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_MARKET_CSV
    requested_session = args[1] if len(args) >= 2 and args[1] else None
    target_date = args[2] if len(args) >= 3 and args[2] else None
    profile = load_profile()
    session = choose_session(profile, requested_session)
    rows = load_market_csv(csv_path, profile["frame"].get("timezone") or "America/Montreal")
    selected_rows, chosen_date = select_session_rows(rows, session, target_date)
    analysis_date = chosen_date or target_date or local_now(profile["frame"].get("timezone") or "America/Montreal").date().isoformat()
    features = build_feature_payload(profile, session, selected_rows, analysis_date, csv_path)
    print(json.dumps(features, indent=2, ensure_ascii=False))
    return 0


def analyze_market_input(args: list[str]) -> int:
    csv_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_MARKET_CSV
    requested_session = args[1] if len(args) >= 2 and args[1] else None
    target_date = args[2] if len(args) >= 3 and args[2] else None
    profile = load_profile()
    session = choose_session(profile, requested_session)
    result = process_market_run(profile, session, csv_path, target_date)
    print(json.dumps(result["run_payload"], indent=2, ensure_ascii=False))
    return 0


def batch_run(args: list[str]) -> int:
    csv_path = Path(args[0]).expanduser() if len(args) >= 1 and args[0] else SAMPLE_MARKET_CSV
    requested_session = args[1] if len(args) >= 2 and args[1] else None
    start_date = args[2] if len(args) >= 3 and args[2] else None
    end_date = args[3] if len(args) >= 4 and args[3] else None

    profile = load_profile()
    session = choose_session(profile, requested_session)
    rows = load_market_csv(csv_path, profile["frame"].get("timezone") or "America/Montreal")
    all_dates = available_dates_for_session(rows, session)
    dates = [d for d in all_dates if (start_date is None or d >= start_date) and (end_date is None or d <= end_date)]

    runs = []
    variants: dict[str, int] = {}
    complete_count = 0
    trade_count = 0
    for day in dates:
        result = process_market_run(profile, session, csv_path, day)
        run_payload = result["run_payload"]
        runs.append(run_payload)
        if result["features"]["sequence_complete"]:
            complete_count += 1
        if result["trade"] is not None:
            trade_count += 1
        variant = result["features"]["variant_id"] or "none"
        variants[variant] = variants.get(variant, 0) + 1

    summary = {
        "batch_ts": local_now(profile["frame"].get("timezone") or "America/Montreal").isoformat(timespec="seconds"),
        "profile_id": profile.get("profile_id"),
        "source_csv": str(csv_path),
        "session_id": session.get("session_id"),
        "start_date": start_date,
        "end_date": end_date,
        "processed_dates": dates,
        "run_count": len(runs),
        "sequence_complete_count": complete_count,
        "trade_count": trade_count,
        "variants": variants,
    }
    append_jsonl(BATCH_RUNS_JSONL, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-profile": show_profile,
    "show-schemas": show_schemas,
    "show-market-source": show_market_source,
    "show-sessions": show_sessions,
    "show-batch-dates": show_batch_dates,
    "sample-event": emit_sample_event,
    "sample-trade": emit_sample_trade,
    "materialize-samples": materialize_samples,
    "journal-status": journal_status,
    "run-once": run_once,
    "extract-features": extract_features,
    "analyze-market-input": analyze_market_input,
    "batch-run": batch_run,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(
            "Usage: trading_lab_v1.py status|show-profile|show-schemas|show-market-source|show-sessions|show-batch-dates [csv_path] [session_id]|sample-event|sample-trade|materialize-samples|journal-status|run-once [session_id]|extract-features [csv_path] [session_id] [local_date]|analyze-market-input [csv_path] [session_id] [local_date]|batch-run [csv_path] [session_id] [start_date] [end_date]",
            file=sys.stderr,
        )
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
