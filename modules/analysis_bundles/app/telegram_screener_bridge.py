"""
telegram_screener_bridge — parse raw collector messages into signals with channel stats.

Reads raw JSONL files from collector_telegram/outputs/raw/,
parses them through parse_telegram_message (with whitelist),
classifies by channel with timestamps,
writes structured signals + per-channel quality stats.
"""

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from modules.desk_pro.telegram.parsers import parse_telegram_message

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"
_SIGNALS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "signals"
_CHANNEL_STATS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "channel_stats"
_DATA_CENTER_TG = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals"

# Channel priority classification
_CHANNEL_PRIORITY = {
    "coinglass_alerts": {"priority": "P0", "type": "whale_trade", "note": "Coinglass whale alerts — Hyperliquid + exchange flows"},
    "fatpigsignals": {"priority": "P0", "type": "trade_setup", "note": "Fat Pig Signals — trade setups with entry/sl/tp"},
    "binancekillers": {"priority": "P1", "type": "trade_signal", "note": "Binance Killers — trade signals"},
    "cryptoquant_official": {"priority": "P1", "type": "onchain_data", "note": "CryptoQuant — on-chain metrics, exchange flows"},
    "glassnode": {"priority": "P1", "type": "onchain_data", "note": "Glassnode — on-chain analytics"},
    "arkhamintelligence": {"priority": "P1", "type": "onchain_data", "note": "Arkham Intelligence — wallet tracking"},
    "whale_alert_io": {"priority": "P1", "type": "whale_alert", "note": "Whale Alert — large transactions"},
    "forexsignals": {"priority": "P2", "type": "trade_signal", "note": "Forex Signals — FX trade ideas"},
    "learn2trade": {"priority": "P2", "type": "trade_signal", "note": "Learn2Trade — educational + signals"},
    "goldsignals": {"priority": "P2", "type": "trade_signal", "note": "Gold Signals — XAU focused"},
    "goldtrading": {"priority": "P2", "type": "trade_signal", "note": "Gold Trading — XAU focused"},
    "wallstreetqueenofficial": {"priority": "Bruit", "type": "noise", "note": "WallStreetQueen — unverified signals"},
    "xauusd": {"priority": "Bruit", "type": "noise", "note": "XAUUSD — likely copy/repost"},
}


def read_all_raw_messages() -> list[dict]:
    """Read all raw JSONL messages from collector output."""
    messages = []
    if not _RAW_DIR.exists():
        return messages

    for jsonl_file in sorted(_RAW_DIR.glob("*.jsonl")):
        try:
            for line in jsonl_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if isinstance(msg, dict) and msg.get("raw_text"):
                        messages.append(msg)
                except json.JSONDecodeError:
                    continue
        except Exception:
            continue

    return messages


def produce_telegram_signals() -> list[dict]:
    """Parse all raw messages, extract claims, write signals per channel with timestamps."""
    now = datetime.now(timezone.utc)
    messages = read_all_raw_messages()

    if not messages:
        return []

    _SIGNALS_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old signal files before regenerating
    for old in _SIGNALS_DIR.glob("signal_*.json"):
        old.unlink()

    signals_written = []
    for msg in messages:
        parsed = parse_telegram_message(msg)

        # Track all parsed types for stats
        channel = msg.get("channel_alias", "unknown")
        ts = msg.get("timestamp_utc", now.isoformat())

        if parsed.claim is None:
            continue

        claim = parsed.claim
        if claim.get("claim_type") != "TRADE_SETUP":
            continue

        asset = claim.get("asset", "")
        if not asset:
            continue

        signal = {
            "contract": "telegram_signal.v1",
            "id": f"tg_{msg.get('message_id', '')}_{now.strftime('%Y%m%dT%H%M%S')}",
            "source": "telegram_screener_bridge",
            "signal_type": "trade",
            "channel": channel,
            "channel_priority": _CHANNEL_PRIORITY.get(channel, {}).get("priority", "P2"),
            "channel_type": _CHANNEL_PRIORITY.get(channel, {}).get("type", "unknown"),
            "parsed_at": ts,
            "produced_at": now.isoformat(),
            "pair": f"{asset}USDT",
            "direction": claim.get("direction", "").upper(),
            "entry_price": claim.get("entry"),
            "sl": claim.get("sl"),
            "tp": claim.get("tp"),
            "tps": claim.get("tps", []),
            "leverage": claim.get("leverage"),
            "confidence": "LOW",
            "raw_text": msg.get("raw_text", ""),
            "summary": f"{asset} {claim.get('direction', '')}",
        }

        # Write per-signal file
        signal_path = _SIGNALS_DIR / f"signal_{signal['id']}.json"
        signal_path.write_text(json.dumps(signal, indent=2, default=str), encoding="utf-8")
        signals_written.append(signal)

    return signals_written


def produce_channel_stats() -> dict:
    """Analyze all messages per channel and produce quality statistics."""
    messages = read_all_raw_messages()
    now = datetime.now(timezone.utc).isoformat()

    channel_data: dict[str, dict] = defaultdict(lambda: {
        "channel": "",
        "priority": "P2",
        "type": "unknown",
        "note": "",
        "total_messages": 0,
        "trade_setups": 0,
        "noise_count": 0,
        "unique_assets": set(),
        "signals_by_asset": defaultdict(int),
        "latest_ts": None,
        "earliest_ts": None,
        "signals_with_entry": 0,
        "signals_with_sl": 0,
        "signals_with_tp": 0,
        "avg_leverage": 0.0,
        "leverage_count": 0,
    })

    for msg in messages:
        channel = msg.get("channel_alias", "unknown")
        ts = msg.get("timestamp_utc", "")

        info = _CHANNEL_PRIORITY.get(channel, {"priority": "P2", "type": "unknown", "note": ""})
        cd = channel_data[channel]
        cd["channel"] = channel
        cd["priority"] = info.get("priority", "P2")
        cd["type"] = info.get("type", "unknown")
        cd["note"] = info.get("note", "")
        cd["total_messages"] += 1

        if ts:
            if cd["latest_ts"] is None or ts > cd["latest_ts"]:
                cd["latest_ts"] = ts
            if cd["earliest_ts"] is None or ts < cd["earliest_ts"]:
                cd["earliest_ts"] = ts

        parsed = parse_telegram_message(msg)
        if parsed.message_type == "TRADE_SETUP" and parsed.claim:
            cd["trade_setups"] += 1
            asset = parsed.claim.get("asset", "?")
            cd["unique_assets"].add(asset)
            cd["signals_by_asset"][asset] += 1
            if parsed.claim.get("entry"):
                cd["signals_with_entry"] += 1
            if parsed.claim.get("sl"):
                cd["signals_with_sl"] += 1
            if parsed.claim.get("tp") or parsed.claim.get("tps"):
                cd["signals_with_tp"] += 1
            if parsed.claim.get("leverage"):
                cd["leverage_count"] += 1
                cd["avg_leverage"] += parsed.claim["leverage"]
        else:
            cd["noise_count"] += 1

    # Build final stats
    stats = {
        "contract": "telegram_channel_stats.v1",
        "produced_at": now,
        "total_channels": len(channel_data),
        "total_messages": len(messages),
        "channels": [],
    }

    for ch, cd in sorted(channel_data.items()):
        cd["unique_assets"] = sorted(cd["unique_assets"])
        cd["signals_by_asset"] = dict(cd["signals_by_asset"])
        if cd["leverage_count"] > 0:
            cd["avg_leverage"] = round(cd["avg_leverage"] / cd["leverage_count"], 1)
        else:
            cd["avg_leverage"] = 0.0
        stats["channels"].append(cd)

    # Write to data_center
    _CHANNEL_STATS_DIR.mkdir(parents=True, exist_ok=True)
    (_CHANNEL_STATS_DIR / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    # Also write to data_center views for DeskPro
    _DATA_CENTER_TG.mkdir(parents=True, exist_ok=True)
    (_DATA_CENTER_TG / "channel_stats" / "latest.json").parent.mkdir(parents=True, exist_ok=True)
    (_DATA_CENTER_TG / "channel_stats" / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    return stats


def produce_latest_index() -> dict:
    """Generate signals, stats, and return summary."""
    signals = produce_telegram_signals()
    stats = produce_channel_stats()

    latest_path = _SIGNALS_DIR / "latest.json"
    btc_signals = [s for s in signals if s.get("pair", "").startswith("BTC")]

    # Write per-channel latest files
    _DATA_CENTER_TG.mkdir(parents=True, exist_ok=True)
    (_DATA_CENTER_TG / "latest.json").write_text(
        json.dumps({
            "contract": "telegram_signal_index.v1",
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "total_signals": len(signals),
            "btc_signals": len(btc_signals),
            "channels": stats["total_channels"],
            "total_messages": stats["total_messages"],
        }, indent=2),
        encoding="utf-8",
    )

    # Write latest BTC signal for bundle reader
    if btc_signals:
        latest_path.write_text(json.dumps(btc_signals[-1], indent=2, default=str), encoding="utf-8")

    return {"signals": len(signals), "btc": len(btc_signals), "channels": stats["total_channels"]}
