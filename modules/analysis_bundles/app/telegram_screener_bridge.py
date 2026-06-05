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
    # ── ACTIVE (>=10 complete setups, backtested) ──
    "wallstreetqueenofficial": {"priority": "P0", "mode": "ACTIVE", "type": "trade_signal", "output": "trade",
        "note": "10 complete setups (Coin+Direction+Entry+SL+TPs), 10 assets, backtest ready"},
    "xauusd": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "8 complete setups (BUY/SELL GOLD+Entry+SL+TPs), backtest ready"},

    # ── QUALIFIED (<10 but >0 complete setups) ──
    # (none yet — wallstreetqueenofficial + xauusd promoted to ACTIVE)

    # ── WATCH (has data, <10 complete setups) ──
    "fatpigsignals": {"priority": "P1", "mode": "WATCH", "type": "trade_setup", "output": "trade",
        "note": "2 trade setups but incomplete (no entry/sl)"},
    "coinglass_alerts": {"priority": "P1", "mode": "WATCH", "type": "whale_trade", "output": "context",
        "note": "16 whale entries, no SL/TP, good for positioning context"},
    "whale_alert_io": {"priority": "P1", "mode": "WATCH", "type": "whale_alert", "output": "context",
        "note": "10 BTC/ETH flows, no trade setups, good for flow analysis"},

    # ── DISCOVERY (pending first data from collector) ──
    "gold_scalping": {"priority": "P1", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade",
        "note": "Pending data — expected GOLD scalping signals"},
    "gold_intraday": {"priority": "P1", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade",
        "note": "Pending data — expected GOLD intraday signals"},
    "forexgoldsignals": {"priority": "P1", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade",
        "note": "Pending data — expected Forex+Gold signals"},
    "fxpremiumsignals": {"priority": "P1", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade",
        "note": "Pending data — expected FX premium signals"},

    # ── CONTEXT ONLY (useful for DeskPro, not for trading) ──
    "cryptoquant_official": {"priority": "P1", "mode": "WATCH", "type": "onchain_data", "output": "context",
        "note": "On-chain analysis, no trade setups"},
    "glassnode": {"priority": "P1", "mode": "WATCH", "type": "onchain_data", "output": "context",
        "note": "On-chain analytics, no trade setups"},
    "arkhamintelligence": {"priority": "P1", "mode": "WATCH", "type": "onchain_data", "output": "context",
        "note": "Product announcements, no trade setups"},
    "forexsignals": {"priority": "P2", "mode": "WATCH", "type": "xau_signal", "output": "context",
        "note": "XAUHQ TP hits only, no complete setups"},
    "goldsignals": {"priority": "P2", "mode": "WATCH", "type": "xau_signal", "output": "context",
        "note": "XAUHQ TP hits only, no complete setups"},

    # ── REJECTED / SKIP ──
    "binancekillers": {"priority": "P2", "mode": "REJECTED", "type": "tp_hits", "output": "skip",
        "note": "TP hit reports only, no setups with entry/sl"},
    "learn2trade": {"priority": "P3", "mode": "REJECTED", "type": "education", "output": "skip",
        "note": "Educational content only, no trade signals"},
    "goldtrading": {"priority": "P3", "mode": "REJECTED", "type": "marketing", "output": "skip",
        "note": "Indonesian marketing, no trade signals"},
}

_DISCOVERY_MAX_MSGS = 200  # Limit DISCOVERY channels to last N messages


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

    # Track per-channel message counts for DISCOVERY limit
    ch_msg_counts: dict[str, int] = {}
    seen_texts: set[str] = set()  # Dedup

    for msg in messages:
        channel = msg.get("channel_alias", "unknown")
        ch_info = _CHANNEL_PRIORITY.get(channel, {"priority": "P2", "mode": "REJECTED", "type": "unknown", "output": "skip"})

        if ch_info.get("output") == "skip" or ch_info.get("mode") == "REJECTED":
            continue

        # DISCOVERY mode: limit to last N messages per channel
        if ch_info.get("mode") == "DISCOVERY":
            cnt = ch_msg_counts.get(channel, 0)
            if cnt >= _DISCOVERY_MAX_MSGS:
                continue
            ch_msg_counts[channel] = cnt + 1

        # Dedup: skip exact duplicate raw_text within same channel
        raw_key = f"{channel}:{msg.get('raw_text', '')[:80]}"
        if raw_key in seen_texts:
            continue
        seen_texts.add(raw_key)

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
        "channel": "", "priority": "P2", "mode": "REJECTED", "type": "unknown", "output": "skip",
        "total_messages": 0, "trade_setups": 0, "context_signals": 0, "skipped": 0,
        "complete_setups": 0, "tp_only_count": 0,
        "unique_assets": set(), "signals_by_asset": defaultdict(int),
        "latest_ts": None, "earliest_ts": None,
        "signals_with_entry": 0, "signals_with_sl": 0, "signals_with_tp": 0,
        "parse_rate": 0, "duplicate_rate": 0, "candidate_score": 0,
    })

    for msg in messages:
        channel = msg.get("channel_alias", "unknown")
        ch_info = _CHANNEL_PRIORITY.get(channel, {"priority": "P2", "type": "unknown", "output": "skip"})
        cd = channel_data[channel]
        cd["channel"] = channel
        cd["mode"] = ch_info.get("mode", "REJECTED")
        cd["priority"] = ch_info["priority"]
        cd["type"] = ch_info["type"]
        cd["output"] = ch_info.get("output", "skip")
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

        # Track TP-only vs complete
        is_complete = claim.get("entry") and claim.get("sl") and claim.get("tp")
        if is_complete: cd["complete_setups"] += 1
        elif not claim.get("entry") and not claim.get("sl") and claim.get("tp"): cd["tp_only_count"] += 1

    # Compute candidate scores
    stats = {"contract": "telegram_channel_stats.v1", "produced_at": now,
             "total_channels": len(channel_data), "total_messages": len(messages), "channels": []}
    for ch, cd in sorted(channel_data.items()):
        ch_info = _CHANNEL_PRIORITY.get(ch, {})
        cd["mode"] = ch_info.get("mode", "REJECTED")
        cd["unique_assets"] = sorted(cd["unique_assets"])
        cd["signals_by_asset"] = dict(cd["signals_by_asset"])
        total = cd["total_messages"]
        setups = cd["trade_setups"]
        complete = cd["complete_setups"]
        tp_only = cd["tp_only_count"]
        cd["parse_rate"] = round((setups / total) * 100, 1) if total else 0
        cd["duplicate_rate"] = 0  # Handled at message level
        cd["candidate_score"] = _compute_candidate_score(cd)
        stats["channels"].append(cd)

    _CHANNEL_STATS_DIR.mkdir(parents=True, exist_ok=True)
    (_CHANNEL_STATS_DIR / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    _DC_TG.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").parent.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    return stats


def _compute_candidate_score(cd: dict) -> int:
    """Score 0-100 for channel qualification."""
    score = 0
    # Complete setups are most important (max 50)
    complete = cd.get("complete_setups", 0)
    score += min(complete * 5, 50)
    # Parse rate (max 30)
    parse_rate = cd.get("parse_rate", 0)
    score += min(int(parse_rate / 3), 30)
    # Assets diversity (max 10)
    assets = len(cd.get("unique_assets", []))
    score += min(assets * 2, 10)
    # Message volume (max 10)
    total = cd.get("total_messages", 0)
    score += min(total // 20, 10)
    return min(score, 100)


def produce_latest_index() -> dict:
    signals = produce_telegram_signals()
    stats = produce_channel_stats()
    active = sum(1 for c in stats["channels"] if c.get("mode") == "ACTIVE")
    qualified = sum(1 for c in stats["channels"] if c.get("mode") == "QUALIFIED")
    total = sum(c["trade_setups"] for c in stats["channels"])
    return {"signals": len(signals), "total_setups": total, "active_channels": active, "qualified_channels": qualified}
