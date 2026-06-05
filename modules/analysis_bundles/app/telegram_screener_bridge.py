"""
telegram_screener_bridge — parse raw collector messages into signals + context.

Outputs:
- Trade signals: direction + entry + sl/tp required (xauusd, wallstreetqueenofficial)
- Context signals: whale flows, coinglass alerts, onchain data (for DeskPro)
- Channel quality stats per channel
"""

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from modules.desk_pro.telegram.parsers import parse_telegram_message

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"
_SIGNALS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "signals"
_CONTEXT_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "context_signals"
_CHANNEL_STATS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "channel_stats"
_DC_TG = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals"
_DC_CTX = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_context"

_CHANNEL_PRIORITY = {
    "coinglass_alerts": {"priority": "P1", "type": "whale_trade", "output": "context"},
    "fatpigsignals": {"priority": "P0", "type": "trade_setup", "output": "trade"},
    "binancekillers": {"priority": "P1", "type": "tp_hits", "output": "skip"},
    "cryptoquant_official": {"priority": "P1", "type": "onchain_data", "output": "context"},
    "glassnode": {"priority": "P1", "type": "onchain_data", "output": "context"},
    "arkhamintelligence": {"priority": "P1", "type": "onchain_data", "output": "context"},
    "whale_alert_io": {"priority": "P1", "type": "whale_alert", "output": "context"},
    "forexsignals": {"priority": "P1", "type": "xau_signal", "output": "trade"},
    "goldsignals": {"priority": "P1", "type": "xau_signal", "output": "trade"},
    "xauusd": {"priority": "P0", "type": "xau_signal", "output": "trade"},
    "wallstreetqueenofficial": {"priority": "P1", "type": "trade_signal", "output": "trade"},
    "learn2trade": {"priority": "P2", "type": "education", "output": "skip"},
    "goldtrading": {"priority": "Bruit", "type": "marketing", "output": "skip"},
    # New channels (enabled 2026-06-05)
    "gold_scalping": {"priority": "P1", "type": "xau_signal", "output": "trade"},
    "gold_intraday": {"priority": "P1", "type": "xau_signal", "output": "trade"},
    "forexgoldsignals": {"priority": "P1", "type": "xau_signal", "output": "trade"},
    "fxpremiumsignals": {"priority": "P1", "type": "xau_signal", "output": "trade"},
}


def read_all_raw_messages() -> list[dict]:
    messages = []
    if not _RAW_DIR.exists():
        return messages
    for jsonl_file in sorted(_RAW_DIR.glob("*.jsonl")):
        try:
            for line in jsonl_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line: continue
                try:
                    msg = json.loads(line)
                    if isinstance(msg, dict) and msg.get("raw_text"):
                        messages.append(msg)
                except json.JSONDecodeError: continue
        except Exception: continue
    return messages


def produce_telegram_signals() -> list[dict]:
    """Parse raw messages, produce trade signals + context signals."""
    now = datetime.now(timezone.utc)
    messages = read_all_raw_messages()
    if not messages: return []

    # Clean old files
    _SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
    _CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    for old in list(_SIGNALS_DIR.glob("signal_*.json")) + list(_CONTEXT_DIR.glob("ctx_*.json")):
        old.unlink()

    trade_signals = []
    context_signals = []

    for msg in messages:
        channel = msg.get("channel_alias", "unknown")
        ch_info = _CHANNEL_PRIORITY.get(channel, {"priority": "P2", "type": "unknown", "output": "skip"})
        if ch_info["output"] == "skip":
            continue

        ts = msg.get("timestamp_utc", now.isoformat())
        parsed = parse_telegram_message(msg)

        if parsed.claim is None:
            continue

        claim = parsed.claim
        claim_type = claim.get("claim_type", "TRADE_SETUP")

        # Route to context signals
        if claim_type == "CRYPTO_FLOW" or ch_info["output"] == "context":
            ctx = {
                "contract": "telegram_context.v1",
                "id": f"ctx_{msg.get('message_id', '')}_{now.strftime('%Y%m%dT%H%M%S')}",
                "source": "telegram_screener_bridge",
                "signal_type": claim_type.lower() if claim_type == "CRYPTO_FLOW" else ch_info["type"],
                "channel": channel,
                "channel_priority": ch_info["priority"],
                "channel_type": ch_info["type"],
                "parsed_at": ts,
                "produced_at": now.isoformat(),
                "asset": claim.get("asset"),
                "direction": claim.get("direction"),
                "entry_price": claim.get("entry"),
                "amount": claim.get("amount"),
                "value_usd": claim.get("value_usd"),
                "raw_text": msg.get("raw_text", ""),
            }
            ctx_path = _CONTEXT_DIR / f"ctx_{ctx['id']}.json"
            ctx_path.write_text(json.dumps(ctx, indent=2, default=str), encoding="utf-8")
            context_signals.append(ctx)
            continue

        if claim_type != "TRADE_SETUP":
            continue

        asset = claim.get("asset", "")
        direction = claim.get("direction")
        has_price = claim.get("entry") or claim.get("sl") or claim.get("tp")
        if not asset or not direction or not has_price:
            continue

        signal = {
            "contract": "telegram_signal.v1",
            "id": f"tg_{msg.get('message_id', '')}_{now.strftime('%Y%m%dT%H%M%S')}",
            "source": "telegram_screener_bridge",
            "signal_type": "trade",
            "channel": channel,
            "channel_priority": ch_info["priority"],
            "channel_type": ch_info["type"],
            "parsed_at": ts,
            "produced_at": now.isoformat(),
            "pair": f"{asset}USDT",
            "direction": direction.upper() if direction else None,
            "entry_price": claim.get("entry"),
            "sl": claim.get("sl"),
            "tp": claim.get("tp"),
            "tps": claim.get("tps", []),
            "leverage": claim.get("leverage"),
            "confidence": "LOW",
            "raw_text": msg.get("raw_text", ""),
            "summary": f"{asset} {direction}",
        }
        sig_path = _SIGNALS_DIR / f"signal_{signal['id']}.json"
        sig_path.write_text(json.dumps(signal, indent=2, default=str), encoding="utf-8")
        trade_signals.append(signal)

    # Write latest.json for trade signals
    (_SIGNALS_DIR / "latest.json").write_text(json.dumps({
        "total": len(trade_signals),
        "produced_at": now.isoformat(),
    }, indent=2), encoding="utf-8")

    # Write context index
    (_CONTEXT_DIR / "latest.json").write_text(json.dumps({
        "total": len(context_signals),
        "produced_at": now.isoformat(),
    }, indent=2), encoding="utf-8")

    # Write to data_center views
    _DC_TG.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "latest.json").write_text(json.dumps({"signals": len(trade_signals), "produced_at": now.isoformat()}, indent=2), encoding="utf-8")

    _DC_CTX.mkdir(parents=True, exist_ok=True)
    (_DC_CTX / "latest.json").write_text(json.dumps({"context_signals": len(context_signals), "produced_at": now.isoformat()}, indent=2), encoding="utf-8")

    return trade_signals


def produce_channel_stats() -> dict:
    messages = read_all_raw_messages()
    now = datetime.now(timezone.utc).isoformat()

    channel_data: dict[str, dict] = defaultdict(lambda: {
        "channel": "", "priority": "P2", "type": "unknown", "output": "skip",
        "total_messages": 0, "trade_setups": 0, "context_signals": 0, "skipped": 0,
        "unique_assets": set(), "signals_by_asset": defaultdict(int),
        "latest_ts": None, "earliest_ts": None,
        "signals_with_entry": 0, "signals_with_sl": 0, "signals_with_tp": 0,
    })

    for msg in messages:
        channel = msg.get("channel_alias", "unknown")
        ch_info = _CHANNEL_PRIORITY.get(channel, {"priority": "P2", "type": "unknown", "output": "skip"})
        cd = channel_data[channel]
        cd["channel"] = channel
        cd["priority"] = ch_info["priority"]
        cd["type"] = ch_info["type"]
        cd["output"] = ch_info["output"]
        cd["total_messages"] += 1

        ts = msg.get("timestamp_utc", "")
        if ts:
            if cd["latest_ts"] is None or ts > cd["latest_ts"]: cd["latest_ts"] = ts
            if cd["earliest_ts"] is None or ts < cd["earliest_ts"]: cd["earliest_ts"] = ts

        parsed = parse_telegram_message(msg)
        if not parsed.claim: continue

        claim = parsed.claim
        claim_type = claim.get("claim_type", "TRADE_SETUP")

        if ch_info["output"] == "skip":
            cd["skipped"] += 1
            continue

        if claim_type == "CRYPTO_FLOW" or ch_info["output"] == "context":
            cd["context_signals"] += 1
            asset = claim.get("asset", "?")
            cd["unique_assets"].add(asset)
            continue

        if claim_type != "TRADE_SETUP": continue

        asset = claim.get("asset", "?")
        direction = claim.get("direction")
        has_price = claim.get("entry") or claim.get("sl") or claim.get("tp")
        if not asset or not direction or not has_price: continue

        cd["trade_setups"] += 1
        cd["unique_assets"].add(asset)
        cd["signals_by_asset"][asset] += 1
        if claim.get("entry"): cd["signals_with_entry"] += 1
        if claim.get("sl"): cd["signals_with_sl"] += 1
        if claim.get("tp"): cd["signals_with_tp"] += 1

    stats = {"contract": "telegram_channel_stats.v1", "produced_at": now,
             "total_channels": len(channel_data), "total_messages": len(messages), "channels": []}
    for ch, cd in sorted(channel_data.items()):
        cd["unique_assets"] = sorted(cd["unique_assets"])
        cd["signals_by_asset"] = dict(cd["signals_by_asset"])
        stats["channels"].append(cd)

    _CHANNEL_STATS_DIR.mkdir(parents=True, exist_ok=True)
    (_CHANNEL_STATS_DIR / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    _DC_TG.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").parent.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    return stats


def produce_latest_index() -> dict:
    signals = produce_telegram_signals()
    stats = produce_channel_stats()
    return {"signals": len(signals), "good_channels": sum(1 for c in stats["channels"] if c["trade_setups"] > 0)}
