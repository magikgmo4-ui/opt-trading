import json
from pathlib import Path


HEADLESS_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"


def test_telegram_mapping_exists_and_covers_all_screen_types():
    mapping = json.loads((HEADLESS_DIR / "telegram_mapping.json").read_text(encoding="utf-8"))
    screen_types = json.loads((HEADLESS_DIR / "screen_types.json").read_text(encoding="utf-8"))
    mapped = {row["screen_type"] for row in mapping["routes"]}
    expected = {row["id"] for row in screen_types["screen_types"]}
    assert mapped == expected


def test_deskpro_mapping_exists_and_covers_all_screen_types():
    mapping = json.loads((HEADLESS_DIR / "deskpro_mapping.json").read_text(encoding="utf-8"))
    screen_types = json.loads((HEADLESS_DIR / "screen_types.json").read_text(encoding="utf-8"))
    mapped = {row["screen_type"] for row in mapping["routes"]}
    expected = {row["id"] for row in screen_types["screen_types"]}
    assert mapped == expected


def test_chart_telegram_route_uses_filter_and_send():
    mapping = json.loads((HEADLESS_DIR / "telegram_mapping.json").read_text(encoding="utf-8"))
    row = next(r for r in mapping["routes"] if r["screen_type"] == "CHART_TECHNICAL")
    assert row["summary_source"] == "telegram_filter"
    assert row["delivery"] == "send_telegram"


def test_news_and_screener_deskpro_paths_are_dedicated():
    mapping = json.loads((HEADLESS_DIR / "deskpro_mapping.json").read_text(encoding="utf-8"))
    news = next(r for r in mapping["routes"] if r["screen_type"] == "NEWS_SENTIMENT")
    screener = next(r for r in mapping["routes"] if r["screen_type"] == "SCREENER_STOCKS")
    assert news["deskpro_path"].endswith("vision_context/news_sentiment/latest.json")
    assert screener["deskpro_path"].endswith("vision_context/screener/latest.json")
