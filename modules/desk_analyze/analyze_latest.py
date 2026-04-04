#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

try:
    from zoneinfo import ZoneInfo  # py>=3.9
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

DEFAULT_TZ = os.getenv("TIMEZONE", "America/Montreal")
DEFAULT_INDEX = os.getenv("INDEX_FILE", "/opt/trading/desk/snapshots/latest.json")
DEFAULT_SYMBOLS = os.getenv("DESK_SYMBOLS", "BTCUSDT.P,XAUUSD,SOLUSDT.P,ETHUSDT.P")
DEFAULT_STALE_MINUTES = int(os.getenv("STALE_MINUTES", "15"))
REALDATA_TIMEOUT_SECONDS = float(os.getenv("DESK_ANALYZE_REALDATA_TIMEOUT_SECONDS", "4"))
BINANCE_FUTURES_BASE_URL = os.getenv("DESK_ANALYZE_BINANCE_FUTURES_BASE_URL", "https://fapi.binance.com")

# OpenAI (Responses API)
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", os.getenv("DESK_ANALYZE_OPENAI_MODEL", "gpt-4.1-mini"))
DESK_ANALYZE_OPENAI = os.getenv("DESK_ANALYZE_OPENAI", "1").strip().lower()  # 1/0
DESK_ANALYZE_MAX_CHARS = int(os.getenv("DESK_ANALYZE_MAX_CHARS", "3600"))  # keep under Telegram limit

# Artifacts
VISION_OUTBOX = os.getenv("VISION_OUTBOX", "/srv/sftp/shared_files/shared/vision_outbox")


@dataclass
class MarketDataStatus:
    source: str
    status: str
    details: Optional[Dict[str, Any]] = None
    error: str = ""

def _tzinfo(name: str):
    if ZoneInfo is None:
        return timezone.utc
    try:
        return ZoneInfo(name)
    except Exception:
        return timezone.utc

def _now_iso(tz_name: str) -> str:
    tz = _tzinfo(tz_name)
    return datetime.now(tz).replace(microsecond=0).isoformat()

def _parse_iso(s: str) -> Optional[datetime]:
    s = (s or "").strip()
    if not s:
        return None
    try:
        # Accept either "...-05:00" or "2026-03-03T12:46:17"
        if s.endswith("Z"):
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            # No offset provided: treat as DEFAULT_TZ (local) instead of UTC.
            dt = dt.replace(tzinfo=_tzinfo(DEFAULT_TZ))
        return dt
    except Exception:
        return None

def _age_minutes(snapshot_ts: str, tz_name: str) -> Optional[int]:
    dt = _parse_iso(snapshot_ts)
    if not dt:
        return None
    now = datetime.now(_tzinfo(tz_name))
    # normalize tz
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_tzinfo(tz_name))
    try:
        dt_local = dt.astimezone(_tzinfo(tz_name))
    except Exception:
        dt_local = dt
    return int((now - dt_local).total_seconds() // 60)

def load_latest(index_path: str) -> Dict[str, Any]:
    if not os.path.exists(index_path):
        return {}
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}

def _boolish(v: str) -> bool:
    return v.strip().lower() in ("1", "true", "yes", "y", "on")

def _safe_telegram(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    # try cut at last newline before limit
    cut = text.rfind("\n", 0, max(0, limit - 50))
    if cut < 200:
        cut = limit - 50
    return text[:cut].rstrip() + "\n…(truncated)"


def _fetch_json(url: str, timeout: float) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "opt-trading/desk-analyze",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def _normalize_binance_symbol(symbol: str) -> Optional[str]:
    base = (symbol or "").strip().upper()
    if not base:
        return None
    if base.endswith(".P"):
        base = base[:-2]
    if not base.endswith("USDT"):
        return None
    if any(ch for ch in base if not (ch.isalnum() or ch == "_")):
        return None
    return base


def _format_compact_float(value: Any, digits: int = 4) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    if abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    if abs(num) >= 100:
        return f"{num:.2f}"
    if abs(num) >= 1:
        return f"{num:.{digits}f}".rstrip("0").rstrip(".")
    return f"{num:.6f}".rstrip("0").rstrip(".")


def _format_pct(value: Any, digits: int = 2) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return "n/a"
    return f"{num:+.{digits}f}%"


def _minutes_until(timestamp_ms: Any, tz_name: str) -> Optional[int]:
    try:
        dt = datetime.fromtimestamp(float(timestamp_ms) / 1000.0, tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
    now = datetime.now(_tzinfo(tz_name))
    return int((dt.astimezone(_tzinfo(tz_name)) - now).total_seconds() // 60)


def fetch_binance_market_data(symbol: str, tz_name: str) -> MarketDataStatus:
    fut_symbol = _normalize_binance_symbol(symbol)
    if not fut_symbol:
        return MarketDataStatus(
            source="binance-futures",
            status="unsupported",
            error="unsupported symbol for Binance USDT futures",
        )

    base = BINANCE_FUTURES_BASE_URL.rstrip("/")
    try:
        ticker = _fetch_json(f"{base}/fapi/v1/ticker/24hr?symbol={fut_symbol}", REALDATA_TIMEOUT_SECONDS)
        premium = _fetch_json(f"{base}/fapi/v1/premiumIndex?symbol={fut_symbol}", REALDATA_TIMEOUT_SECONDS)
        open_interest = _fetch_json(f"{base}/fapi/v1/openInterest?symbol={fut_symbol}", REALDATA_TIMEOUT_SECONDS)
    except urllib.error.HTTPError as e:
        return MarketDataStatus(source="binance-futures", status="error", error=f"HTTP {getattr(e, 'code', '?')}")
    except urllib.error.URLError as e:
        return MarketDataStatus(source="binance-futures", status="error", error=f"network: {e.reason}")
    except Exception as e:
        return MarketDataStatus(source="binance-futures", status="error", error=str(e))

    details = {
        "symbol": fut_symbol,
        "last_price": ticker.get("lastPrice"),
        "price_change_pct": ticker.get("priceChangePercent"),
        "quote_volume": ticker.get("quoteVolume"),
        "funding_rate": premium.get("lastFundingRate"),
        "mark_price": premium.get("markPrice"),
        "next_funding_minutes": _minutes_until(premium.get("nextFundingTime"), tz_name),
        "open_interest": open_interest.get("openInterest"),
        "exchange_time": premium.get("time") or ticker.get("closeTime") or open_interest.get("time"),
    }
    return MarketDataStatus(source="binance-futures", status="ok", details=details)


def collect_market_data(symbols: List[str], tz_name: str) -> Dict[str, MarketDataStatus]:
    return {symbol: fetch_binance_market_data(symbol, tz_name) for symbol in symbols}


def _build_chart_runtime_line(snap: Dict[str, Any]) -> str:
    image_path = str(snap.get("path") or "")
    image_ok = os.path.exists(image_path) if image_path else False
    image_name = os.path.basename(image_path) if image_path else "n/a"
    return f"- TV/runtime: image={'OK' if image_ok else 'missing'} file={image_name}"


def _build_market_line(market: Optional[MarketDataStatus]) -> str:
    if not market:
        return "- Market: unavailable (no fetch attempted)"
    if market.status == "unsupported":
        return "- Market: n/a for this symbol (Binance USDT futures only in V1)"
    if market.status != "ok" or not market.details:
        reason = market.error or "source unavailable"
        return f"- Market: unavailable ({reason})"

    details = market.details
    raw_funding = details.get("funding_rate")
    try:
        funding_pct = float(raw_funding) * 100.0 if raw_funding is not None else None
    except (TypeError, ValueError):
        funding_pct = None
    funding_txt = _format_pct(funding_pct, digits=4)
    next_funding = details.get("next_funding_minutes")
    next_funding_txt = "n/a" if next_funding is None else f"{next_funding}m"
    return (
        "- Market: "
        f"px={_format_compact_float(details.get('last_price'))} "
        f"24h={_format_pct(details.get('price_change_pct'))} "
        f"funding={funding_txt} "
        f"OI={_format_compact_float(details.get('open_interest'))} "
        f"vol24h={_format_compact_float(details.get('quote_volume'))} "
        f"next={next_funding_txt}"
    )

def _openai_responses_vision(prompt: str, labeled_images: List[Tuple[str, str]]) -> str:
    """
    labeled_images: list of (label, file_path)
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is empty")
    url = f"{OPENAI_API_BASE.rstrip('/')}/responses"

    content: List[Dict[str, Any]] = [{"type": "input_text", "text": prompt}]
    for label, path in labeled_images:
        with open(path, "rb") as f:
            b = f.read()
        b64 = base64.b64encode(b).decode("ascii")
        # Most files are PNG in our pipeline.
        content.append({"type": "input_text", "text": f"Chart: {label}"})
        content.append({"type": "input_image", "image_url": f"data:image/png;base64,{b64}"})

    payload = {
        "model": OPENAI_MODEL,
        "input": [{"role": "user", "content": content}],
        "max_output_tokens": 700,
        "temperature": 0.2,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        raise RuntimeError(f"OpenAI HTTP {getattr(e, 'code', '?')}: {body[:800]}") from e
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {e}") from e

    try:
        r = json.loads(body)
    except Exception:
        return body.strip()

    # Best-effort extraction across response shapes
    if isinstance(r, dict) and isinstance(r.get("output_text"), str) and r["output_text"].strip():
        return r["output_text"].strip()

    parts: List[str] = []
    for item in (r.get("output") or []):
        for c in (item.get("content") or []):
            t = c.get("type")
            if t in ("output_text", "text"):
                tx = c.get("text") or ""
                if tx.strip():
                    parts.append(tx.strip())
    out = "\n\n".join(parts).strip()
    return out or "(no text output)"

def build_status_text(
    latest: Dict[str, Any],
    symbols: List[str],
    stale_minutes: int,
    tz_name: str,
    market_data: Optional[Dict[str, MarketDataStatus]] = None,
) -> Tuple[str, Dict[str, Any]]:
    now = _now_iso(tz_name)
    lines: List[str] = []
    lines.append(f"[Desk Pro /analyze] {now} ({tz_name})")
    lines.append(f"Source: latest.json (local) | stale>= {stale_minutes} min")
    lines.append("")

    missing = [s for s in symbols if s not in latest]
    ages: Dict[str, Optional[int]] = {}
    stale: List[str] = []

    for s in symbols:
        snap = latest.get(s) or {}
        age = _age_minutes(str(snap.get("snapshot_ts") or ""), tz_name)
        ages[s] = age
        if age is None or age >= stale_minutes:
            stale.append(s)

    if missing:
        lines.append("WARN:")
        lines.append("MISSING: " + ", ".join(missing))
        lines.append("")

    ok_syms = [s for s in symbols if s in latest]
    if stale:
        lines.append("OK:" if ok_syms else "ERROR:")
        if ok_syms:
            lines.append("STALE: " + ", ".join(stale))
        else:
            lines.append("No symbols present in latest.json")
        lines.append("")
    else:
        lines.append("OK: " + ", ".join(ok_syms))
        lines.append("")

    for s in symbols:
        snap = latest.get(s)
        age = ages.get(s)
        if not snap:
            lines.append(f"{s} [MISSING]")
            continue
        age_txt = "?" if age is None else str(age)
        badge = "STALE" if (age is None or age >= stale_minutes) else "OK"
        lines.append(f"{s} {snap.get('tf','?')} [{badge}] age={age_txt}m")
        lines.append(f"- snapshot_ts: {snap.get('snapshot_ts')}")
        if snap.get("meta"):
            lines.append(f"- meta: source={snap['meta'].get('source')} host={snap['meta'].get('host')}")
        lines.append(f"- path: {snap.get('path')}")
        lines.append(_build_chart_runtime_line(snap))
        lines.append(_build_market_line((market_data or {}).get(s)))
        lines.append("")

    if stale:
        lines.append("Action:")
        lines.append("- refresh capture (snapshots too old)")
        lines.append("")

    meta = {
        "now": now,
        "tz": tz_name,
        "stale_minutes": stale_minutes,
        "missing": missing,
        "stale": stale,
        "ages": ages,
    }
    return "\n".join(lines).rstrip(), meta

def build_vision_prompt(symbols: List[str], tf: str = "H1", t: Optional[str] = None) -> str:
    if t:
        tf = t
    # FR, ultra-compact. This prompt is designed to fit in a single Telegram message.
    order = ", ".join(symbols)
    return f"""Tu es un analyste trading. Analyse des captures TradingView (layout 2x2) au timeframe {tf}.
Réponds STRICTEMENT en FRANÇAIS.

Objectif: un résumé TECHNIQUE (pas de blabla) qui tient dans Telegram.

FORMAT OBLIGATOIRE (Markdown), 5 lignes MAX par symbole:
## <SYMBOL>
- Tendance: <haussier/baissier/range> (6 mots max)
- Structure: <HH/HL ou LL/LH ou range + biais>
- Niveaux: S1=..., S2=... | R1=..., R2=... (si illisible: n/v)
- Plan: <LONG/SHORT/NEUTRE> — condition déclencheur (1 ligne)
- Invalidation: <niveau/condition> (1 ligne)

Règles:
- Pas de paragraphes. Pas de répétitions. Pas d’emojis.
- Utilise des prix EXACTS si lisibles, sinon arrondis/approximations et marque "~".
- Si l’info n’est pas visible: "n/v".

Symboles (ordre): {order}
"""


def compact_vision_text(raw: str, symbols: List[str], max_lines_per_symbol: int = 5, max_chars: int = 2400) -> str:
    """Turn any OpenAI output into a compact, Telegram-safe summary.

    Prefer '## SYMBOL' headings; otherwise fall back to first lines.
    """
    raw = (raw or "").replace("\r\n", "\n").strip()

    # Remove code fences if any
    raw = re.sub(r"```.*?```", "", raw, flags=re.S).strip()

    # Parse sections by markdown heading
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    buf: List[str] = []

    for line in raw.split("\n"):
        m = re.match(r"^\s*##\s*(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = buf
            current = m.group(1).strip()
            buf = []
            continue
        if current is not None:
            buf.append(line.rstrip())

    if current is not None:
        sections[current] = buf

    def _pick_section(sym: str) -> Optional[List[str]]:
        # Try exact / normalized match
        sym_n = re.sub(r"\s+", "", sym).lower()
        for k,v in sections.items():
            k_n = re.sub(r"\s+", "", k).lower()
            if k_n == sym_n or k_n.startswith(sym_n) or sym_n.startswith(k_n):
                return v
        return None

    out: List[str] = []
    for sym in symbols:
        body = _pick_section(sym)
        if not body:
            continue
        out.append(f"## {sym}")
        kept = []
        for l in body:
            if l.strip() == "":
                continue
            kept.append(l)
            if len(kept) >= max_lines_per_symbol:
                break
        out.extend(kept)
        out.append("")

    compact = "\n".join(out).strip()
    if not compact:
        compact = "\n".join(raw.split("\n")[:40]).strip()

    if len(compact) > max_chars:
        compact = compact[:max_chars].rstrip() + "\n…"
    return compact

def write_outbox(run_id: str, text: str) -> Dict[str, str]:
    os.makedirs(VISION_OUTBOX, exist_ok=True)
    txt_path = os.path.join(VISION_OUTBOX, f"analyze_{run_id}.txt")
    md_path = os.path.join(VISION_OUTBOX, f"analyze_{run_id}.md")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return {"txt": txt_path, "md": md_path}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=DEFAULT_INDEX)
    ap.add_argument("--symbols", default=DEFAULT_SYMBOLS)
    ap.add_argument("--stale-minutes", type=int, default=DEFAULT_STALE_MINUTES)
    ap.add_argument("--json", action="store_true", help="Output JSON (debug)")
    ap.add_argument("--no-openai", action="store_true", help="Disable OpenAI vision analysis")
    args = ap.parse_args()

    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    latest = load_latest(args.index)

    market_data = collect_market_data(symbols, DEFAULT_TZ)

    status_text, meta = build_status_text(latest, symbols, args.stale_minutes, DEFAULT_TZ, market_data=market_data)

    openai_enabled = (not args.no_openai) and _boolish(DESK_ANALYZE_OPENAI) and bool(OPENAI_API_KEY)
    vision_text = ""
    vision_err = ""

    # Only do vision if we have all symbol paths and nothing is missing
    if openai_enabled and not meta.get("missing"):
        labeled: List[Tuple[str, str]] = []
        for s in symbols:
            p = (latest.get(s) or {}).get("path")
            if p and os.path.exists(str(p)):
                labeled.append((f"{s} { (latest.get(s) or {}).get('tf','?') }", str(p)))
        if len(labeled) == len(symbols):
            try:
                prompt = build_vision_prompt(symbols, tf="H1")
                vision_text = _openai_responses_vision(prompt, labeled)
            except Exception as e:
                vision_err = str(e)
        else:
            vision_err = "Some image paths missing on disk; cannot run vision."

    # Build combined output
    combined = status_text
    run_id = datetime.now(_tzinfo(DEFAULT_TZ)).strftime("%Y%m%d_%H%M%S")
    outbox_paths: Dict[str, str] = {}

    if vision_text:
        vision_raw = vision_text.strip()
        vision_compact = compact_vision_text(vision_raw, symbols, max_lines_per_symbol=5, max_chars=2400)

        # Save FULL output to outbox (WinSCP-safe), but keep Telegram message compact.
        combined_full = status_text + "\n\n=== Vision (OpenAI) ===\n" + vision_raw
        outbox_paths = write_outbox(run_id, combined_full)

        combined = status_text + "\n\n=== Vision (résumé) ===\n" + vision_compact
        if outbox_paths.get("txt"):
            combined += f"\n\n(fichier complet: {outbox_paths.get('txt')})"

    elif vision_err and openai_enabled:
        combined += "\n\n=== Vision (OpenAI) ===\n" + f"ERROR: {vision_err}"

    combined = _safe_telegram(combined, DESK_ANALYZE_MAX_CHARS)

    if args.json:
        payload = {
            "status_text": status_text,
            "vision_text": vision_text,
            "vision_error": vision_err,
            "outbox": outbox_paths,
            "real_data": {
                symbol: {
                    "source": status.source,
                    "status": status.status,
                    "details": status.details,
                    "error": status.error,
                }
                for symbol, status in market_data.items()
            },
            "meta": meta,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(combined)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
