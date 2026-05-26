"""
Contract tests for PF_DATA_CENTER.

Validates the chain:
  producer registry -> market_metrics_writer -> data/data_center/
    -> consumer registry -> Desk Pro / future surfaces

These are smoke/contract tests — no live API calls, no DB, no Telegram.
"""
import json
import tempfile
import shutil
from pathlib import Path

import pytest

from modules.data_center.layout import (
    load_producers_registry,
    load_consumers_registry,
    get_producer_dir,
)
from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    MetricsPayload,
    ProviderCoverage,
    Refs,
)
from modules.derivatives_collector.app.market_metrics_writer import (
    write_market_metrics_to_data_center,
    write_market_metrics_view,
    write_market_metrics_history_view,
    publish_market_metrics,
)
from modules.data_center.pair_snapshot_view_writer import write_pair_market_snapshot_view

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_REFS = Refs(
    primary_output="data/data_center/derivatives/derivatives_collector__binance/normalized/x.json",
    meta_output="data/data_center/derivatives/derivatives_collector__binance/normalized/x.meta.json",
    latest="data/data_center/derivatives/derivatives_collector__binance/latest.json",
    status="data/data_center/derivatives/derivatives_collector__binance/status.json",
)

_FULL_METRICS = ["open_interest", "funding_rate", "volume_futures",
                 "long_short_ratio", "liquidations_long", "liquidations_short"]

KNOWN_FALLBACKS = {"silent_empty", "stale_ok", "error", "block"}
KNOWN_COVERAGE_STATUSES = {"full", "partial", "not_proven_runtime_adapter", "spot_only"}
KNOWN_IMPL_STATUSES = {"implemented", "planned", "not_started"}


def _make_pair_snapshot_payload(symbol: str = "BTCUSDT") -> dict:
    return {
        "contract_version": "v1",
        "schema_version": "v1",
        "module_id": "collector_binance_spot",
        "provider_id": "binance_spot",
        "run_id": "20260523_000000_test",
        "generated_at": "2026-05-23T00:00:00Z",
        "entity_type": "pair_market_snapshot",
        "records": [
            {
                "pair_symbol": symbol,
                "base_asset": symbol[:3],
                "quote_asset": "USDT",
                "trading_status": "TRADING",
                "is_spot_trading_allowed": True,
                "last_price": "51200.00",
                "open_price_24h": "50500.00",
                "high_price_24h": "51500.00",
                "low_price_24h": "50000.00",
                "price_change_percent_24h": "1.25",
                "volume_base_24h": "1234.56000000",
                "volume_quote_24h": "63000000.00000000",
                "trade_count_24h": 111111,
                "window_open_at": "2026-05-23T00:00:00Z",
                "window_close_at": "2026-05-23T08:00:00Z",
                "weighted_avg_price_24h": "51000.00",
                "source": {"provider_symbol": symbol},
            }
        ],
    }


def _make_full_payload(provider_id: str, symbol: str = "BTCUSDT") -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id=provider_id,
        symbol=symbol,
        metrics_ts="2026-05-23T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="full",
            collectable_metrics=_FULL_METRICS,
            missing_metrics=[],
        ),
        metrics=MetricsPayload(
            open_interest=72145.89,
            funding_rate=0.000125,
            volume_futures=4890123456.78,
            long_short_ratio=1.8234,
            liquidations_long=987654.32,
            liquidations_short=123456.78,
        ),
        refs=_REFS,
        warnings=[],
    )


# ---------------------------------------------------------------------------
# 1. Producer registry consistency
# ---------------------------------------------------------------------------

class TestProducerRegistryConsistency:
    def setup_method(self):
        self.reg = load_producers_registry()
        self.producers = self.reg["producers"]

    def test_registry_version_is_v1(self):
        assert self.reg["registry_version"] == "v1"

    def test_all_producers_have_unique_ids(self):
        ids = [p["producer_id"] for p in self.producers]
        assert len(ids) == len(set(ids)), "duplicate producer_id found"

    def test_all_coverage_statuses_are_known(self):
        for p in self.producers:
            assert p["coverage_status"] in KNOWN_COVERAGE_STATUSES, \
                f"{p['producer_id']}: unknown coverage_status '{p['coverage_status']}'"

    def test_full_producers_have_empty_missing_metrics(self):
        for p in self.producers:
            if p["coverage_status"] == "full":
                assert p["missing_metrics"] == [], \
                    f"{p['producer_id']}: full coverage but missing_metrics is not empty"

    def test_partial_producers_have_non_empty_missing_metrics(self):
        for p in self.producers:
            if p["coverage_status"] == "partial":
                assert len(p["missing_metrics"]) > 0, \
                    f"{p['producer_id']}: partial coverage but missing_metrics is empty"

    def test_bitget_is_full_6_of_6(self):
        bitget = next(p for p in self.producers if p["producer_id"] == "derivatives_collector__bitget")
        assert bitget["coverage_status"] == "full"
        assert set(bitget["collectable_metrics"]) == set(_FULL_METRICS)
        assert bitget["missing_metrics"] == []

    def test_binance_is_full_6_of_6(self):
        binance = next(p for p in self.producers if p["producer_id"] == "derivatives_collector__binance")
        assert binance["coverage_status"] == "full"
        assert set(binance["collectable_metrics"]) == set(_FULL_METRICS)
        assert binance["missing_metrics"] == []

    def test_output_path_root_follows_dc_layout(self):
        for p in self.producers:
            root = p["output_path_root"]
            assert root.startswith("data/data_center/"), \
                f"{p['producer_id']}: output_path_root must be under data/data_center/"
            assert root.endswith("/"), \
                f"{p['producer_id']}: output_path_root must end with /"
            # pattern: data/data_center/<family>/<producer_id>/
            parts = root.rstrip("/").split("/")
            assert len(parts) == 4, \
                f"{p['producer_id']}: output_path_root must have 4 parts (data/data_center/family/id)"
            assert parts[3] == p["producer_id"], \
                f"{p['producer_id']}: last segment of output_path_root must match producer_id"


# ---------------------------------------------------------------------------
# 2. Consumer registry consistency
# ---------------------------------------------------------------------------

class TestConsumerRegistryConsistency:
    def setup_method(self):
        self.reg = load_consumers_registry()
        self.consumers = self.reg["consumers"]

    def test_registry_version_is_v1(self):
        assert self.reg["registry_version"] == "v1"

    def test_all_consumers_have_unique_ids(self):
        ids = [c["consumer_id"] for c in self.consumers]
        assert len(ids) == len(set(ids)), "duplicate consumer_id found"

    def test_all_fallbacks_are_known(self):
        for c in self.consumers:
            assert c["fallback"] in KNOWN_FALLBACKS, \
                f"{c['consumer_id']}: unknown fallback '{c['fallback']}'"

    def test_all_implementation_statuses_are_known(self):
        for c in self.consumers:
            assert c["implementation_status"] in KNOWN_IMPL_STATUSES, \
                f"{c['consumer_id']}: unknown implementation_status"

    def test_migration_needed_consumers_have_current_path(self):
        for c in self.consumers:
            if c.get("migration_needed"):
                assert c.get("read_path_current"), \
                    f"{c['consumer_id']}: migration_needed=true but read_path_current is null"

    def test_desk_pro_market_metrics_is_implemented(self):
        desk_pro = next(c for c in self.consumers if c["consumer_id"] == "desk_pro__market_metrics")
        assert desk_pro["implementation_status"] == "implemented"

    def test_desk_pro_migration_complete(self):
        """Migration done: desk_pro reads DC view, no longer needs legacy path."""
        desk_pro = next(c for c in self.consumers if c["consumer_id"] == "desk_pro__market_metrics")
        assert desk_pro["migration_needed"] is False
        assert desk_pro["read_path_current"] is None

    def test_google_sheets_market_reporting_is_implemented(self):
        sheets = next(c for c in self.consumers if c["consumer_id"] == "google_sheets__market_reporting")
        assert sheets["implementation_status"] == "implemented"
        assert sheets["validated_at"] is not None

    def test_not_implemented_consumers_remain_not_started(self):
        """Consumers without runtime readers must stay not_started — no fake runtime."""
        no_reader = {
            "telegram_screener__signal_context",
            "strategy_framework__market_context",
            "perf_engine__replay_context",
        }
        for c in self.consumers:
            if c["consumer_id"] in no_reader:
                assert c["implementation_status"] == "not_started", \
                    f"{c['consumer_id']}: no reader exists, must be not_started"

    def test_critical_consumers_have_error_fallback(self):
        """Reporting/replay consumers must not silently fail."""
        critical = {"perf_engine__replay_context", "google_sheets__market_reporting"}
        for c in self.consumers:
            if c["consumer_id"] in critical:
                assert c["fallback"] == "error", \
                    f"{c['consumer_id']}: critical consumer must have fallback=error"

    def test_localcms_is_implemented(self):
        localcms = next(c for c in self.consumers if c["consumer_id"] == "localcms__data_center_health")
        assert localcms["implementation_status"] == "implemented"

    def test_at_least_two_consumers_implemented(self):
        """CLOSE_GATE_MASTER_TARGET requires ≥2 runtime consumers."""
        implemented = [c for c in self.consumers if c["implementation_status"] == "implemented"]
        assert len(implemented) >= 2, \
            f"CLOSE_GATE_MASTER_TARGET requires ≥2 implemented consumers, got {len(implemented)}"


# ---------------------------------------------------------------------------
# 3. Registry alignment (producer ↔ consumer cross-check)
# ---------------------------------------------------------------------------

class TestRegistryAlignment:
    def setup_method(self):
        self.producers = load_producers_registry()["producers"]
        self.consumers = load_consumers_registry()["consumers"]
        self.producer_contract_classes = {p["contract_class"] for p in self.producers}

    def test_all_consumer_contract_classes_have_a_producer(self):
        """Every non-null consumer contract_class must exist in the producer registry."""
        for c in self.consumers:
            cc = c.get("contract_class")
            if cc is None:
                continue
            assert cc in self.producer_contract_classes, \
                f"{c['consumer_id']}: contract_class '{cc}' not found in any producer"

    def test_desk_pro_reads_from_contract_class_view(self):
        """Desk Pro reads from the neutral view, not from a producer_id path."""
        desk_pro = next(c for c in self.consumers if c["consumer_id"] == "desk_pro__market_metrics")
        assert "data/data_center/views/" in desk_pro["read_path"], \
            f"desk_pro read_path must use views/, got: {desk_pro['read_path']}"
        assert "bitget" not in desk_pro["read_path"], \
            "desk_pro read_path must not reference a producer_id"
        assert "binance" not in desk_pro["read_path"], \
            "desk_pro read_path must not reference a producer_id"

    def test_latest_only_consumers_read_from_view(self):
        """All latest_only market_metrics consumers read from the neutral view."""
        for c in self.consumers:
            if c.get("access_pattern") == "latest_only" and c.get("contract_class") == "market_metrics.v1":
                assert "data/data_center/views/" in c["read_path"], \
                    f"{c['consumer_id']}: latest_only consumer must read from views/"

    def test_latest_only_consumers_have_no_producer_id_in_path(self):
        """No latest_only consumer path may reference a producer_id."""
        for c in self.consumers:
            if c.get("access_pattern") == "latest_only" and c.get("contract_class") == "market_metrics.v1":
                path = c["read_path"]
                assert "bitget" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "binance" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "derivatives_collector__" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"

    def test_by_symbol_consumers_read_from_view(self):
        """All by_symbol market_metrics.v1 consumers read from the view, not producer paths."""
        for c in self.consumers:
            if c.get("access_pattern") == "by_symbol" and c.get("contract_class") == "market_metrics.v1":
                assert "data/data_center/views/" in c["read_path"], \
                    f"{c['consumer_id']}: by_symbol consumer must read from views/"

    def test_by_symbol_consumers_have_no_producer_id_in_path(self):
        """No by_symbol consumer path may reference a producer_id."""
        for c in self.consumers:
            if c.get("access_pattern") == "by_symbol" and c.get("contract_class") == "market_metrics.v1":
                path = c["read_path"]
                assert "bitget" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "binance" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "derivatives_collector__" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"

    def test_full_history_consumers_read_from_view(self):
        """All full_history market_metrics.v1 consumers read from the view, not producer paths."""
        for c in self.consumers:
            if c.get("access_pattern") == "full_history" and c.get("contract_class") == "market_metrics.v1":
                assert "data/data_center/views/" in c["read_path"], \
                    f"{c['consumer_id']}: full_history consumer must read from views/"

    def test_full_history_consumers_have_no_producer_id_in_path(self):
        """No full_history consumer path may reference a producer_id."""
        for c in self.consumers:
            if c.get("access_pattern") == "full_history" and c.get("contract_class") == "market_metrics.v1":
                path = c["read_path"]
                assert "bitget" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "binance" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "derivatives_collector__" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "normalized" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer subdir"

    def test_pair_snapshot_consumers_read_from_view(self):
        """All pair_market_snapshot.v1 consumers read from the view, not producer paths."""
        for c in self.consumers:
            if c.get("contract_class") == "pair_market_snapshot.v1":
                assert "data/data_center/views/" in c["read_path"], \
                    f"{c['consumer_id']}: pair_market_snapshot consumer must read from views/"

    def test_pair_snapshot_consumers_have_no_producer_id_in_path(self):
        """No pair_market_snapshot consumer path may reference a producer_id."""
        for c in self.consumers:
            if c.get("contract_class") == "pair_market_snapshot.v1":
                path = c["read_path"]
                assert "collector_binance_spot" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"
                assert "binance_spot" not in path, \
                    f"{c['consumer_id']}: read_path must not reference a producer_id"

    def test_no_consumer_reads_from_raw(self):
        """No production consumer should read from raw/ — that's for audit only."""
        for c in self.consumers:
            path = c.get("read_path", "")
            assert "/raw/" not in path, \
                f"{c['consumer_id']}: production consumer must not read from raw/"


# ---------------------------------------------------------------------------
# 4. Writer → Data Center path validation
# ---------------------------------------------------------------------------

class TestWriterToDataCenterChain:
    def test_binance_writer_path_matches_producer_registry(self):
        td = Path(tempfile.mkdtemp())
        try:
            payload = _make_full_payload("binance_derivatives")
            result = write_market_metrics_to_data_center(payload, root=td)
            assert result is not None
            producer = next(
                p for p in load_producers_registry()["producers"]
                if p["producer_id"] == "derivatives_collector__binance"
            )
            expected_root = td / producer["output_path_root"].rstrip("/")
            assert result["latest"] == expected_root / "latest.json"
            assert result["by_symbol"].as_posix().endswith("/by_symbol/BTCUSDT.json")
        finally:
            shutil.rmtree(td)

    def test_bitget_writer_path_matches_producer_registry(self):
        td = Path(tempfile.mkdtemp())
        try:
            payload = _make_full_payload("bitget", symbol="ETHUSDT")
            result = write_market_metrics_to_data_center(payload, root=td)
            assert result is not None
            producer = next(
                p for p in load_producers_registry()["producers"]
                if p["producer_id"] == "derivatives_collector__bitget"
            )
            expected_root = td / producer["output_path_root"].rstrip("/")
            assert result["latest"] == expected_root / "latest.json"
            assert result["by_symbol"].as_posix().endswith("/by_symbol/ETHUSDT.json")
        finally:
            shutil.rmtree(td)

    def test_binance_and_bitget_write_to_distinct_dc_paths(self):
        td = Path(tempfile.mkdtemp())
        try:
            r_binance = write_market_metrics_to_data_center(_make_full_payload("binance_derivatives"), root=td)
            r_bitget = write_market_metrics_to_data_center(_make_full_payload("bitget"), root=td)
            assert r_binance["latest"] != r_bitget["latest"]
        finally:
            shutil.rmtree(td)

    def test_written_payload_has_full_coverage(self):
        td = Path(tempfile.mkdtemp())
        try:
            payload = _make_full_payload("binance_derivatives")
            result = write_market_metrics_to_data_center(payload, root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            assert data["provider_coverage"]["status"] == "full"
            assert data["provider_coverage"]["missing_metrics"] == []
            assert len(data["provider_coverage"]["collectable_metrics"]) == 6
        finally:
            shutil.rmtree(td)

    def test_consumer_read_path_reachable_via_view_writer(self):
        """desk_pro read_path is reachable after write_market_metrics_view — any provider."""
        td = Path(tempfile.mkdtemp())
        try:
            consumers = load_consumers_registry()["consumers"]
            desk_pro = next(c for c in consumers if c["consumer_id"] == "desk_pro__market_metrics")
            result = write_market_metrics_view(
                _make_full_payload("binance_derivatives"), root=td
            )
            expected_path = td / desk_pro["read_path"]
            assert result["latest"] == expected_path, \
                f"view writer produced {result['latest']} but consumer expects {expected_path}"
        finally:
            shutil.rmtree(td)

    def test_strategy_framework_by_symbol_path_reachable_via_view_writer(self):
        """strategy_framework by_symbol read_path is reachable after write_market_metrics_view."""
        td = Path(tempfile.mkdtemp())
        try:
            consumers = load_consumers_registry()["consumers"]
            sf = next(c for c in consumers if c["consumer_id"] == "strategy_framework__market_context")
            result = write_market_metrics_view(
                _make_full_payload("binance_derivatives"), root=td
            )
            # by_symbol path for BTCUSDT (default fixture symbol)
            expected_path = td / sf["read_path"] / "BTCUSDT.json"
            assert result["by_symbol"] == expected_path, \
                f"view writer produced {result['by_symbol']} but strategy_framework expects {expected_path}"
            assert result["by_symbol"].exists()
        finally:
            shutil.rmtree(td)

    def test_desk_pro_spot_snapshot_path_reachable_via_view_writer(self):
        """desk_pro__spot_snapshot read_path is reachable after write_pair_market_snapshot_view."""
        td = Path(tempfile.mkdtemp())
        try:
            consumers = load_consumers_registry()["consumers"]
            snap = next(c for c in consumers if c["consumer_id"] == "desk_pro__spot_snapshot")
            result = write_pair_market_snapshot_view(_make_pair_snapshot_payload(), root=td)
            expected_path = td / snap["read_path"]
            assert result["latest"] == expected_path, \
                f"view writer produced {result['latest']} but consumer expects {expected_path}"
            assert result["latest"].exists()
            path_str = result["latest"].as_posix()
            assert "collector_binance_spot" not in path_str
            assert "views/pair_market_snapshot" in path_str
        finally:
            shutil.rmtree(td)

    def test_perf_engine_history_path_reachable_via_history_writer(self):
        """perf_engine full_history read_path is reachable after write_market_metrics_history_view."""
        td = Path(tempfile.mkdtemp())
        try:
            consumers = load_consumers_registry()["consumers"]
            perf = next(c for c in consumers if c["consumer_id"] == "perf_engine__replay_context")
            result = write_market_metrics_history_view(
                _make_full_payload("bitget"), root=td, run_id="20260523T000000Z"
            )
            assert result is not None
            # history path: read_path/<SYMBOL>/<run_id>.json
            expected_base = td / perf["read_path"] / "BTCUSDT"
            assert result["history"].parent == expected_base
            assert result["history"].exists()
            path_str = str(result["history"])
            assert "bitget" not in path_str
            assert "derivatives_collector__" not in path_str
        finally:
            shutil.rmtree(td)


# ---------------------------------------------------------------------------
# 5. Desk Pro chain (end-to-end smoke)
# ---------------------------------------------------------------------------

class TestDeskProChain:
    def test_full_publish_and_deskpro_reader(self):
        """Full chain: write to Data Center + Desk Pro view -> reader finds metrics."""
        from modules.desk_pro.service.market_metrics_reader import read_market_metrics
        td = Path(tempfile.mkdtemp())
        try:
            payload = _make_full_payload("binance_derivatives")
            result = publish_market_metrics(payload, root=td)
            assert result is not None
            assert result["data_center"] is not None
            assert result["view"] is not None
            assert result["deskpro"] is not None
            # Desk Pro reader reads from the deskpro view (pre-migration path)
            metrics = read_market_metrics(path=result["deskpro"]["latest"])
            assert len(metrics) > 0
            metric_names = {m.metric for m in metrics}
            assert "open_interest" in metric_names
            assert "long_short_ratio" in metric_names
            assert "liquidations_long" in metric_names
        finally:
            shutil.rmtree(td)

    def test_dc_latest_is_valid_market_metrics_v1(self):
        """Data Center latest.json passes market_metrics.v1 contract validation."""
        td = Path(tempfile.mkdtemp())
        try:
            payload = _make_full_payload("bitget")
            result = write_market_metrics_to_data_center(payload, root=td)
            data = json.loads(result["latest"].read_text(encoding="utf-8"))
            # Reconstruct and validate via the dataclass
            rebuilt = MarketMetricsV1(
                contract_version=data["contract_version"],
                input_class=data["input_class"],
                module_id=data["module_id"],
                provider_id=data["provider_id"],
                symbol=data["symbol"],
                metrics_ts=data["metrics_ts"],
                freshness_state=data["freshness_state"],
                provider_coverage=ProviderCoverage(**data["provider_coverage"]),
                metrics=MetricsPayload(**data["metrics"]),
                refs=Refs(**data["refs"]),
                warnings=data.get("warnings", []),
            )
            assert rebuilt.validate() is True
        finally:
            shutil.rmtree(td)

    def test_desk_pro_reader_returns_empty_without_dc_write(self):
        """Without any write, Desk Pro reader degrades gracefully to empty list."""
        from modules.desk_pro.service.market_metrics_reader import read_market_metrics
        td = Path(tempfile.mkdtemp())
        try:
            fake_path = td / "nonexistent.json"
            metrics = read_market_metrics(path=fake_path)
            assert metrics == []
        finally:
            shutil.rmtree(td)
