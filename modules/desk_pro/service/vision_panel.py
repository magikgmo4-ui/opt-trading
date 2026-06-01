from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VISION_CONTEXT_LATEST = Path(
    "data/deskpro/inputs/vision_context/coinglass/latest.json"
)
VISION_CONTEXT_NEWS_LATEST = Path(
    "data/deskpro/inputs/vision_context/news_sentiment/latest.json"
)
VISION_CONTEXT_SCREENER_LATEST = Path(
    "data/deskpro/inputs/vision_context/screener/latest.json"
)
TELEGRAM_CLAIM_LATEST = Path(
    "data/deskpro/inputs/telegram_claim/latest.json"
)


def _age_hours(screenshot_ts: str) -> Optional[float]:
    try:
        ts = datetime.fromisoformat(screenshot_ts.replace("Z", "+00:00"))
        return (datetime.now(tz=timezone.utc) - ts).total_seconds() / 3600
    except Exception:
        return None


def read_vision_panel_data(path: Optional[Path] = None) -> dict:
    """Read vision_context.coinglass.v1 and return panel-ready dict.

    Returns {"ok": False, "vision": None, "reason": "..."} on any failure.
    Returns {"ok": True, "vision": {...}, "age_hours": float|None} on success.
    Never raises.
    """
    p = path or VISION_CONTEXT_LATEST
    if not p.exists():
        return {"ok": False, "vision": None, "reason": "no_data"}

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "vision": None, "reason": "read_error"}

    if data.get("input_class") != "vision_context.coinglass.v1":
        return {"ok": False, "vision": None, "reason": "wrong_input_class"}

    age = _age_hours(data.get("screenshot_ts", ""))
    return {"ok": True, "vision": data, "age_hours": age}


def _read_simple_payload(path: Path, input_class: str, ts_key: str) -> dict:
    if not path.exists():
        return {"ok": False, "payload": None, "reason": "no_data"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "payload": None, "reason": "read_error"}
    if data.get("input_class") != input_class:
        return {"ok": False, "payload": None, "reason": "wrong_input_class"}
    age = _age_hours(data.get(ts_key, ""))
    return {"ok": True, "payload": data, "age_hours": age}


def read_news_panel_data(path: Optional[Path] = None) -> dict:
    return _read_simple_payload(path or VISION_CONTEXT_NEWS_LATEST, "vision_context.news_sentiment.v1", "analysis_ts")


def read_screener_panel_data(path: Optional[Path] = None) -> dict:
    return _read_simple_payload(path or VISION_CONTEXT_SCREENER_LATEST, "vision_context.screener.v1", "analysis_ts")


def read_telegram_claim_panel_data(path: Optional[Path] = None) -> dict:
    return _read_simple_payload(path or TELEGRAM_CLAIM_LATEST, "telegram_claim.v1", "claim_ts")
