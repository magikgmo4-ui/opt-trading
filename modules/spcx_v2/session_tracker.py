"""SPCX V2 — Session tracker: counts paper sessions, validates setups."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.spcx_v2.config import OUTPUT_DIR, PROJECT_ROOT
from modules.spcx_v2.paper_logger import list_candidates, get_summary, _read_jsonl
from modules.spcx_v2.perf_calculator import compute_stats_by_setup, compute_stats_by_grade
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.session_tracker")

SESSION_FILE = PROJECT_ROOT / "data" / "ipo" / "spacex" / "session_counter.json"
GRADUATION_FILE = PROJECT_ROOT / "data" / "ipo" / "spacex" / "graduation.json"
TARGET_SESSIONS = 20
INTERIM_INTERVAL = 5

VALIDATION_THRESHOLDS = {
    "IPO_ORB_5M": {"min_trades": 5, "min_winrate": 45, "min_expectancy_r": 0, "min_profit_factor": 1.1},
    "IPO_ORB_15M": {"min_trades": 5, "min_winrate": 45, "min_expectancy_r": 0, "min_profit_factor": 1.1},
    "IPO_ORB_30M": {"min_trades": 3, "min_winrate": 40, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "VWAP_HOLD_LONG": {"min_trades": 3, "min_winrate": 40, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "VWAP_RECLAIM": {"min_trades": 3, "min_winrate": 40, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "IPO_PRICE_RECLAIM": {"min_trades": 3, "min_winrate": 40, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "GAP_AND_GO": {"min_trades": 3, "min_winrate": 40, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "FVG_BULLISH_RECLAIM": {"min_trades": 2, "min_winrate": 35, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "BOS_CONTINUATION": {"min_trades": 2, "min_winrate": 35, "min_expectancy_r": 0, "min_profit_factor": 1.0},
    "CHOCH_REVERSAL": {"min_trades": 2, "min_winrate": 35, "min_expectancy_r": 0, "min_profit_factor": 1.0},
}  # other setups get default threshold

DEFAULT_THRESHOLD = {"min_trades": 2, "min_winrate": 35, "min_expectancy_r": 0, "min_profit_factor": 1.0}


def _ensure_session_dir():
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)


def bump_session() -> int:
    _ensure_session_dir()
    if SESSION_FILE.exists():
        try:
            data = json.loads(SESSION_FILE.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}
    else:
        data = {}

    current = data.get("count", 0)
    current += 1
    data["count"] = current
    data["bumped_at"] = datetime.now(timezone.utc).isoformat()
    SESSION_FILE.write_text(json.dumps(data, indent=2))

    if current % INTERIM_INTERVAL == 0:
        logger.info("SPCX V2 session %d/%d — generating interim report", current, TARGET_SESSIONS)
        _write_interim_report(current)

    if current == TARGET_SESSIONS:
        logger.info("SPCX V2 session %d/%d — final graduation", current, TARGET_SESSIONS)

    return current


def get_session_count() -> int:
    if not SESSION_FILE.exists():
        return 0
    try:
        data = json.loads(SESSION_FILE.read_text())
        return data.get("count", 0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0


def is_test_complete() -> bool:
    return get_session_count() >= TARGET_SESSIONS


def validate_setup(setup_type: str, candidates: list[dict]) -> dict:
    stats = compute_stats_by_setup(candidates)
    setup_stats = stats.get(setup_type, {})
    thresholds = VALIDATION_THRESHOLDS.get(setup_type, DEFAULT_THRESHOLD)

    trades = setup_stats.get("total_trades", 0)
    winrate = setup_stats.get("winrate", 0)
    exp_r = setup_stats.get("expectancy_R", 0)
    pf = setup_stats.get("profit_factor", 0) or 0

    enough_trades = trades >= thresholds["min_trades"]
    wr_ok = winrate >= thresholds["min_winrate"]
    exp_ok = exp_r > thresholds["min_expectancy_r"]
    pf_ok = pf >= thresholds["min_profit_factor"]

    passed = enough_trades and wr_ok and exp_ok and pf_ok

    return {
        "setup_type": setup_type,
        "passed": passed,
        "metrics": {
            "trades": trades,
            "min_trades_needed": thresholds["min_trades"],
            "winrate": round(winrate, 2),
            "min_winrate_needed": thresholds["min_winrate"],
            "expectancy_R": round(exp_r, 3),
            "profit_factor": round(pf, 2) if pf else None,
            "min_profit_factor_needed": thresholds["min_profit_factor"],
        },
        "checks": {
            "enough_trades": enough_trades,
            "winrate_ok": wr_ok,
            "expectancy_ok": exp_ok,
            "profit_factor_ok": pf_ok,
        },
    }


def graduation_report() -> dict:
    candidates = list_candidates()
    results_file = OUTPUT_DIR / "results.jsonl"
    results = _read_jsonl(results_file)

    all_trades = []
    for r in results:
        cid = r.get("candidate_id")
        matching = [c for c in candidates if c.candidate_id == cid]
        if matching:
            c = matching[0]
            all_trades.append({
                "setup_type": c.setup_type,
                "grade": c.grade,
                "r_multiple": r.get("r_multiple"),
                "mfe": r.get("mfe"),
                "mae": r.get("mae"),
                "hit_tp1": r.get("hit_tp1", False),
                "hit_tp2": r.get("hit_tp2", False),
                "hit_sl": r.get("hit_sl", False),
            })

    setup_types_seen = sorted(set(t.get("setup_type", "UNKNOWN") for t in all_trades))

    setup_validations = {}
    for st in setup_types_seen:
        setup_validations[st] = validate_setup(st, all_trades)

    global_stats = get_summary()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sessions_completed": get_session_count(),
        "target_sessions": TARGET_SESSIONS,
        "test_complete": is_test_complete(),
        "global": {
            "total_trades": global_stats.get("total_results", 0),
            "winrate": global_stats.get("winrate", 0),
            "expectancy_R": global_stats.get("expectancy_R", 0),
            "profit_factor": global_stats.get("profit_factor"),
        },
        "setups": setup_validations,
        "summary": {
            "passed": sum(1 for v in setup_validations.values() if v["passed"]),
            "failed": sum(1 for v in setup_validations.values() if not v["passed"]),
            "total_setups_tested": len(setup_validations),
        },
    }

    GRADUATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    GRADUATION_FILE.write_text(json.dumps(report, indent=2, default=str))

    return report


def _write_interim_report(session: int):
    summary = get_summary()
    path = PROJECT_ROOT / "reports" / "ipo" / "spacex" / f"spcx_v2_interim_{session}.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# SPCX V2 — Interim Report Session {session}/{TARGET_SESSIONS}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        f"- Candidates: {summary.get('total_candidates', 0)}",
        f"- Rejects: {summary.get('total_rejects', 0)}",
        f"- Winrate: {summary.get('winrate', 0)}%",
        f"- Expectancy: {summary.get('expectancy_R', 0)}R",
        f"- Profit Factor: {summary.get('profit_factor', 'N/A')}",
        "",
        "## By Grade",
        "",
    ]
    for g in ["A+", "A", "B"]:
        count = summary.get("by_grade", {}).get(g, 0)
        lines.append(f"- {g}: {count}")

    lines += [
        "",
        "<i>Paper-only. {}/{}</i>".format(session, TARGET_SESSIONS),
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
