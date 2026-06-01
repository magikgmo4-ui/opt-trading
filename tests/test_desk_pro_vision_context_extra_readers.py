import json
from pathlib import Path

from modules.desk_pro.service.vision_context_reader import (
    read_vision_context_news_sentiment,
    read_vision_context_screener,
)


FIXTURES = Path(__file__).parent / "fixtures" / "capture_mapping"


def test_read_news_sentiment_fixture(tmp_path):
    data = json.loads((FIXTURES / "vision_context_news_sentiment_v1_sample.json").read_text(encoding="utf-8"))
    path = tmp_path / "latest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    result = read_vision_context_news_sentiment(path=path)
    assert result is not None
    assert result["input_class"] == "vision_context.news_sentiment.v1"
    assert result["article_count"] == 3


def test_read_screener_fixture(tmp_path):
    data = json.loads((FIXTURES / "vision_context_screener_v1_sample.json").read_text(encoding="utf-8"))
    path = tmp_path / "latest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    result = read_vision_context_screener(path=path)
    assert result is not None
    assert result["input_class"] == "vision_context.screener.v1"
    assert result["stock_count"] == 3


def test_wrong_input_class_returns_none(tmp_path):
    path = tmp_path / "latest.json"
    path.write_text(json.dumps({"input_class": "wrong.v1"}), encoding="utf-8")
    assert read_vision_context_news_sentiment(path=path) is None
    assert read_vision_context_screener(path=path) is None
