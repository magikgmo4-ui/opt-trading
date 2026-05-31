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


# ── Stub mode output ───────────────────────────────────────

class TestNewsSentimentAnalyzerStub:
    def test_analyze_returns_valid_schema(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze(sources=["coindesk"])
        assert result["input_class"] == "vision_context.news_sentiment.v1"
        assert result["article_count"] > 0
        assert len(result["articles"]) > 0

    def test_articles_have_required_fields(self):
        import importlib.util
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            from news_sentiment_analyzer import analyze
        finally:
            sys.path.pop(0)

        result = analyze(sources=["coindesk", "cointelegraph"])
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

        result = analyze(sources=["coindesk", "cointelegraph", "theblock"])
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
               "--sources", "coindesk", "cointelegraph"]
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

        result = analyze(sources=NEWS_SOURCES)
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

        r1 = analyze(sources=["coindesk"])
        r2 = analyze(sources=["coindesk"])
        assert len(r1["articles"]) == len(r2["articles"])
        for a1, a2 in zip(r1["articles"], r2["articles"]):
            assert a1["headline"] == a2["headline"]
            assert a1["score"] == a2["score"]


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
