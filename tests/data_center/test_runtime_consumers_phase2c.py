import tempfile
from pathlib import Path

from modules.derivatives_collector.app.market_metrics_v1 import (
    MarketMetricsV1,
    MetricsPayload,
    ProviderCoverage,
    Refs,
)
from modules.derivatives_collector.app.market_metrics_writer import (
    write_market_metrics_history_view,
    write_market_metrics_view,
)
from modules.perf_engine.replay_context_reader import read_replay_context
from modules.strategy.market_context_reader import read_market_context


def _payload(provider_id: str = "binance_derivatives", symbol: str = "BTCUSDT") -> MarketMetricsV1:
    return MarketMetricsV1(
        contract_version="v1",
        input_class="market_metrics.v1",
        module_id="derivatives_collector",
        provider_id=provider_id,
        symbol=symbol,
        metrics_ts="2026-05-28T00:00:00Z",
        freshness_state="fresh",
        provider_coverage=ProviderCoverage(
            status="full",
            collectable_metrics=[
                "open_interest",
                "funding_rate",
                "volume_futures",
                "long_short_ratio",
                "liquidations_long",
                "liquidations_short",
            ],
            missing_metrics=[],
        ),
        metrics=MetricsPayload(
            open_interest=1.0,
            funding_rate=0.1,
            volume_futures=2.0,
            long_short_ratio=3.0,
            liquidations_long=4.0,
            liquidations_short=5.0,
        ),
        refs=Refs(
            primary_output="a",
            meta_output="b",
            latest="c",
            status="d",
        ),
        warnings=[],
    )


def test_strategy_market_context_reads_by_symbol_view():
    td = Path(tempfile.mkdtemp())
    write_market_metrics_view(_payload(), root=td)
    data = read_market_context("BTCUSDT", root=td)
    assert data is not None
    assert data["input_class"] == "market_metrics.v1"
    assert data["symbol"] == "BTCUSDT"


def test_strategy_market_context_missing_returns_none():
    td = Path(tempfile.mkdtemp())
    assert read_market_context("BTCUSDT", root=td) is None


def test_perf_replay_context_reads_multiple_history_runs():
    td = Path(tempfile.mkdtemp())
    write_market_metrics_history_view(_payload(provider_id="bitget"), root=td, run_id="run001")
    write_market_metrics_history_view(_payload(provider_id="bitget"), root=td, run_id="run002")
    rows = read_replay_context("BTCUSDT", root=td)
    assert len(rows) == 2
    assert all(row["input_class"] == "market_metrics.v1" for row in rows)


def test_perf_replay_context_missing_history_raises():
    td = Path(tempfile.mkdtemp())
    try:
        read_replay_context("BTCUSDT", root=td)
    except FileNotFoundError:
        return
    assert False, "expected FileNotFoundError"
