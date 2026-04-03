#!/usr/bin/env python3
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


def iso_now_local(tz_name: str) -> str:
    return datetime.now(ZoneInfo(tz_name)).isoformat(timespec="seconds")


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
    if requested is None:
        return enabled_sessions[0]
    for session in enabled_sessions:
        if session.get("session_id") == requested:
            return session
    raise SystemExit(f"Unknown session_id: {requested}")


def choose_variant(profile: dict) -> str | None:
    for variant in profile["strategy"]["variants"]:
        if variant.get("enabled", False):
            return variant.get("variant_id")
    if profile["strategy"]["variants"]:
        return profile["strategy"]["variants"][0].get("variant_id")
    return None


def sample_event() -> dict:
    return {
        "event_id": "evt_sample_xau_001",
        "event_ts": iso_now_local("America/Montreal"),
        "profile_id": "xauusd_dual_stack_v1",
        "mode": "observation",
        "symbol": "XAUUSD",
        "timeframe_context": {
            "trigger_tf": "M1",
            "context_tf": "M5"
        },
        "session_name": "gold_open_18h",
        "local_date": local_now("America/Montreal").date().isoformat(),
        "timezone": "America/Montreal",
        "strategy_id": "xau_session_open_v1",
        "variant_id": "xau_open_sweep_fvg",
        "setup_instance_id": "setup_sample_xau_001",
        "event_type": "setup_classified",
        "decision_state": "observed",
        "direction": "bullish",
        "signal_ts": iso_now_local("America/Montreal"),
        "filters_state": {
            "require_session_window": True,
            "require_complete_open_sequence": True
        },
        "frame_state": {
            "session_allowed": True,
            "max_trades_per_day_ok": True,
            "cooldown_ok": True
        },
        "raw_features": {
            "sweep_detected": True,
            "fvg_detected": True,
            "m5_open_candle_captured": True,
            "m1_first_5_complete": True
        },
        "notes": None
    }


def sample_trade() -> dict:
    return {
        "trade_id": "trd_sample_xau_001",
        "event_id_origin": "evt_sample_xau_001",
        "profile_id": "xauusd_dual_stack_v1",
        "mode": "observation",
        "symbol": "XAUUSD",
        "strategy_id": "xau_session_open_v1",
        "variant_id": "xau_open_sweep_fvg",
        "setup_instance_id": "setup_sample_xau_001",
        "session_name": "gold_open_18h",
        "local_date": local_now("America/Montreal").date().isoformat(),
        "timezone": "America/Montreal",
        "direction": "bullish",
        "entry_ts": iso_now_local("America/Montreal"),
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


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for _ in fh)


def build_event(profile: dict, session: dict, now_dt: datetime, session_is_active: bool) -> dict:
    stamp = now_dt.strftime("%Y%m%d_%H%M%S")
    variant_id = choose_variant(profile)
    session_id = session.get("session_id", "unknown_session")
    event_type = "setup_classified" if session_is_active else "setup_blocked"
    decision_state = "observed" if session_is_active else "blocked_by_frame"
    return {
        "event_id": f"evt_{stamp}_{session_id}",
        "event_ts": now_dt.isoformat(timespec="seconds"),
        "profile_id": profile.get("profile_id") or "xauusd_dual_stack_v1",
        "mode": "observation",
        "symbol": profile["frame"].get("symbol") or "XAUUSD",
        "timeframe_context": {
            "trigger_tf": "M1",
            "context_tf": "M5",
            "runner": "trading_lab_v1"
        },
        "session_name": session_id,
        "local_date": now_dt.date().isoformat(),
        "timezone": profile["frame"].get("timezone") or "America/Montreal",
        "strategy_id": profile["strategy"].get("strategy_id") or "xau_session_open_v1",
        "variant_id": variant_id,
        "setup_instance_id": f"setup_{stamp}_{session_id}",
        "event_type": event_type,
        "decision_state": decision_state,
        "direction": "bullish",
        "signal_ts": now_dt.isoformat(timespec="seconds"),
        "filters_state": {
            "require_session_window": True,
            "require_complete_open_sequence": True
        },
        "frame_state": {
            "session_allowed": session_is_active,
            "max_trades_per_day_ok": True,
            "cooldown_ok": True,
            "session_window_start": session.get("signal_window_start"),
            "session_window_end": session.get("signal_window_end")
        },
        "raw_features": {
            "sweep_detected": session_is_active,
            "fvg_detected": session_is_active,
            "m5_open_candle_captured": session_is_active,
            "m1_first_5_complete": session_is_active
        },
        "notes": None
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


def status(_: list[str]) -> int:
    payload = {
        "module": "trading_lab_v1",
        "base": str(BASE),
        "repo_root": str(REPO_ROOT),
        "profile_exists": PROFILE_PATH.exists(),
        "event_schema_exists": EVENT_SCHEMA_PATH.exists(),
        "trade_schema_exists": TRADE_SCHEMA_PATH.exists(),
        "state_dir": str(STATE_DIR),
        "events_jsonl": str(EVENTS_JSONL),
        "trades_jsonl": str(TRADES_JSONL),
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


def emit_sample_event(_: list[str]) -> int:
    print(json.dumps(sample_event(), indent=2, ensure_ascii=False))
    return 0


def emit_sample_trade(_: list[str]) -> int:
    print(json.dumps(sample_trade(), indent=2, ensure_ascii=False))
    return 0


def materialize_samples(_: list[str]) -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    event_path = STATE_DIR / "sample_event_v1.json"
    trade_path = STATE_DIR / "sample_trade_v1.json"
    event_path.write_text(json.dumps(sample_event(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    trade_path.write_text(json.dumps(sample_trade(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "event_sample": str(event_path),
        "trade_sample": str(trade_path)
    }, indent=2, ensure_ascii=False))
    return 0


def journal_status(_: list[str]) -> int:
    payload = {
        "events_jsonl": str(EVENTS_JSONL),
        "events_count": count_jsonl(EVENTS_JSONL),
        "trades_jsonl": str(TRADES_JSONL),
        "trades_count": count_jsonl(TRADES_JSONL),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def run_once(args: list[str]) -> int:
    requested_session = args[0] if args else None
    profile = load_profile()
    tz_name = profile["frame"].get("timezone") or "America/Montreal"
    now_dt = local_now(tz_name)
    session = choose_session(profile, requested_session)
    is_active = active_now(session, now_dt)
    event = build_event(profile, session, now_dt, is_active)
    append_jsonl(EVENTS_JSONL, event)
    trade_path = None
    if is_active:
        trade = build_trade(event)
        append_jsonl(TRADES_JSONL, trade)
        trade_path = str(TRADES_JSONL)
    payload = {
        "profile_id": profile.get("profile_id"),
        "session_id": session.get("session_id"),
        "active_now": is_active,
        "event_written": str(EVENTS_JSONL),
        "trade_written": trade_path,
        "event_decision_state": event["decision_state"],
        "event_type": event["event_type"]
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


COMMANDS = {
    "status": status,
    "show-profile": show_profile,
    "show-schemas": show_schemas,
    "show-sessions": show_sessions,
    "sample-event": emit_sample_event,
    "sample-trade": emit_sample_trade,
    "materialize-samples": materialize_samples,
    "journal-status": journal_status,
    "run-once": run_once,
}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(
            "Usage: trading_lab_v1.py status|show-profile|show-schemas|show-sessions|sample-event|sample-trade|materialize-samples|journal-status|run-once [session_id]",
            file=sys.stderr,
        )
        return 1
    return fn(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
