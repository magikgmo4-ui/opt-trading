"""Validate News Sentiment analyzer (A-09), writer, fixtures, and DC registry."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "capture_mapping"
PROFILES_DIR = Path(__file__).resolve().parent.parent / "modules" / "bot_vision" / "headless_capture"
SCRIPTS_DIR = PROFILES_DIR / "scripts"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# ── News Sentiment Analyzer import ─────────────────────────

class TestNewsSentimentAnalyzerImport:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "news_sentiment_analyzer.py"
        spec = importlib.util.spec_from_file_location("news_sentiment_analyzer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_has_analyze_function(self):
        source = (SCRIPTS_DIR / "news_sentiment_analyzer.py").read_text(encoding="utf-8")
        assert "def analyze" in source

    def test_defines_news_sources(self):
        source = (SCRIPTS_DIR / "news_sentiment_analyzer.py").read_text(encoding="utf-8")
        assert "coindesk" in source
        assert "cointelegraph" in source
        assert "theblock" in source
        assert "FEED_URLS" in source


# ── Stub mode output ───────────────────────────────────────

class TestNewsSentimentAnalyzerStub:
    def test_analyze_returns_valid_schema(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze(sources=["coindesk"], prefer_live=False)
        assert result["input_class"] == "vision_context.news_sentiment.v1"
        assert result["article_count"] > 0
        assert len(result["articles"]) > 0
        assert result["refs"]["fetch_mode"] == "stub"

    def test_articles_have_required_fields(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze(sources=["coindesk", "cointelegraph"], prefer_live=False)
        for article in result["articles"]:
            assert "source" in article
            assert "headline" in article
            assert "sentiment" in article
            assert "score" in article
            assert isinstance(article["score"], (int, float))
            assert "topics" in article

    def test_aggregate_fields(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze(sources=["coindesk", "cointelegraph", "theblock"], prefer_live=False)
        agg = result["aggregate"]
        assert "average_sentiment_score" in agg
        assert "sentiment_label" in agg
        assert "positive_count" in agg
        assert "negative_count" in agg
        assert "neutral_count" in agg
        assert "dominant_topics" in agg
        assert result["article_count"] == agg["positive_count"] + agg["negative_count"] + agg["neutral_count"]

    def test_analyze_pipe_via_cli(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / "news_sentiment_analyzer.py"),
               "--sources", "coindesk", "cointelegraph", "--stub-only"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert data["input_class"] == "vision_context.news_sentiment.v1"
        assert data["article_count"] > 0
        assert set(data["sources_fetched"]) == {"coindesk", "cointelegraph"}

    def test_all_sources_produce_output(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze, NEWS_SOURCES
        finally:
            sys.path.pop(0)

        result = analyze(sources=NEWS_SOURCES, prefer_live=False)
        seen_sources = {a["source"] for a in result["articles"]}
        for s in NEWS_SOURCES:
            assert s in seen_sources, f"Missing articles from source: {s}"

    def test_deterministic_stub(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        r1 = analyze(sources=["coindesk"], prefer_live=False)
        r2 = analyze(sources=["coindesk"], prefer_live=False)
        assert len(r1["articles"]) == len(r2["articles"])
        for a1, a2 in zip(r1["articles"], r2["articles"]):
            assert a1["headline"] == a2["headline"]
            assert a1["score"] == a2["score"]


class TestNewsSentimentAnalyzerLiveFallback:
    def test_live_fetch_used_when_available(self, monkeypatch):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        def fake_fetch(source: str, limit: int = 5):
            return [{
                "source": source,
                "headline": f"{source} ETF inflows resume",
                "sentiment": "positive",
                "score": 0.54,
                "topics": ["bitcoin", "institutional"],
                "published_at": "2026-05-31T12:00:00Z",
                "fetch_method": "rss",
                "confidence": 0.82,
            }]

        monkeypatch.setattr("news_sentiment_analyzer._fetch_live_articles", fake_fetch)
        result = analyze(sources=["coindesk", "cointelegraph"], prefer_live=True)
        assert result["article_count"] == 2
        assert result["refs"]["fetch_mode"] == "live"
        assert all(article["fetch_method"] == "rss" for article in result["articles"])

    def test_stub_fallback_when_live_fetch_empty(self, monkeypatch):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        monkeypatch.setattr("news_sentiment_analyzer._fetch_live_articles", lambda source, limit=5: [])
        result = analyze(sources=["coindesk"], prefer_live=True)
        assert result["article_count"] > 0
        assert result["refs"]["fetch_mode"] == "stub"
        assert all(article["fetch_method"] == "stub" for article in result["articles"])

    def test_mixed_mode_when_some_sources_live(self, monkeypatch):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        def fake_fetch(source: str, limit: int = 5):
            if source == "coindesk":
                return [{
                    "source": source,
                    "headline": "Bitcoin ETF inflows grow",
                    "sentiment": "positive",
                    "score": 0.36,
                    "topics": ["bitcoin", "institutional"],
                    "published_at": "2026-05-31T12:00:00Z",
                    "fetch_method": "rss",
                    "confidence": 0.82,
                }]
            return []

        monkeypatch.setattr("news_sentiment_analyzer._fetch_live_articles", fake_fetch)
        result = analyze(sources=["coindesk", "cointelegraph"], prefer_live=True)
        assert result["refs"]["fetch_mode"] == "mixed"
        methods = {article["fetch_method"] for article in result["articles"]}
        assert methods == {"rss", "stub"}


# ── News Sentiment Writer ──────────────────────────────────

class TestNewsSentimentWriter:
    def test_import_ok(self):
        import importlib.util
        path = SCRIPTS_DIR / "news_sentiment_writer.py"
        spec = importlib.util.spec_from_file_location("news_sentiment_writer", str(path))
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"

    def test_validate_rejects_bad_input_class(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_writer import validate
        finally:
            sys.path.pop(0)

        assert validate({"input_class": "wrong"}) is False
        assert validate({"input_class": "vision_context.news_sentiment.v1", "articles": []}) is True

    def test_pipe_via_stdin(self):
        data = load_fixture("vision_context_news_sentiment_v1_sample.json")
        cmd = [sys.executable, str(SCRIPTS_DIR / "news_sentiment_writer.py"), "--dry-run", "--stdin"]
        result = subprocess.run(cmd, input=json.dumps(data), capture_output=True, text=True, timeout=15)
        assert result.returncode == 0


# ── Fixture validation ────────────────────────────────────

class TestNewsSentimentFixture:
    FIXTURE = "vision_context_news_sentiment_v1_sample.json"

    def test_required_fields(self):
        data = load_fixture(self.FIXTURE)
        assert data["input_class"] == "vision_context.news_sentiment.v1"
        assert "sources_fetched" in data
        assert "articles" in data
        assert "article_count" in data
        assert "aggregate" in data

    def test_article_structure(self):
        data = load_fixture(self.FIXTURE)
        for article in data["articles"]:
            assert "source" in article
            assert "headline" in article
            assert "sentiment" in article
            assert "score" in article
            assert isinstance(article["score"], (int, float))

    def test_article_count_matches(self):
        data = load_fixture(self.FIXTURE)
        assert data["article_count"] == len(data["articles"])

    def test_aggregate_consistency(self):
        data = load_fixture(self.FIXTURE)
        agg = data["aggregate"]
        assert agg["positive_count"] + agg["neutral_count"] + agg["negative_count"] == data["article_count"]


# ── Screen Types Registry ─────────────────────────────────

class TestScreenTypesNewsSentiment:
    def test_news_sentiment_analyzer_ref_updated(self):
        data = json.loads((PROFILES_DIR / "screen_types.json").read_text(encoding="utf-8"))
        for st in data["screen_types"]:
            if st["id"] == "NEWS_SENTIMENT":
                assert "news_sentiment_analyzer" in st["analyzer"]
                assert "A-09" in st["analyzer"]


# ── Data Center Registry ──────────────────────────────────

class TestDataCenterRegistryNews:
    DC_REGISTRY_DIR = Path(__file__).resolve().parent.parent / "modules" / "data_center" / "registry"

    def test_producer_includes_news_sentiment(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        producer_ids = {p["producer_id"] for p in data["producers"]}
        assert "bot_vision_headless__news_sentiment" in producer_ids

    def test_producer_contract_correct(self):
        data = json.loads((self.DC_REGISTRY_DIR / "producers.json").read_text(encoding="utf-8"))
        for p in data["producers"]:
            if p["producer_id"] == "bot_vision_headless__news_sentiment":
                assert p["contract_class"] == "vision_context.news_sentiment.v1"
                assert p["family"] == "vision"

    def test_consumer_includes_news_sentiment(self):
        data = json.loads((self.DC_REGISTRY_DIR / "consumers.json").read_text(encoding="utf-8"))
        consumer_ids = {c["consumer_id"] for c in data["consumers"]}
        assert "desk_pro__vision_context_news_sentiment" in consumer_ids
        assert "dashboards__news_sentiment_history" in consumer_ids


# ── Pipeline reference check ──────────────────────────────

class TestPipelineRefs:
    def test_pipeline_import_ok(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run_vision_pipeline_news",
            str(SCRIPTS_DIR / "run_vision_pipeline.py"),
        )
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            assert False, f"Import failed: {e}"
