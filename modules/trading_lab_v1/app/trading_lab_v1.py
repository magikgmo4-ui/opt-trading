#!/usr/bin/env python3
import csv
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

from modules.strategy.adapter import validate_strategy_id, log_unknown_strategy_id_warning

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
BATCH_REPORTS_JSONL = STATE_DIR / "batch_reports_v1.jsonl"
SAMPLE_MARKET_CSV = BASE / "data" / "sample_xauusd_m1_real_like.csv"
DEFAULT_STRATEGY_ID = "xau_session_open_v1"

log = logging.getLogger("trading_lab_v1")


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


def resolve_strategy_id(profile: dict) -> str:
    strategy_id = profile["strategy"].get("strategy_id") or DEFAULT_STRATEGY_ID
    if not validate_strategy_id(strategy_id):
        source = "fallback" if not profile["strategy"].get("strategy_id") else "profile"
        log_unknown_strategy_id_warning(strategy_id, f"trading_lab_v1:{source}")
    return strategy_id


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


def count_jsonl(path: Path) -> int:
    return len(load_jsonl(path))


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
    return sorted({row["ts"].date().isoformat() for row in rows if in_signal_window(session, row["ts"])})


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
            return {"fvg_detected": True, "fvg_direction": "bullish", "fvg_gap_points": round(c3["low"] - c1["high"], 4), "fvg_window_index": i}
        if c3["high"] < c1["low"]:
            return {"fvg_detected": True, "fvg_direction": "bearish", "fvg_gap_points": round(c1["low"] - c3["high"], 4), "fvg_window_index": i}
    return {"fvg_detected": False, "fvg_direction": None, "fvg_gap_points": 0.0, "fvg_window_index": None}


def detect_sweep(first_five: list[dict]) -> dict:
    first = first_five[0]
    sweep_above = any(c["high"] > first["high"] for c in first_five[1:])
    sweep_below = any(c["low"] < first["low"] for c in first_five[1:])
    return {"sweep_above": sweep_above, "sweep_below": sweep_below, "sweep_detected": sweep_above or sweep_below}


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
        base_payload.update({
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
        })
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
        base_payload.update({
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
        })
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
    entry_candle_ts = first_five[-1]["ts"].isoformat(timespec="seconds")

    base_payload.update({
        "open_candle": open_candle,
        "first5_range_points": first5_range_points,
        "first5_body_delta": first5_body_delta,
        "first5_direction": direction,
        **sweep,
        **fvg,
        "variant_id": variant_id,
        "entry": entry,
        "entry_candle_ts": entry_candle_ts,
        "sl": sl,
        "rr_planned": 2.0,
    })
    return base_payload


def build_market_event(profile: dict, session: dict, features: dict) -> dict:
    observed = bool(features.get("sequence_complete"))
    strategy_id = resolve_strategy_id(profile)
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
            "market_input_source": features["source_csv"],
        },
        "session_name": features["session_name"],
        "local_date": features["local_date"],
        "timezone": features["timezone"],
        "strategy_id": strategy_id,
        "variant_id": features["variant_id"],
        "setup_instance_id": features["feature_id"].replace("feat_", "setup_", 1),
        "event_type": "setup_classified" if observed else "setup_blocked",
        "decision_state": "observed" if observed else "blocked_by_filters",
        "direction": features["first5_direction"],
        "signal_ts": features["feature_ts"],
        "filters_state": {"require_session_window": True, "require_complete_open_sequence": observed},
        "frame_state": {
            "session_allowed": True,
            "max_trades_per_day_ok": True,
            "cooldown_ok": True,
            "session_window_start": session.get("signal_window_start"),
            "session_window_end": session.get("signal_window_end"),
        },
        "raw_features": features,
        "notes": f"market_input:{Path(features['source_csv']).name}",
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
        "tp_plan": {"type": "rr_multiple", "rr_target": 2.0},
        "risk_pct": 1.0,
        "rr_planned": 2.0,
        "result": "open",
        "r_realized": None,
        "mfe": None,
        "mae": None,
        "time_in_trade_seconds": None,
        "execution_state": "virtual_open",
        "exit_reason": None,
        "slippage_points": 0.0,
    }


def build_market_trade(event: dict, features: dict) -> dict:
    trade = build_trade(event)
    trade["entry"] = features["entry"]
    trade["entry_candle_ts"] = features.get("entry_candle_ts")
    trade["sl"] = features["sl"]
    trade["rr_planned"] = features["rr_planned"]
    trade["tp_plan"] = {"type": "rr_multiple", "rr_target": features["rr_planned"]}
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
    return {"features": features, "event": event, "trade": trade, "run_payload": run_payload}


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


def batch_report(args: list[str]) -> int:
    session_id = args[0] if len(args) >= 1 and args[0] else None
    start_date = args[1] if len(args) >= 2 and args[1] else None
    end_date = args[2] if len(args) >= 3 and args[2] else None
    tz_name = load_profile()["frame"].get("timezone") or "America/Montreal"

    features = filter_records(load_jsonl(FEATURES_JSONL), session_id, start_date, end_date)
    trades = filter_records(load_jsonl(TRADES_JSONL), session_id, start_date, end_date)
    market_runs = filter_records(load_jsonl(MARKET_RUNS_JSONL), session_id, start_date, end_date)
    batch_runs = filter_records(load_jsonl(BATCH_RUNS_JSONL), session_id, start_date, end_date)

    report = {
        "report_ts": local_now(tz_name).isoformat(timespec="seconds"),
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
        "win_count": sum(1 for t in trades if t.get("result") == "win"),
        "loss_count": sum(1 for t in trades if t.get("result") == "loss"),
        "timeout_count": sum(1 for t in trades if t.get("result") == "timeout"),
        "avg_r_realized": avg([t.get("r_realized") for t in trades]),
    }
    append_jsonl(BATCH_REPORTS_JSONL, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def apply_outcomes(args: list[str]) -> int:
    """Resolve exit outcomes for all open trades using post-entry candles from a CSV."""
    from modules.trading_lab_v1.app.exit_outcome_v1 import resolve_exit_outcome, get_post_entry_candles

    csv_path = Path(args[0]) if args else SAMPLE_MARKET_CSV
    profile = load_profile()
    tz_name = profile["frame"].get("timezone") or "America/Montreal"

    trades = load_jsonl(TRADES_JSONL)
    if not trades:
        print(json.dumps({"message": "no trades found", "resolved": 0}, indent=2))
        return 0

    all_rows = load_market_csv(csv_path, tz_name)
    resolved = 0
    updated: list[dict] = []

    for trade in trades:
        if trade.get("execution_state") != "virtual_open":
            updated.append(trade)
            continue
        entry = trade.get("entry")
        sl = trade.get("sl")
        rr = trade.get("rr_planned", 2.0)
        direction = trade.get("direction", "bullish")
        entry_candle_ts = trade.get("entry_candle_ts") or trade.get("entry_ts")
        if entry is None or sl is None or entry_candle_ts is None:
            updated.append(trade)
            continue
        post_candles = get_post_entry_candles(all_rows, entry_candle_ts, tz_name)
        outcome = resolve_exit_outcome(entry, sl, rr, direction, post_candles)
        trade.update({
            "result": outcome["result"],
            "r_realized": outcome["r_realized"],
            "exit_price": outcome["exit_price"],
            "exit_ts": outcome["exit_ts"],
            "bars_held": outcome["bars_held"],
            "outcome_reason": outcome["outcome_reason"],
            "tp": outcome["tp"],
            "execution_state": "virtual_closed" if outcome["result"] != "timeout" else "virtual_open",
        })
        resolved += 1
        updated.append(trade)

    TRADES_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with TRADES_JSONL.open("w", encoding="utf-8") as fh:
        for t in updated:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")

    r_vals = [t["r_realized"] for t in updated if t.get("r_realized") is not None]
    print(json.dumps({
        "resolved": resolved,
        "total": len(trades),
        "wins": sum(1 for t in updated if t.get("result") == "win"),
        "losses": sum(1 for t in updated if t.get("result") == "loss"),
        "timeouts": sum(1 for t in updated if t.get("result") == "timeout"),
        "avg_r_realized": round(sum(r_vals) / len(r_vals), 4) if r_vals else None,
    }, indent=2))
    return 0


def show_last_batch_report(_: list[str]) -> int:
    reports = load_jsonl(BATCH_REPORTS_JSONL)
    if not reports:
        print(json.dumps({"message": "no batch report yet"}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(reports[-1], indent=2, ensure_ascii=False))
    return 0


def _sweep_data_path() -> Path:
    return REPO_ROOT / "modules" / "trading_lab_v1" / "data" / "btcusd_coinm_backtest_data.jsonl"


def param_sweep_run(args: list[str]) -> int:
    config_path = Path(args[0]) if len(args) > 0 else None
    data_path = Path(args[1]) if len(args) > 1 else _sweep_data_path()
    if config_path is None:
        print("Usage: param-sweep-run <config_json> [data_jsonl]", file=sys.stderr)
        return 1
    from . import param_sweep_engine_v1 as eng
    from . import param_sweep_classify_v1 as clf
    config = json.loads(config_path.read_text(encoding="utf-8"))
    candles = eng.load_jsonl(data_path)
    if not candles:
        print(json.dumps({"error": "no candles loaded"}, indent=2, ensure_ascii=False))
        return 1
    result = eng.simulate_run(config, candles)
    result = clf.classify_run(result)
    eng.append_jsonl(eng.RUNS_SUMMARY_JSONL, result)
    print(json.dumps({k: result[k] for k in (
        "run_id", "config_hash", "delta_btc_net", "delta_btc_pct",
        "net_btc_final", "simulation_stop_reason", "classification_primary",
    )}, indent=2, ensure_ascii=False))
    return 0


def param_sweep_batch(args: list[str]) -> int:
    if len(args) < 1:
        print("Usage: param-sweep-batch <campaign_config_json>", file=sys.stderr)
        return 1
    import time
    from . import param_sweep_engine_v1 as eng
    from . import param_sweep_config_v1 as gen
    from . import param_sweep_classify_v1 as clf

    campaign = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    data_path = Path(campaign.get("data_path", str(_sweep_data_path())))
    count = campaign.get("count", 100)
    method = campaign.get("method", "random")
    seed = campaign.get("seed", 0)
    space = campaign.get("space", {})
    configs = gen.generate_configs(space, count, method, seed)
    candles = eng.load_jsonl(data_path)

    t0 = time.time()
    for i, cfg in enumerate(configs):
        cfg["config_hash"] = gen.config_hash(cfg)
        result = eng.simulate_run(cfg, candles)
        result = clf.classify_run(result)
        result["batch_id"] = campaign.get("batch_id", "")
        eng.append_jsonl(eng.RUNS_SUMMARY_JSONL, result)
        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (count - i - 1) / rate if rate > 0 else 0
            print(f"[{i+1}/{count}] rate={rate:.0f}r/s ETA={eta:.0f}s")
    elapsed = time.time() - t0
    print(f"Done: {count} runs in {elapsed:.1f}s ({count/elapsed:.0f} r/s)")
    return 0


def param_sweep_report(args: list[str]) -> int:
    from . import param_sweep_engine_v1 as eng
    from . import param_sweep_rank_v1 as rank
    runs = eng.load_jsonl(eng.RUNS_SUMMARY_JSONL)
    if not runs:
        print("No sweep runs found.")
        return 1
    best = rank.rank_runs(runs, "raw_best")
    worst = rank.rank_runs(runs, "raw_worst")
    md_best = rank.format_top_markdown(best, 100, "Top 100 — Raw Best (delta_btc_net)")
    md_worst = rank.format_top_markdown(worst, 100, "Top 100 — Raw Worst (delta_btc_net)")
    out_dir = eng.STATE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "param_sweep_top_best.md").write_text(md_best, encoding="utf-8")
    (out_dir / "param_sweep_top_worst.md").write_text(md_worst, encoding="utf-8")
    print(md_best[:3000])
    return 0


def param_sweep_export(args: list[str]) -> int:
    import csv
    from . import param_sweep_engine_v1 as eng
    runs = eng.load_jsonl(eng.RUNS_SUMMARY_JSONL)
    if not runs:
        print("No sweep runs found.")
        return 1
    csv_path = eng.STATE_DIR / "param_sweep_runs_summary.csv"
    cols = [
        "run_id", "config_hash", "net_btc_initial", "net_btc_final",
        "delta_btc_net", "delta_btc_pct", "max_drawdown_btc",
        "liquidation_count", "margin_breach_count", "funding_paid_btc",
        "funding_received_btc", "fees_btc", "spot_btc_final",
        "margin_btc_final", "realized_pnl_btc", "unrealized_pnl_btc",
        "classification_primary", "reject_reasons",
    ]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in runs:
            r["reject_reasons"] = ";".join(r.get("reject_reasons", []))
            w.writerow(r)
    print(f"Exported {len(runs)} runs to {csv_path}")
    return 0


COMMANDS = {
    "batch-report": batch_report,
    "apply-outcomes": apply_outcomes,
    "show-last-batch-report": show_last_batch_report,
    "param-sweep-run": param_sweep_run,
    "param-sweep-batch": param_sweep_batch,
    "param-sweep-report": param_sweep_report,
    "param-sweep-export": param_sweep_export,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(
            "Usage: trading_lab_v1.py status|show-profile|show-schemas|show-market-source|show-sessions|show-batch-dates [csv_path] [session_id]|sample-event|sample-trade|materialize-samples|journal-status|run-once [session_id]|extract-features [csv_path] [session_id] [local_date]|analyze-market-input [csv_path] [session_id] [local_date]|batch-run [csv_path] [session_id] [start_date] [end_date]|batch-report [session_id] [start_date] [end_date]|show-last-batch-report|param-sweep-run <config_json> [data_jsonl]|param-sweep-batch <campaign_json>|param-sweep-report|param-sweep-export",
            file=sys.stderr,
        )
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
