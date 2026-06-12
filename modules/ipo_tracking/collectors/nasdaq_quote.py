from __future__ import annotations
import json
import urllib.request
from datetime import datetime, timezone
from typing import Any
from ..io import utc_now, REPO_ROOT, read_json

NASDAQ_QUOTE_API = "https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks"
NASDAQ_REAL_TIME_API = "https://api.nasdaq.com/api/quote/{symbol}/realtime?assetclass=stocks"


def collect_nasdaq_quote(symbol: str = "SPCX", *, timeout: int = 12) -> dict[str, Any]:
    out: dict[str, Any] = {
        "source": "nasdaq_quote",
        "symbol": symbol,
        "collected_at": utc_now(),
        "ok": False,
        "regular_market_price": None,
        "previous_close": None,
        "volume": None,
        "ipo_cross_state": "unknown",
        "indicative_price": None,
        "first_print": None,
        "first_print_ts": None,
        "halt_status": None,
        "market_phase": _current_market_phase(),
        "price_status": "missing",
        "error": None,
    }

    try:
        url = NASDAQ_QUOTE_API.format(symbol=symbol)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 opt-trading spacex_super_desk",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if data.get("status", {}).get("rCode") == 200:
            quote = data.get("data", {})
            out["ok"] = True
            out["regular_market_price"] = _num(quote.get("lastSalePrice"))
            out["previous_close"] = _num(quote.get("previousClose"))
            out["volume"] = _num(quote.get("volume"))
            out["exchange"] = quote.get("exchange")
            out["company_name"] = quote.get("companyName")

            if out["regular_market_price"] is not None:
                out["price_status"] = "live"
            elif _is_ipo_cross_active():
                out["ipo_cross_state"] = "pending"
                out["price_status"] = "indicative"
            else:
                out["price_status"] = "missing"

    except Exception as exc:
        out["error"] = str(exc)

    _enrich_from_bot_vision(out, symbol)

    if out["regular_market_price"] is None:
        phase = _current_market_phase()
        if phase == "preopen":
            out["ipo_cross_state"] = "pending"
            out["price_status"] = "WAITING_FIRST_PRINT"
        elif phase == "regular":
            out["price_status"] = "NO_PRICE_AVAILABLE_YET"

    return out


def _enrich_from_bot_vision(out: dict[str, Any], symbol: str) -> None:
    try:
        bot_vision_dir = REPO_ROOT / "data" / "bot_vision" / "outputs"
        if not bot_vision_dir.exists():
            return
        files = sorted(bot_vision_dir.rglob("*.json"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
        for fp in files:
            data = read_json(fp, {})
            page_id = data.get("page_id", "")
            if "nasdaq" in page_id.lower() and symbol.lower() in page_id.lower():
                preview = data.get("json_preview", {})
                if not preview and isinstance(data.get("extracted_text"), str):
                    extracted = data["extracted_text"]
                    price_match = _extract_price_from_text(extracted)
                    if price_match:
                        out["regular_market_price"] = out["regular_market_price"] or price_match
                        if out["price_status"] == "missing":
                            out["price_status"] = "indicative"
                        out["ipo_cross_state"] = "released"
                break
    except Exception:
        pass


def _extract_price_from_text(text: str) -> float | None:
    import re
    matches = re.findall(r'\$?\s*(\d{1,4}\.\d{2})', text)
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            pass
    return None


def _current_market_phase() -> str:
    now = datetime.now(timezone.utc)
    h = now.hour + now.minute / 60.0
    wd = now.weekday()
    if wd >= 5:
        return "closed"
    if h < 13.25:
        return "preopen"
    if h < 13.5:
        return "preopen"
    if h < 20.0:
        return "regular"
    if h < 23.0:
        return "after_hours"
    return "closed"


def _is_ipo_cross_active() -> bool:
    now = datetime.now(timezone.utc)
    h = now.hour + now.minute / 60.0
    wd = now.weekday()
    if wd >= 5:
        return False
    return 13.416 <= h < 14.0


def _num(v: Any) -> float | None:
    if v is None or v == "" or v == "N/A":
        return None
    try:
        return float(str(v).replace("$", "").replace(",", ""))
    except (TypeError, ValueError):
        return None
