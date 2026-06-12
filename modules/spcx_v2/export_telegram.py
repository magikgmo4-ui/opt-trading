"""SPCX V2 — Telegram export: A+ alerts and EOD summary."""

import json
from pathlib import Path
from typing import Optional

from modules.spcx_v2.paper_logger import list_candidates, get_summary
from modules.spcx_v2.config import OUTPUT_DIR
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.export_telegram")

_SENT_CACHE_FILE = OUTPUT_DIR / "telegram_sent.json"


def _load_sent_ids() -> set:
    if not _SENT_CACHE_FILE.exists():
        return set()
    try:
        with open(_SENT_CACHE_FILE) as f:
            return set(json.load(f))
    except (json.JSONDecodeError, FileNotFoundError):
        return set()


def _save_sent_ids(ids: set):
    _SENT_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_SENT_CACHE_FILE, "w") as f:
        json.dump(sorted(ids), f)


def _send_telegram(message: str) -> bool:
    try:
        from shared.telegram_notify import send_telegram
        send_telegram(message)
        return True
    except Exception as e:
        logger.warning("telegram send failed: %s", e)
        return False


def _format_alert(candidate) -> str:
    return (
        f"[{candidate.grade}] {candidate.symbol} {candidate.setup_type} | "
        f"TR{candidate.scores.trade_ready} LQ{candidate.scores.liquidity} "
        f"RS{candidate.scores.risk} SM{candidate.scores.smart_money} "
        f"CT{candidate.scores.catalyst}"
    )


def send_a_plus_alerts() -> int:
    sent_ids = _load_sent_ids()
    a_plus = [c for c in list_candidates() if c.grade == "A+"]

    count = 0
    for c in a_plus:
        if c.candidate_id in sent_ids:
            continue
        msg = _format_alert(c) + "\n\n<i>Paper-only. No execution.</i>"
        if _send_telegram(msg):
            sent_ids.add(c.candidate_id)
            count += 1
            logger.info("telegram alert sent for %s", c.candidate_id)

    _save_sent_ids(sent_ids)
    return count


def send_eod_summary() -> str:
    summary = get_summary()

    lines = [
        "<b>SPCX V2 — EOD Summary</b>",
        "",
        f"Setups detected: {summary['total_candidates']}",
        f"Rejects: {summary['total_rejects']}",
        f"Winrate: {summary['winrate']}%",
        f"Expectancy: {summary['expectancy_R']}R",
    ]

    if summary.get("profit_factor") is not None:
        lines.append(f"Profit Factor: {summary['profit_factor']}")

    by_grade = summary.get("by_grade", {})
    if by_grade:
        lines.append("")
        lines.append("<b>By grade:</b>")
        for g in ["A+", "A", "B", "reject"]:
            lines.append(f"  {g}: {by_grade.get(g, 0)}")

    lines.append("")
    lines.append(f"<i>Paper-only. Generated {summary.get('generated_at', '')}</i>")

    msg = "\n".join(lines)
    _send_telegram(msg)
    return msg
