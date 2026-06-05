"""
telegram_screener_bridge — parse raw collector messages into signals.

Reads raw JSONL files from collector_telegram/outputs/raw/,
parses them through parse_telegram_message (desk_pro/telegram/parsers),
and writes structured signals to telegram_screener/signals/.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from modules.desk_pro.telegram.parsers import parse_telegram_message

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"
_SIGNALS_DIR = _PROJECT_ROOT / "data" / "telegram_screener" / "signals"


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
    """Parse all raw messages, extract claims, write as signals."""
    now = datetime.now(timezone.utc)
    messages = read_all_raw_messages()

    if not messages:
        return []

    _SIGNALS_DIR.mkdir(parents=True, exist_ok=True)

    signals_written = []
    for msg in messages:
        # Parse through desk_pro parser
        parsed = parse_telegram_message(msg)

        if parsed.claim is None:
            continue

        # Only keep TRADE_SETUP claims with known assets
        claim = parsed.claim
        if claim.get("claim_type") != "TRADE_SETUP":
            continue

        asset = claim.get("asset", "")
        if not asset:
            continue

        # Build signal
        signal = {
            "contract": "telegram_signal.v1",
            "id": f"tg_{msg.get('message_id', '')}_{now.strftime('%Y%m%dT%H%M%S')}",
            "source": "telegram_screener_bridge",
            "signal_type": "trade",
            "channel": msg.get("channel_alias", "unknown"),
            "parsed_at": msg.get("timestamp_utc", now.isoformat()),
            "produced_at": now.isoformat(),
            "pair": f"{asset}USDT",
            "direction": claim.get("direction", "").upper(),
            "entry_price": claim.get("entry"),
            "sl": claim.get("sl"),
            "tp": claim.get("tp"),
            "confidence": "LOW",
            "raw_text": msg.get("raw_text", ""),
            "summary": f"{asset} {claim.get('direction', '')}",
        }

        # Write signal
        signal_path = _SIGNALS_DIR / f"signal_{signal['id']}.json"
        signal_path.write_text(json.dumps(signal, indent=2, default=str), encoding="utf-8")

        signals_written.append(signal)

    return signals_written


def produce_latest_index() -> dict:
    """Write a latest.json index of all signals."""
    signals = produce_telegram_signals()
    latest_path = _SIGNALS_DIR / "latest.json"

    btc_signals = [s for s in signals if s.get("pair", "").startswith("BTC")]
    eth_signals = [s for s in signals if s.get("pair", "").startswith("ETH")]

    index = {
        "contract": "telegram_signal_index.v1",
        "produced_at": datetime.now(timezone.utc).isoformat(),
        "total_signals": len(signals),
        "btc_signals": len(btc_signals),
        "eth_signals": len(eth_signals),
        "signals": [s["id"] for s in signals],
    }

    # Write individual BTC signals for the latest path
    for s in btc_signals[-5:]:
        latest_path.write_text(json.dumps(s, indent=2, default=str), encoding="utf-8")

    return index
