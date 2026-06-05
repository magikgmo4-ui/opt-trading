"""
signal_tracker — archive clean trade signals per channel for trading lab backtesting.

Stores signals with entry, direction (LONG/SHORT), sl, tp, tps, leverage.
Data center output: data_center/views/telegram_signals/ for perf engine consumption.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"
_ARCHIVE_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "trade_signals"
_DC_TRADES = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals" / "trade_history"

_PRICE_STR = r'\d{1,8}(?:\.\d+)?'

# ── WSQ setup: "Coin: #APTUSDT Direction: Long Entry: $0.9545 Stop-loss: $0.9380" ──
_WSQ_SETUP_RE = re.compile(
    r'Coin(?:\s*name)?\s*:\s*\**\#?(?P<asset>[A-Z]{2,10})USDT\**.*?'
    r'Direction\s*:\s*(?P<direction>Long|Short).*?'
    r'Entry\s*:\s*\$?(?P<entry>' + _PRICE_STR + r').*?'
    r'(?:Stop[-\s]?loss|SL)\s*:\s*\$?(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

# ── WSQ targets: "Targets: $0.9740 - $0.9940 - $1.0140" ──
_WSQ_TARGETS_RE = re.compile(
    r'\$?(?P<tp>' + _PRICE_STR + r')\$?\s*[-–]\s*\$?(?P<tp2>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

# ── GOLD signals: "BUY GOLD Entry: 4496 SL: 4485 TP1: 4503 TP2: 4510" ──
_GOLD_SETUP_RE = re.compile(
    r'(?P<direction>BUY|SELL)\s+GOLD\b.*?'
    r'Entry\s*(?:Point|Price)?\s*[:\s]+\s*(?P<entry>' + _PRICE_STR + r')\b.*?'
    r'(?:Stop[-\s]?Loss|SL)\s*[:\s]+\s*(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

_GOLD_TPS_RE = re.compile(
    r'TP\s*\d+\s*[:\s]+\s*(?P<tp>' + _PRICE_STR + r')',
    re.IGNORECASE,
)


def extract_trade_signals(channel: str) -> list[dict]:
    """Extract all complete trade signals from a channel's raw messages."""
    raw_file = _RAW_DIR / f"{channel}.jsonl"
    if not raw_file.exists():
        return []

    messages = []
    for line in raw_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line: continue
        try: messages.append(json.loads(line))
        except: continue

    messages.reverse()  # chronological order
    signals = []

    for msg in messages:
        text = msg.get("raw_text", "")
        ts = msg.get("timestamp_utc", "")
        msg_id = msg.get("message_id", "")

        sgn = None

        # Try WSQ format
        m = _WSQ_SETUP_RE.search(text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG" if m.group("direction").upper() == "LONG" else "SHORT"
            entry = float(m.group("entry"))
            sl = float(m.group("sl"))

            # Extract all target prices — find the "Targets:" line
            targets_section = ""
            targets_marker = re.search(r'Targets?\s*:\s*(.+)', text, re.IGNORECASE)
            if targets_marker:
                targets_section = targets_marker.group(1)

            tps = []
            if targets_section:
                # Extract all prices from targets section
                for pm in re.finditer(r'\$?(' + _PRICE_STR + r')\$?', targets_section):
                    val = float(pm.group(1))
                    # Exclude small integers that are likely leverage (5, 10, 20...)
                    # Exclude values that are the entry/sl themselves
                    if val == int(val) and val <= 50:
                        continue
                    if abs(val - entry) < 0.0001:
                        continue
                    tps.append(val)
                tps = sorted(set(tps))

            lev_m = re.search(r'(?:Leverage|Lev)\s*:\s*(\d+)', text, re.IGNORECASE)
            leverage = int(lev_m.group(1)) if lev_m else None

            sgn = {
                "asset": asset, "direction": direction, "entry": entry,
                "sl": sl, "tps": tps, "leverage": leverage,
            }

        # Try GOLD format
        if sgn is None:
            m = _GOLD_SETUP_RE.search(text)
            if m:
                direction = "LONG" if m.group("direction").upper() == "BUY" else "SHORT"
                entry = float(m.group("entry"))
                sl = float(m.group("sl"))
                tps = [float(m.group("tp")) for m in _GOLD_TPS_RE.finditer(text)]

                sgn = {
                    "asset": "XAUUSD", "direction": direction, "entry": entry,
                    "sl": sl, "tps": tps, "leverage": None,
                }

        if sgn is None:
            continue

        signal = {
            "contract": "telegram_trade_signal.v1",
            "id": f"trade_{channel}_{msg_id}_{ts}",
            "source": "telegram_screener_bridge",
            "channel": channel,
            "parsed_at": ts,
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "pair": f"{sgn['asset']}USDT",
            "asset": sgn["asset"],
            "direction": sgn["direction"],
            "entry_price": sgn["entry"],
            "sl": sgn["sl"],
            "tp": sgn["tps"][0] if sgn["tps"] else None,
            "tps": sgn["tps"],
            "leverage": sgn["leverage"],
            "raw_text": text,
        }
        signals.append(signal)

    return signals


def archive_channel_signals(channel: str = "wallstreetqueenofficial") -> dict:
    """Archive all trade signals from a channel for trading lab consumption."""
    signals = extract_trade_signals(channel)

    if not signals:
        return {"channel": channel, "signals": 0}

    # Write per-channel archive
    out_dir = _ARCHIVE_DIR / channel
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest.json").write_text(json.dumps(signals, indent=2, default=str), encoding="utf-8")

    # Write to data_center for trading lab / perf engine
    dc_dir = _DC_TRADES
    dc_dir.mkdir(parents=True, exist_ok=True)
    (dc_dir / f"{channel}_signals.json").write_text(json.dumps(signals, indent=2, default=str), encoding="utf-8")

    # Write history index
    last_ts = signals[-1]["parsed_at"] if signals else ""
    first_ts = signals[0]["parsed_at"] if signals else ""

    return {
        "channel": channel,
        "signals": len(signals),
        "first_ts": first_ts,
        "last_ts": last_ts,
        "assets": sorted(set(s["asset"] for s in signals)),
    }


def archive_all_channels() -> dict:
    """Archive signals from all channels that produce trade setups."""
    now = datetime.now(timezone.utc).isoformat()
    channels = ["wallstreetqueenofficial", "xauusd", "forexsignals", "goldsignals"]
    results = {}

    for ch in channels:
        r = archive_channel_signals(ch)
        results[ch] = r

    summary = {
        "contract": "telegram_trade_archive.v1",
        "produced_at": now,
        "total_signals": sum(r.get("signals", 0) for r in results.values()),
        "channels": results,
    }

    _DC_TRADES.mkdir(parents=True, exist_ok=True)
    (_DC_TRADES / "latest.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    return summary
