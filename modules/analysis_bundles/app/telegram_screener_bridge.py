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

# Forex pairs that should NOT have USDT appended
_FOREX_ONLY = {
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY",
    "EURGBP", "EURAUD", "EURNZD", "EURCAD", "EURCHF",
    "GBPAUD", "GBPNZD", "GBPCAD", "GBPCHF",
    "AUDNZD", "AUDCAD", "AUDCHF",
    "NZDCAD", "NZDCHF", "CADCHF",
}
_ALREADY_SUFFIXED = {"USDT", "USDC", "BUSD", "BTC", "ETH"}

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
    "xauusd_trading_signals": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "22 complete setups (XAUUSD BUY/SELL inline), top performer"},
    "xauusd_free_signals": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "11 complete setups (XAUUSD BUY/SELL inline), 2nd best"},
    "xauusd_trading_free": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "11 complete setups (XAUUSD + EURUSD), multi-asset"},
    "signalsGOLD1": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "43 complete setups (XAUUSD), TOP performer"},
    "trading_signals_gold": {"priority": "P0", "mode": "ACTIVE", "type": "trade_signal", "output": "trade",
        "note": "30 complete setups (BTC+ETH+XAUUSD), multi-asset top"},
    "USDJPY_XAUUSD_SIGNALS": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "21 complete setups (XAUUSD)"},
    "btcusdt_xauusd_eurusd_signal": {"priority": "P0", "mode": "ACTIVE", "type": "trade_signal", "output": "trade",
        "note": "13 complete setups (EURUSD+GBPUSD+XAUUSD), multi-asset"},
    "GBPUSD_FOREXSiGNAL": {"priority": "P0", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "12 complete setups (EURUSD+XAUUSD)"},

    # ── NEWLY PROMOTED (>=3 verified complete setups, 2026-06-11 scan) ──
    "angela_xauusd": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "23 clean complete (XAUUSD), 0 dirty, top performer"},
    "goldtradermofxx": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "20 clean complete (XAUUSD), 0 dirty"},
    "LexatyCryptoSignals": {"priority": "P1", "mode": "ACTIVE", "type": "trade_signal", "output": "trade",
        "note": "15 clean complete (BTCUSDT crypto futures), 0 dirty"},
    "aussieforex": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "11 clean complete (XAUUSD), 0 dirty"},
    "BTCUSDGOLDVIP_SIGNALS": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "10 clean complete (XAUUSD), 0 dirty"},
    "GOLD_FOREX_SIGN": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "10 clean complete (XAUUSD), 0 dirty"},
    "GBPUSDEURUSDXAUUSDFX_Vip1": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "9 clean complete (XAUUSD), 0 dirty"},
    "Tradinghub3_fuII": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "9 clean complete (XAUUSD), 0 dirty"},
    "gold_trading_vip": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "8 clean complete (XAUUSD), 0 dirty"},
    "goldmarket67": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "8 clean complete (XAUUSD), 0 dirty"},
    "paulgoldhunterfxsignals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "6 clean complete (XAUUSD), 0 dirty"},
    "wfr_analysis": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "6 clean complete (XAUUSD), 0 dirty"},
    "xauusd_trading_gold_signals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "6 clean complete (XAUUSD), 0 dirty"},
    "forexfever11": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "5 clean complete (XAUUSD), 0 dirty"},
    "gold_forex_signals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "5 clean complete (XAUUSD), 0 dirty"},
    "goldsnipers11": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "5 clean complete (XAUUSD), 0 dirty"},
    "vasilytradersignalforex": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "4 clean complete (XAUUSD), 0 dirty"},
    "XAUUSDGOLDsignals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "3 clean complete (XAUUSD), 0 dirty"},
    "gold_pro_trader_signals_btcusd": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "3 clean complete (XAUUSD), 0 dirty"},

    # ── PROMOTED WITH CAUTION (>=3 clean, few dirty) ──
    "forexbookspdf": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "21 clean / 1 dirty (XAUUSD)"},
    "XauusdUSpips": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "19 clean / 3 dirty (XAUUSD)"},
    "GolddExpert": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "16 clean / 1 dirty (XAUUSD)"},
    "XAUUSDSIGNALSG1": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "14 clean / 3 dirty (XAUUSD)"},
    "forex_gold_signals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "9 clean / 48 dirty (XAUUSD) — high dirty rate, review needed"},
    "robertcroakgoldsignals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "9 clean / 7 dirty (XAUUSD)"},
    "Btcusdtradingdaily": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "8 clean / 3 dirty (XAUUSD)"},
    "NASDAQ100US30GOLDFX1PIP": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "8 clean / 1 dirty (XAUUSD)"},
    "usdjpy_xauusd_forex_signals": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "4 clean / 2 dirty (XAUUSD)"},
    "BTC_USD_GOLD_FREE_SIGNALS": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "3 clean / 1 dirty (XAUUSD+BTC)"},
    "WhaleTank": {"priority": "P1", "mode": "ACTIVE", "type": "trade_signal", "output": "trade",
        "note": "3 clean / 1 dirty (XAUUSD+BTC)"},
    "XAUUSDUSDJPYEURUSDfx": {"priority": "P1", "mode": "ACTIVE", "type": "xau_signal", "output": "trade",
        "note": "3 clean / 1 dirty (XAUUSD)"},

    # ── QUALIFIED (<3 clean but has parseable trade content) ──

    # ── WATCH (has data, incomplete setups) ──
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

    # ── DISCOVERY — XAU batch, 17 validated on Telegram, pending signal qualification ──
    "xauusd_signals": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "83 msgs, 0 setups"},
    "xauusd_signals_free": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "1 msg"},
    "gold_signals_vip": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "92 msgs"},
    "xauusd_vip_signals": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "validated"},
    "gold_trading_vip": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "60 msgs"},
    "xauusd_premium": {"priority": "P2", "mode": "DISCOVERY", "type": "xau_signal", "output": "trade", "note": "validated"},
}

_DISCOVERY_MAX_MSGS = 200  # Limit DISCOVERY channels to last N messages
_BATCH_SIZE = 100          # Messages per channel per batch

# LLM/OCR gate: only top candidates
_LLM_OCR_ALLOWED_MODES = {"ACTIVE", "QUALIFIED"}


def is_llm_ocr_allowed(channel: str) -> bool:
    """Check if LLM/OCR analysis is allowed for this channel."""
    ch_info = _CHANNEL_PRIORITY.get(channel, {})
    return ch_info.get("mode") in _LLM_OCR_ALLOWED_MODES


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

        # Build pair: don't append USDT to forex pairs or already-suffixed assets
        asset_upper = asset.upper()
        if asset_upper in _FOREX_ONLY:
            pair = asset_upper
        elif any(asset_upper.endswith(s) for s in _ALREADY_SUFFIXED):
            pair = asset_upper + "USDT" if not asset_upper.endswith("USDT") else asset_upper
        elif asset_upper == "XAUUSD" or asset_upper == "GOLD" or asset_upper == "XAU":
            pair = "XAU/USD"
        else:
            pair = asset_upper + "USDT"

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
            "pair": pair,
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

    # ── Write to data_center views (structured, versioned) ──
    _DC_TG.mkdir(parents=True, exist_ok=True)
    _DC_CTX.mkdir(parents=True, exist_ok=True)

    # 1. Global latest (counter)
    (_DC_TG / "latest.json").write_text(json.dumps({
        "input_class": "telegram_signals.v1",
        "provider_id": "telegram_screener_bridge",
        "signals": len(trade_signals),
        "active_channels": len({s["channel"] for s in trade_signals}),
        "produced_at": now.isoformat(),
    }, indent=2, default=str), encoding="utf-8")

    (_DC_CTX / "latest.json").write_text(json.dumps({
        "input_class": "telegram_context.v1",
        "provider_id": "telegram_screener_bridge",
        "context_signals": len(context_signals),
        "produced_at": now.isoformat(),
    }, indent=2, default=str), encoding="utf-8")

    # 2. By symbol — one file per symbol with its signals
    by_symbol: dict[str, list[dict]] = {}
    for s in trade_signals:
        sym = s["pair"].replace("/", "_")
        by_symbol.setdefault(sym, []).append({
            "id": s["id"], "channel": s["channel"], "direction": s["direction"],
            "entry_price": s["entry_price"], "sl": s["sl"], "tp": s["tp"],
            "confidence": s["confidence"], "parsed_at": s["parsed_at"],
        })
    for sym, items in by_symbol.items():
        sym_dir = _DC_TG / "by_symbol" / sym
        sym_dir.mkdir(parents=True, exist_ok=True)
        (sym_dir / "latest.json").write_text(json.dumps({
            "input_class": "telegram_signals.by_symbol.v1",
            "symbol": sym, "total": len(items), "signals": items,
            "produced_at": now.isoformat(),
        }, indent=2, default=str), encoding="utf-8")

    # 3. By channel — one file per channel with its signals
    by_channel: dict[str, list[dict]] = {}
    for s in trade_signals:
        ch = s["channel"]
        by_channel.setdefault(ch, []).append({
            "id": s["id"], "pair": s["pair"], "direction": s["direction"],
            "entry_price": s["entry_price"], "sl": s["sl"], "tp": s["tp"],
            "confidence": s["confidence"], "parsed_at": s["parsed_at"],
        })
    for ch, items in by_channel.items():
        ch_dir = _DC_TG / "by_channel" / ch
        ch_dir.mkdir(parents=True, exist_ok=True)
        (ch_dir / "latest.json").write_text(json.dumps({
            "input_class": "telegram_signals.by_channel.v1",
            "channel": ch, "total": len(items), "signals": items,
            "produced_at": now.isoformat(),
        }, indent=2, default=str), encoding="utf-8")

    # 4. History — archive individual signals
    for s in trade_signals:
        hist_dir = _DC_TG / "history"
        hist_dir.mkdir(parents=True, exist_ok=True)
        (hist_dir / f"{s['id']}.json").write_text(json.dumps({
            "input_class": "telegram_signal.v1",
            **s,
        }, indent=2, default=str), encoding="utf-8")

    # 5. Context history
    for ctx in context_signals:
        ctx_hist = _DC_CTX / "history"
        ctx_hist.mkdir(parents=True, exist_ok=True)
        (ctx_hist / f"{ctx['id']}.json").write_text(json.dumps(ctx, indent=2, default=str), encoding="utf-8")

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

    # data_center: channel stats with proper contract
    stats_dc = {
        "input_class": "telegram_channel_stats.v1",
        "provider_id": "telegram_screener_bridge",
        **stats,
    }
    _DC_TG.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").parent.mkdir(parents=True, exist_ok=True)
    (_DC_TG / "channel_stats" / "latest.json").write_text(json.dumps(stats_dc, indent=2, default=str), encoding="utf-8")

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
