"""Telegram alerter for stock_true_value scores — passive, read-only, no trading commands."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCORES_PATH = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest" / "scores.json"

# Prohibited terms — must never appear in any alert
_FORBIDDEN = frozenset({"BUY", "SELL", "EXECUTE", "ORDER", "LONG", "SHORT", "ENTRY", "EXIT", "TP", "SL"})


def _clean(text: str) -> str:
    for w in _FORBIDDEN:
        if w in text.upper():
            raise ValueError(f"FORBIDDEN term '{w}' found in alert text")
    return text


def _load_scores() -> dict:
    if not SCORES_PATH.exists():
        print(f"No scores file at {SCORES_PATH}")
        sys.exit(0)
    return json.loads(SCORES_PATH.read_text())


def _check_alerts(items: list[dict]) -> list[str]:
    alerts: list[str] = []

    for it in items:
        ticker = it.get("ticker", "?")
        grade = it.get("final_grade", "?")
        hype = it.get("hype_score", 0) or 0
        risk = it.get("risk_score", 0) or 0
        conf = it.get("confidence_score", 0) or 0
        true_value = it.get("true_value_score", 0) or 0

        # Thresholds from plan
        if grade == "A+":
            alerts.append(_clean(f"📐 A+ GRADE: {ticker} TrueValue={true_value:.0f} Risk={risk:.0f}"))
        elif conf > 80:
            alerts.append(_clean(f"📐 HIGH CONFIDENCE: {ticker} {grade} TrueValue={true_value:.0f} Conf={conf:.0f}%"))
        elif hype > 90:
            alerts.append(_clean(f"📐 EXTREME HYPE: {ticker} Hype={hype:.0f} TrueValue={true_value:.0f}"))
        elif risk > 85:
            alerts.append(_clean(f"📐 HIGH RISK: {ticker} Risk={risk:.0f} Grade={grade}"))

    return alerts


def run(dry_run: bool = False) -> dict:
    """Generate alerts from latest scores. Set dry_run=True to preview without sending."""
    data = _load_scores()
    items = data.get("items", [])
    alerts = _check_alerts(items)

    result = {
        "asof": data.get("asof", ""),
        "items_total": len(items),
        "alerts_count": len(alerts),
        "alerts": alerts,
        "dry_run": dry_run,
        "sent": 0,
    }

    if not alerts:
        print("No alerts triggered.")
        return result

    if dry_run:
        print(f"DRY RUN — {len(alerts)} alert(s) would be sent:")
        for a in alerts:
            print(f"  {a}")
        return result

    from modules.env.env import load_env
    load_env()

    from shared.telegram_notify import send_telegram

    header = "📐 True Value Alerts\n"
    footer = "\n\nDecision Support Only — no trading instruction."

    for alert in alerts:
        try:
            sent = send_telegram(header + alert + footer)
            if sent:
                result["sent"] += 1
                print(f"  sent: {alert[:80]}...")
        except Exception as e:
            print(f"  FAIL: {alert[:80]} — {e}")

    return result


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    result = run(dry_run=dry)
    if not dry:
        print(f"\nSent {result['sent']}/{result['alerts_count']} alerts.")
