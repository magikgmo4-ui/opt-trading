"""
backtest_export.py — export backtest results to Google Sheets (CSV) and JSON.

Usage:
    python -m modules.trading_lab_v1.app.backtest_export
    python -m modules.trading_lab_v1.app.backtest_export --csv /tmp/backtest.csv
"""

from __future__ import annotations

import csv
import json
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_BACKTEST_DIR = _PROJECT_ROOT / "data" / "trading_lab_v1" / "backtests"
_EXPORT_DIR = _PROJECT_ROOT / "data" / "trading_lab_v1" / "exports"


def export_csv(output_path: Optional[Path] = None) -> Path:
    """Export latest backtest as CSV (Google Sheets compatible)."""
    latest = _BACKTEST_DIR / "latest.json"
    if not latest.exists():
        raise FileNotFoundError("No backtest report found. Run backtest first.")

    data = json.loads(latest.read_text(encoding="utf-8"))

    _EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = output_path or (_EXPORT_DIR / f"backtest_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header
        writer.writerow([
            "Channel", "Pair", "Direction", "Entry", "SL", "TP",
            "R_multiple", "Outcome", "P&L", "Signal_Date", "Backtest_Mode"
        ])

        for cr in data.get("by_channel", []):
            for t in cr.get("trades", []):
                writer.writerow([
                    cr["channel"],
                    t["pair"],
                    t["direction"],
                    t["entry"],
                    t["sl"],
                    t["tp"],
                    t["r_multiple"],
                    t["outcome"],
                    t["pnl"],
                    t.get("parsed_at", "")[:19],
                    data.get("mode", "optimistic"),
                ])

        # Summary rows
        writer.writerow([])
        writer.writerow(["=== SUMMARY BY CHANNEL ==="])
        writer.writerow(["Channel", "Trades", "Wins", "Losses", "Winrate%", "Avg_R", "P&L", "Pairs", "Date_Range"])
        for cr in data.get("by_channel", []):
            writer.writerow([
                cr["channel"], cr["total_trades"], cr["wins"], cr["losses"],
                cr["winrate_pct"], cr["avg_r"], cr["total_pnl"],
                ", ".join(cr.get("pairs", [])), cr.get("date_range", ""),
            ])

        gt = data.get("grand_total", {})
        writer.writerow([])
        writer.writerow(["=== GRAND TOTAL ==="])
        writer.writerow(["Channels", "Trades", "Wins", "Losses", "Winrate%", "Avg_R", "P&L"])
        writer.writerow([
            gt.get("channels"), gt.get("trades"), gt.get("wins"), gt.get("losses"),
            gt.get("winrate_pct"), gt.get("avg_r"), gt.get("total_pnl"),
        ])

    return path


def export_json(output_path: Optional[Path] = None) -> Path:
    """Export latest backtest as clean JSON for LocalCMS."""
    latest = _BACKTEST_DIR / "latest.json"
    if not latest.exists():
        raise FileNotFoundError("No backtest report found.")

    data = json.loads(latest.read_text(encoding="utf-8"))

    _EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = output_path or (_EXPORT_DIR / "latest.json")

    # Compact version for LocalCMS
    compact = {
        "contract": "backtest_export.v1",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "mode": data.get("mode"),
        "grand_total": data.get("grand_total"),
        "by_channel": [
            {
                "channel": cr["channel"],
                "trades": cr["total_trades"],
                "wins": cr["wins"],
                "losses": cr["losses"],
                "winrate_pct": cr["winrate_pct"],
                "avg_r": cr["avg_r"],
                "pnl": cr["total_pnl"],
                "pairs": cr.get("pairs", []),
                "date_range": cr.get("date_range", ""),
                "top_trades": cr.get("trades", [])[:5],
            }
            for cr in data.get("by_channel", [])
        ],
    }
    path.write_text(json.dumps(compact, indent=2, default=str), encoding="utf-8")
    return path


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    csv_path = None
    i = 0
    while i < len(args):
        if args[i] == "--csv" and i + 1 < len(args):
            csv_path = Path(args[i + 1]); i += 2
        else:
            i += 1

    csv_out = export_csv(csv_path)
    json_out = export_json()
    print(f"CSV: {csv_out}")
    print(f"JSON: {json_out}")
