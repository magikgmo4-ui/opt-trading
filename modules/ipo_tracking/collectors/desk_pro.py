from __future__ import annotations
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json


def collect_desk_pro(symbol: str = "SPCX") -> dict[str, Any]:
    out: dict[str, Any] = {
        "source": "desk_pro_latest",
        "symbol": symbol,
        "collected_at": utc_now(),
        "ok": False,
        "price": None,
        "scores": {},
        "signals": [],
        "signals_count": 0,
        "freshness_seconds": None,
        "error": None,
    }
    try:
        desk_path = REPO_ROOT / "ui/spacex_desk/latest.json"
        if not desk_path.exists():
            out["error"] = "desk_pro snapshot not found"
            return out

        data = read_json(desk_path, {})
        if not data:
            out["error"] = "desk_pro snapshot empty"
            return out

        out["ok"] = True
        out["price"] = data.get("price")
        out["scores"] = data.get("scores", {}) or {}
        out["signals"] = data.get("signals", []) or []
        out["signals_count"] = len(out["signals"])

        written_at = data.get("written_at") or data.get("produced_at")
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
