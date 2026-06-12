from __future__ import annotations
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json


def collect_telegram_signal(symbol: str = "SPCX") -> dict[str, Any]:
    out: dict[str, Any] = {
        "source": "telegram_signal",
        "symbol": symbol,
        "collected_at": utc_now(),
        "ok": False,
        "signals": [],
        "signals_count": 0,
        "alert_sent": False,
        "freshness_seconds": None,
        "error": None,
    }
    try:
        snap_path = REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json"
        if not snap_path.exists():
            out["error"] = "no scored snapshot"
            return out

        snap = read_json(snap_path, {})
        if not snap:
            out["error"] = "scored snapshot empty"
            return out

        signals = snap.get("signals", []) or []
        alerts = snap.get("alerts", []) or []
        all_signals = list(set(signals + [a.get("event", "") for a in alerts if a.get("event")]))

        out["ok"] = True
        out["signals"] = all_signals
        out["signals_count"] = len(all_signals)

        if all_signals:
            try:
                from ..telegram_dispatcher import send_spacex_alert
                result = send_spacex_alert(snap, channel="push")
                out["alert_sent"] = result.get("ok", False)
                out["alert_result"] = result
            except Exception as exc:
                out["alert_error"] = str(exc)

        written_at = snap.get("written_at") or snap.get("produced_at")
        if written_at:
            try:
                from datetime import datetime, timezone
                col_dt = datetime.fromisoformat(out["collected_at"].replace("Z", "+00:00"))
                wr_dt = datetime.fromisoformat(written_at.replace("Z", "+00:00"))
                out["freshness_seconds"] = (col_dt - wr_dt).total_seconds()
            except Exception:
                pass

    except Exception as exc:
        out["error"] = str(exc)

    return out
