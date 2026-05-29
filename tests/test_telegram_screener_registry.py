from pathlib import Path

import pytest

from modules.telegram_screener.registry import (
    Channel,
    ChannelRegistry,
    TrustTier,
    load_channel_registry,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class TestModels:
    def test_channel_defaults(self):
        c = Channel(alias="TG_SRC_TEST_01", kind="channel", title="Test", trust_tier=TrustTier.C)
        assert c.alias == "TG_SRC_TEST_01"
        assert c.enabled is False
        assert c.categories == []
        assert c.expected_parsers == []

    def test_channel_enabled_true(self):
        c = Channel(alias="TG_SRC_TEST_01", kind="channel", title="Test", trust_tier=TrustTier.A, enabled=True)
        assert c.enabled is True

    def test_trust_tier_values(self):
        assert TrustTier.A.value == "A"
        assert TrustTier.B.value == "B"
        assert TrustTier.C.value == "C"
        assert TrustTier.D.value == "D"

    def test_registry_methods(self):
        c1 = Channel(alias="TG_SRC_A_01", kind="channel", title="A", trust_tier=TrustTier.A, enabled=True,
                     categories=["signals"])
        c2 = Channel(alias="TG_SRC_B_01", kind="channel", title="B", trust_tier=TrustTier.B, enabled=False,
                     categories=["news"])
        c3 = Channel(alias="TG_SRC_C_01", kind="channel", title="C", trust_tier=TrustTier.C, enabled=True,
                     categories=["signals"])
        reg = ChannelRegistry(version=1, updated_at="2026-05-28", channels=[c1, c2, c3])

        enabled = reg.enabled_channels()
        assert len(enabled) == 2
        assert reg.by_tier(TrustTier.A) == [c1]
        assert len(reg.by_tier(TrustTier.C)) == 1
        assert len(reg.by_category("signals")) == 2
        assert len(reg.by_category("news")) == 1
        assert reg.by_alias("TG_SRC_B_01") == c2
        assert reg.by_alias("NONEXISTENT") is None


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

class TestLoader:
    def test_load_default_registry(self):
        reg = load_channel_registry()
        assert reg.version == 1
        assert len(reg.channels) >= 2

    def test_load_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_channel_registry(Path("/nonexistent/path.yaml"))

    def test_load_valid_yaml(self, tmp_path: Path):
        path = tmp_path / "registry.yaml"
        path.write_text("""
version: 1
updated_at: "2026-05-28"
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        reg = load_channel_registry(path)
        assert len(reg.channels) == 1
        assert reg.channels[0].alias == "TG_SRC_TEST_01"

    def test_load_wrong_version(self, tmp_path: Path):
        path = tmp_path / "bad_version.yaml"
        path.write_text("version: 2\nchannels: []", encoding="utf-8")
        with pytest.raises(ValueError, match="Unsupported registry version"):
            load_channel_registry(path)

    def test_load_invalid_alias(self, tmp_path: Path):
        path = tmp_path / "bad_alias.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "bad_alias"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid alias"):
            load_channel_registry(path)

    def test_load_invalid_tier(self, tmp_path: Path):
        path = tmp_path / "bad_tier.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "E"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid trust_tier"):
            load_channel_registry(path)

    def test_load_invalid_kind(self, tmp_path: Path):
        path = tmp_path / "bad_kind.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "bot"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid kind"):
            load_channel_registry(path)

    def test_load_malformed_yaml(self, tmp_path: Path):
        path = tmp_path / "malformed.yaml"
        path.write_text("{bad yaml: [", encoding="utf-8")
        with pytest.raises(Exception):
            load_channel_registry(path)

    def test_load_not_a_mapping(self, tmp_path: Path):
        path = tmp_path / "scalar.yaml"
        path.write_text("just a string", encoding="utf-8")
        with pytest.raises(ValueError, match="must be a YAML mapping"):
            load_channel_registry(path)

    def test_load_empty_categories_raises(self, tmp_path: Path):
        path = tmp_path / "empty_cat.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: []
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        with pytest.raises(ValueError, match="categories must be non-empty"):
            load_channel_registry(path)

    def test_load_empty_parsers_raises(self, tmp_path: Path):
        path = tmp_path / "empty_parsers.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: []
""", encoding="utf-8")
        with pytest.raises(ValueError, match="expected_parsers must be non-empty"):
            load_channel_registry(path)

    def test_enabled_false_by_default(self, tmp_path: Path):
        path = tmp_path / "default_disabled.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
""", encoding="utf-8")
        reg = load_channel_registry(path)
        assert reg.channels[0].enabled is False

    def test_enabled_true(self, tmp_path: Path):
        path = tmp_path / "enabled.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_TEST_01"
    kind: "channel"
    title: "Test"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
    enabled: true
""", encoding="utf-8")
        reg = load_channel_registry(path)
        assert reg.channels[0].enabled is True

    def test_registry_queries(self, tmp_path: Path):
        path = tmp_path / "multi.yaml"
        path.write_text("""
version: 1
channels:
  - alias: "TG_SRC_A_01"
    kind: "channel"
    title: "A"
    trust_tier: "A"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
    enabled: true
  - alias: "TG_SRC_B_01"
    kind: "channel"
    title: "B"
    trust_tier: "B"
    categories: ["news"]
    expected_parsers: ["news"]
    enabled: false
  - alias: "TG_SRC_C_01"
    kind: "channel"
    title: "C"
    trust_tier: "C"
    categories: ["signals"]
    expected_parsers: ["trade_claim"]
    enabled: true
""", encoding="utf-8")
        reg = load_channel_registry(path)
        assert len(reg.enabled_channels()) == 2
        assert len(reg.by_tier(TrustTier.A)) == 1
        assert len(reg.by_category("signals")) == 2
        assert reg.by_alias("TG_SRC_B_01") is not None

    def test_default_registry_has_placeholder_channels(self):
        reg = load_channel_registry()
        assert reg.by_alias("TG_SRC_SIGNALS_01") is not None
        assert reg.by_alias("TG_SRC_NEWS_01") is not None
        signals = reg.by_alias("TG_SRC_SIGNALS_01")
        assert signals is not None
        assert signals.enabled is False
        assert TrustTier.C in (signals.trust_tier,)
        news = reg.by_alias("TG_SRC_NEWS_01")
        assert news is not None
        assert news.enabled is True
