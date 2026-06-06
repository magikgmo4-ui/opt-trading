"""
signal_tracker — archive clean trade signals per channel for trading lab backtesting.

Stores signals with entry, direction (LONG/SHORT), sl, tp, tps, leverage.
Data center output: data_center/views/telegram_signals/ for perf engine consumption.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from modules.desk_pro.telegram.parsers import parse_telegram_message

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"
_ARCHIVE_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "trade_signals"
_DC_TRADES = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals" / "trade_history"


from modules.desk_pro.telegram.parsers import parse_telegram_message


def extract_trade_signals(channel: str) -> list[dict]:
    """Extract all complete trade signals using unified parser (handles all formats).
    
    Asset-agnostic: accepts any asset the parser finds (XAUUSD, BTC, ETH, APT, etc.).
    Only archives signals with direction + entry + sl.
    """
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

        parsed = parse_telegram_message({"raw_text": text, "channel_alias": channel})

        if not parsed.claim or parsed.claim.get("claim_type") != "TRADE_SETUP":
            continue

        claim = parsed.claim
        asset = claim.get("asset", "")
        direction = claim.get("direction")
        entry = claim.get("entry")
        sl = claim.get("sl")
        tps = claim.get("tps", [])

        # ── Normalize ──
        # Clean asset: remove trailing USDT suffix if present, skip fake assets
        asset_raw = asset.upper()
        if asset_raw.endswith("USDT"):
            asset_clean = asset_raw[:-4]
        else:
            asset_clean = asset_raw
        if asset_clean in ("SIGNAL", "COIN", "PAIR", "ENTRY", "STOP", "TARGET", "LONG", "SHORT", "BUY", "SELL", ""):
            continue
        if len(asset_clean) < 2:
            continue
        asset = asset_clean

        # Build pair: forex pairs keep their name; crypto gets USDT suffix
        if len(asset) == 6 and asset[3:] == "USD":  # EURUSD, GBPUSD, AUDUSD...
            pair = asset
        elif len(asset) == 3 and asset != "USD":  # BTC, ETH, SOL...
            pair = f"{asset}USDT"
        elif len(asset) == 6 and asset.endswith("JPY"):  # USDJPY, AUDJPY...
            pair = asset
        else:
            pair = f"{asset}USDT"

        # Filter TP noise: remove small integers that are likely leverage/volume, not prices
        if tps and entry:
            tps = [t for t in tps if t > entry * 0.001 or t < entry * 1000]
            tps = [t for t in tps if not (t == float(int(t)) and t <= 50)]
            tps = sorted(set(tps))

        # Quality gate: must have direction + entry + sl
        if not entry or not sl:
            continue

        signal = {
            "contract": "telegram_trade_signal.v1",
            "id": f"trade_{channel}_{msg_id}_{ts}",
            "source": "telegram_screener_bridge",
            "channel": channel,
            "parsed_at": ts,
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "pair": pair,
            "asset": asset,
            "direction": direction,
            "entry_price": entry,
            "sl": sl,
            "tp": tps[0] if tps else None,
            "tps": tps,
            "leverage": claim.get("leverage"),
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
    """Archive signals from ALL channels with raw data that produce trade setups."""
    now = datetime.now(timezone.utc).isoformat()
    results = {}

    # Process all channels with raw data
    if _RAW_DIR.exists():
        for jsonl_file in sorted(_RAW_DIR.glob("*.jsonl")):
            ch = jsonl_file.stem
            r = archive_channel_signals(ch)
            if r.get("signals", 0) > 0:
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
