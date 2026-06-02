from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from modules.telegram_ingestion.parser.message_schema import RawMessage


MODULE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = MODULE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from collector_telegram.config import enabled_channels, load_config  # noqa: E402
from collector_telegram.normalize import parse_message  # noqa: E402
from collector_telegram.run import run_collection, run_sanity  # noqa: E402


class FakeClient:
    def __init__(self, messages: dict[str, list[RawMessage]]):
        self.messages = messages

    def fetch_messages(self, source_ref: str, limit: int) -> list[RawMessage]:
        return self.messages.get(source_ref, [])[:limit]


def test_load_config_has_enabled_context_channels():
    config = load_config(MODULE_DIR)
    enabled = enabled_channels(config)
    aliases = {channel.alias for channel in enabled}
    assert "coinglass_alerts" in aliases
    assert "whale_alert_io" in aliases
    assert len(config.channels) >= 10


def test_parse_message_handles_trade_signal():
    raw = RawMessage(message_id="1", channel="signals", raw_text="BTCUSDT: LONG @ 65000 SL 64000 TP 66000")
    parsed = parse_message(raw)
    assert parsed["message_type"] == "TRADE_SIGNAL"
    assert parsed["parser_status"] == "parsed"
    assert parsed["parsed"]["symbol"] == "BTCUSDT"


def test_parse_message_handles_coinglass_partial_signal():
    raw = RawMessage(
        message_id="2",
        channel="coinglass_alerts",
        raw_text="实时监控：Hyperliquid巨鲸**(0x2ab2)** 以 **40x** 杠杆做多**BTC**,开仓价格 **$71567**,仓位价值**132.6万**美元.",
    )
    parsed = parse_message(raw)
    assert parsed["message_type"] == "MARKET_STRUCTURE"
    assert parsed["parser_status"] == "partial"
    assert parsed["parsed"]["symbol"] == "BTC"
    assert parsed["parsed"]["side"] == "LONG"


def test_run_collection_writes_runtime_outputs(tmp_path, monkeypatch):
    module_dir = tmp_path / "collector_telegram"
    (module_dir / "config").mkdir(parents=True)
    (module_dir / "config" / "channels.json").write_text(
        json.dumps(
            {
                "version": 1,
                "updated_at": "2026-06-02",
                "channels": [
                    {"alias": "coinglass_alerts", "source_ref": "coinglass_alerts", "enabled": True, "categories": ["context"]}
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("TELEGRAM_API_ID", "123")
    monkeypatch.setenv("TELEGRAM_API_HASH", "hash")

    fake = FakeClient(
        {
            "coinglass_alerts": [
                RawMessage(message_id="11", channel="coinglass_alerts", raw_text="BTCUSDT: LONG @ 65000"),
                RawMessage(message_id="11", channel="coinglass_alerts", raw_text="BTCUSDT: LONG @ 65000"),
                RawMessage(message_id="12", channel="coinglass_alerts", raw_text="🚨 🚨 🚨  774 $BTC (55,429,876 USD) transferred from #Kraken to unknown wallet"),
            ]
        }
    )

    result = run_collection(module_dir, channel_alias="coinglass_alerts", limit=100, client=fake)
    assert result["messages_total"] == 2
    latest = json.loads((module_dir / "outputs" / "latest.json").read_text(encoding="utf-8"))
    assert latest["summary"]["channels"] == ["coinglass_alerts"]
    raw_lines = (module_dir / "outputs" / "raw" / "coinglass_alerts.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(raw_lines) == 2


def test_run_sanity_reports_missing_env_without_crash(monkeypatch):
    monkeypatch.delenv("TELEGRAM_API_ID", raising=False)
    monkeypatch.delenv("TELEGRAM_API_HASH", raising=False)
    report = run_sanity(MODULE_DIR)
    assert report["module_id"] == "collector_telegram"
    assert report["channels_total"] >= 10
    assert report["telegram_api_id_present"] is False
    assert report["telegram_api_hash_present"] is False
