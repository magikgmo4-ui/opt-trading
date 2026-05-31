#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

VISION_ANALYSIS_OUT = Path(
    os.getenv("VISION_ANALYSIS_OUT", str(REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis"))
)
ANALYSIS_LATEST = VISION_ANALYSIS_OUT / "latest.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _capture_id(symbol: str, timeframe: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"cap_{ts}_{symbol}_{timeframe}"


def openai_vision_analysis(png_path: str, symbol: str, timeframe: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    with open(png_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    prompt = (
        f"Tu es un analyste trading. Analyse ce chart {symbol} en timeframe {timeframe}.\n\n"
        f"Réponds STRICTEMENT en FRANÇAIS, format compact.\n\n"
        f"Structure obligatoire:\n"
        f"## SIGNAL\n"
        f"- Direction: bullish/bearish/neutral\n"
        f"- Confiance: 0.0-1.0\n"
        f"- Preuves: liste courte\n\n"
        f"## NIVEAUX\n"
        f"- Support: prix identifiés\n"
        f"- Résistance: prix identifiés\n\n"
        f"## STRUCTURE\n"
        f"- Tendance: haussier/baissier/range\n"
        f"- Structure: HH/HL, LH/LL, range\n\n"
        f"## RISQUES\n"
        f"- Flags: funding, volume, divergence, etc.\n\n"
        f"Regles: pas de blabla, prix exacts si lisibles sinon ~, n/v si invisible."
    )

    url = f"{OPENAI_API_BASE.rstrip('/')}/responses"
    content = [
        {"type": "input_text", "text": prompt},
        {"type": "input_image", "image_url": f"data:image/png;base64,{b64}"},
    ]
    payload = {
        "model": OPENAI_MODEL,
        "input": [{"role": "user", "content": content}],
        "max_output_tokens": 1000,
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

    r = json.loads(body)
    if isinstance(r, dict) and isinstance(r.get("output_text"), str) and r["output_text"].strip():
        return r["output_text"].strip()

    parts = []
    for item in r.get("output") or []:
        for c in item.get("content") or []:
            t = c.get("type")
            if t in ("output_text", "text"):
                tx = c.get("text") or ""
                if tx.strip():
                    parts.append(tx.strip())
    return "\n\n".join(parts).strip() or "(no text output)"


def parse_openai_to_signals(raw: str, symbol: str, timeframe: str) -> list[dict]:
    signals = []
    raw_lower = raw.lower()

    direction = "neutral"
    if "bullish" in raw_lower or "haussier" in raw_lower:
        direction = "bullish"
    elif "bearish" in raw_lower or "baissier" in raw_lower:
        direction = "bearish"

    confidence = 0.5
    import re
    conf_match = re.search(r"confiance[:\s]*([0-9]+\.[0-9]+)", raw_lower)
    if conf_match:
        confidence = float(conf_match.group(1))

    support_levels = re.findall(r"(?:support|S)[:\s]*([0-9,.\s]+)", raw_lower)
    resistance_levels = re.findall(r"(?:résistance|resistance|R)[:\s]*([0-9,.\s]+)", raw_lower)

    def extract_numbers(text: str) -> list[float]:
        nums = re.findall(r"[0-9]+(?:\.[0-9]+)?", text.replace(",", ""))
        return [float(n) for n in nums if float(n) > 1000]

    supports = []
    for s in support_levels:
        supports.extend(extract_numbers(s))

    resistances = []
    for r in resistance_levels:
        resistances.extend(extract_numbers(r))

    signals.append({
        "type": "trend_direction",
        "value": direction,
        "confidence": confidence,
        "note": raw.split("## SIGNAL")[-1].split("##")[0].strip()[:200] if "## SIGNAL" in raw else ""
    })

    if supports:
        signals.append({
            "type": "support_level",
            "value": supports[0],
            "confidence": min(confidence + 0.1, 1.0),
            "note": f"Support level: {supports[0]}"
        })

    if resistances:
        signals.append({
            "type": "resistance_level",
            "value": resistances[0],
            "confidence": min(confidence + 0.1, 1.0),
            "note": f"Resistance level: {resistances[0]}"
        })

    if direction != "neutral" and confidence >= 0.5:
        signals.append({
            "type": "setup_signal",
            "value": direction,
            "confidence": confidence,
            "note": f"Setup signal detected: {direction} (conf={confidence})"
        })

    return signals


def build_vision_analysis_v1(
    symbol: str,
    timeframe: str,
    capture_id: str,
    signals: list[dict],
    raw_analysis: str,
    png_path: str | None = None,
) -> dict:
    return {
        "input_class": "vision_analysis.v1",
        "capture_id": capture_id,
        "symbol": symbol,
        "timeframe": timeframe,
        "analysis_ts": _utc_now_iso(),
        "source_module": "bot_vision_headless_poc",
        "freshness_state": "fresh",
        "signals": signals,
        "raw_analysis": raw_analysis,
        "image_ref": png_path or "",
    }


def write_vision_analysis(data: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    tmp = output_dir / "latest.json.uploading"
    final = output_dir / "latest.json"

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, final)

    print(f"OK: {final}")
    return final


def telegram_summary(data: dict) -> str:
    symbol = data.get("symbol", "?")
    tf = data.get("timeframe", "?")
    signals = data.get("signals", [])
    lines = [f"<b>{symbol} ({tf})</b> - Vision Analysis"]
    for s in signals:
        t = s.get("type", "")
        v = s.get("value", "")
        c = s.get("confidence", 0)
        icon = {"trend_direction": "📊", "support_level": "🟢", "resistance_level": "🔴", "setup_signal": "⚡"}.get(t, "•")
        lines.append(f"{icon} {t}: {v} (conf={c:.2f})")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze a captured screenshot using OpenAI vision")
    ap.add_argument("--png", required=True, help="Path to screenshot PNG")
    ap.add_argument("--symbol", default="BTCUSDT", help="Asset symbol")
    ap.add_argument("--timeframe", default="15m", help="Chart timeframe")
    ap.add_argument("--capture-id", default="", help="Capture ID (auto if empty)")
    ap.add_argument("--telegram", action="store_true", help="Send Telegram notification")
    ap.add_argument("--telegram-only-signal", action="store_true", default=True,
                    help="Only send Telegram if signal confidence >= 0.6")
    ap.add_argument("--output-dir", default=str(VISION_ANALYSIS_OUT), help="Output directory")
    ap.add_argument("--dry-run", action="store_true", help="Skip OpenAI call, produce stub")
    args = ap.parse_args()

    if not os.path.exists(args.png):
        print(f"ERROR: PNG not found: {args.png}", file=sys.stderr)
        return 1

    capture_id = args.capture_id or _capture_id(args.symbol, args.timeframe)

    if args.dry_run:
        signals = [
            {"type": "trend_direction", "value": "neutral", "confidence": 0.5,
             "note": "Dry run — no analysis performed"},
        ]
        raw = "(dry run)"
    else:
        raw = openai_vision_analysis(args.png, args.symbol, args.timeframe)
        signals = parse_openai_to_signals(raw, args.symbol, args.timeframe)

    analysis = build_vision_analysis_v1(
        symbol=args.symbol,
        timeframe=args.timeframe,
        capture_id=capture_id,
        signals=signals,
        raw_analysis=raw,
        png_path=args.png,
    )

    out_path = write_vision_analysis(analysis, Path(args.output_dir))
    print(f"Signals: {len(signals)}")
    for s in signals:
        print(f"  {s['type']}: {s['value']} (conf={s['confidence']})")

    if args.telegram:
        max_conf = max((s.get("confidence", 0) for s in signals), default=0)
        if args.telegram_only_signal and max_conf < 0.6:
            print(f"SKIP Telegram: max confidence {max_conf:.2f} < 0.6")
        else:
            try:
                sys.path.insert(0, str(REPO_ROOT))
                from shared.telegram_notify import send_telegram_with_metrics
                msg = telegram_summary(analysis)
                result = send_telegram_with_metrics(msg, source="bot_vision_poc", tags={"capture_id": capture_id})
                if result.get("ok"):
                    print(f"OK: Telegram sent")
                else:
                    print(f"SKIP Telegram: {result.get('error', 'unknown')}")
            except ImportError as e:
                print(f"SKIP Telegram: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
