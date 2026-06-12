from __future__ import annotations
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json


def collect_sheets(symbol: str = "SPCX") -> dict[str, Any]:
    out: dict[str, Any] = {
        "source": "google_sheets_latest",
        "symbol": symbol,
        "collected_at": utc_now(),
        "ok": False,
        "rows_count": 0,
        "metrics": {},
        "freshness_seconds": None,
        "error": None,
    }
    try:
        snap_path = REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json"
        if not snap_path.exists():
            out["error"] = "no scored snapshot for sheets proxy"
            return out

        snap = read_json(snap_path, {})
        if not snap:
            out["error"] = "scored snapshot empty"
            return out

        scores = snap.get("scores", {}) or {}
        signals = snap.get("signals", []) or []
        price = snap.get("price")

        out["ok"] = True
        out["rows_count"] = len(scores) + len(signals) + (1 if price is not None else 0)
        out["metrics"] = {
            "price": price,
            "scores": scores,
            "signals": signals,
        }

        written_at = snap.get("written_at") or snap.get("produced_at")
        if written_at:
            try:
                from datetime import datetime, timezone
                col_dt = datetime.fromisoformat(out["collected_at"].replace("Z", "+00:00"))
                wr_dt = datetime.fromisoformat(written_at.replace("Z", "+00:00"))
                out["freshness_seconds"] = (col_dt - wr_dt).total_seconds()
            except Exception:
                pass

        try:
            from ..sheets_consumer import write_spacex_to_sheets
            result = write_spacex_to_sheets()
            out["sheets_push"] = {
                "ok": result.ok,
                "rows_written": result.rows_written,
                "mode": result.mode,
            }
        except Exception:
            out["sheets_push"] = {"ok": False, "mode": "unavailable"}

    except Exception as exc:
        out["error"] = str(exc)

    return out
