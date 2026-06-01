import json
from pathlib import Path

from modules.desk_pro.service.telegram_claim_reader import read_telegram_claim


FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def test_bot_vision_like_telegram_claim_is_readable(tmp_path):
    payload = {
        "input_class": "telegram_claim.v1",
        "claim_id": "tg_claim_20260531_BTCUSDT.P",
        "source": "bot_vision",
        "channel_id": "-123",
        "message_id": "msg001",
        "symbol": "BTCUSDT.P",
        "timeframe": "15m",
        "claim_ts": "2026-05-31T12:00:00Z",
        "claim_type": "trade_context",
        "text": "Support 65000, bullish trend",
        "entities": {"direction": "long", "levels": [65000.0], "confidence": 0.81},
        "refs": {"telegram_message_ref": "telegram://-123/msg001", "run_id": "run_001"},
    }
    path = tmp_path / "latest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = read_telegram_claim(path=path)
    assert result is not None
    assert result["source"] == "bot_vision"
    assert result["claim_type"] == "trade_context"
