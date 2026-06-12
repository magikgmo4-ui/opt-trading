from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from statistics import mean

from .setups import SETUPS, list_setups
from .enrichment.feature_schema import ENRICHED_CANDLE_FEATURES
from .io import utc_now


FEATURE_GROUPS = {
    "trend": ["ema_20", "ema_50", "ema_200", "sma_20", "sma_50", "trend_score"],
    "momentum": ["rsi_14", "macd_line", "macd_histogram", "momentum_score", "relative_volume"],
    "volume": ["relative_volume", "volume_zscore", "liquidity_score", "volatility_score"],
    "smart_money": ["fvg_bullish", "fvg_bearish", "bos", "choch", "liquidity_sweep_high", "liquidity_sweep_low", "smc_score"],
    "premium_discount": ["premium_discount_regime", "premium_discount_position_pct"],
    "catalyst": ["news_count", "sec_filings_count", "catalyst_score", "news_score"],
    "consensus": ["consensus_price", "source_count", "source_disagreement_score", "weighted_trust_score"],
    "gaps": ["ipo_gap_pct", "prev_gap_pct", "vwap_distance_pct"],
    "bands": ["bb_upper", "bb_middle", "bb_lower", "atr_14"],
    "opening_range": ["opening_range_5m_high", "opening_range_5m_low", "opening_range_15m_high", "opening_range_15m_low"],
}


@dataclass
class SignalQualityRow:
    feature: str
    setup_id: str
    timeframe: str
    signal_quality: float
    expectancy: float
    sample_count: int
    correlation: float


@dataclass
class AblationResult:
    setup_id: str
    baseline_expectancy: float
    ablated_group: str
    ablated_expectancy: float
    delta: float
    importance: str       # critical, significant, minor, none
    sample_count: int


@dataclass
class SourceReliability:
    source_id: str
    freshness_score: float
    coverage_score: float
    accuracy_score: float
    agreement_score: float
    latency_seconds: float | None
    impact_on_signal: float
    composite_score: float
    grade: str           # A, B, C, D, F


@dataclass
class AlertPrecision:
    alert_event: str
    total_count: int
    true_positives: int
    false_positives: int
    missed_moves: int
    precision: float
    recall: float
    avg_r_after: float
    max_adverse_excursion: float
    max_favorable_excursion: float
    avg_bars_to_target: float


def build_signal_quality_matrix(
    enriched_history: list[dict[str, Any]],
    backtest_results: list[dict[str, Any]],
) -> list[SignalQualityRow]:
    rows: list[SignalQualityRow] = []
    for setup_id, bt_result in _index_by_setup(backtest_results).items():
        for feature in _extract_features(enriched_history):
            correlation = _feature_signal_correlation(feature, enriched_history, bt_result)
            expectancy = bt_result.get("expectancy_r", 0)
            rows.append(SignalQualityRow(
                feature=feature,
                setup_id=setup_id,
                timeframe=_setup_timeframe(setup_id),
                signal_quality=round(correlation * abs(expectancy), 3),
                expectancy=expectancy,
                sample_count=bt_result.get("total_trades", 0),
                correlation=round(correlation, 3),
            ))
    return sorted(rows, key=lambda r: abs(r.signal_quality), reverse=True)


def run_feature_ablation(
    enriched_history: list[dict[str, Any]],
    backtest_results: list[dict[str, Any]],
) -> list[AblationResult]:
    results: list[AblationResult] = []
    baseline_by_setup = _index_by_setup(backtest_results)

    for setup_id, baseline in baseline_by_setup.items():
        base_r = baseline.get("expectancy_r", 0)
        for group_name in FEATURE_GROUPS:
            ablated_r = _simulate_ablation(setup_id, group_name, baseline, enriched_history)
            delta = base_r - ablated_r
            importance = (
                "critical" if delta > 0.15 else
                "significant" if delta > 0.08 else
                "minor" if delta > 0.02 else
                "none"
            )
            results.append(AblationResult(
                setup_id=setup_id,
                baseline_expectancy=base_r,
                ablated_group=group_name,
                ablated_expectancy=ablated_r,
                delta=round(delta, 3),
                importance=importance,
                sample_count=baseline.get("total_trades", 0),
            ))
    return sorted(results, key=lambda r: abs(r.delta), reverse=True)


def score_source_reliability(
    events: list[dict[str, Any]],
    snapshot: dict[str, Any],
) -> list[SourceReliability]:
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    results: list[SourceReliability] = []

    sources_info = {
        "yahoo_chart": {"weight": 0.25, "target_latency": 60},
        "tradingview_webhook": {"weight": 0.25, "target_latency": 120},
        "bot_vision_adapter": {"weight": 0.15, "target_latency": 600},
        "sec_edgar": {"weight": 0.10, "target_latency": 86400},
        "yahoo_news_rss": {"weight": 0.10, "target_latency": 3600},
    }

    for src, info in sources_info.items():
        src_events = [e for e in events if e.get("source") == src]
        ok_events = [e for e in src_events if e.get("ok")]

        freshness = 0.0
        if src_events:
            for e in src_events:
                ct = e.get("collected_at")
                if ct:
                    try:
                        age = (now - datetime.fromisoformat(ct.replace("Z", "+00:00"))).total_seconds()
                        freshness = max(freshness, max(0.0, 1.0 - age / info["target_latency"]))
                    except (ValueError, TypeError):
                        pass

        coverage = len(ok_events) / max(1, len(src_events))
        accuracy = 1.0 if any(e.get("ok") for e in src_events) else 0.0

        agreement = 0.8 if len(ok_events) > 0 else 0.3
        impact = round(info["weight"] * (0.5 * freshness + 0.3 * coverage + 0.2 * accuracy), 3)

        composite = round(0.35 * freshness + 0.25 * coverage + 0.15 * accuracy + 0.15 * agreement + 0.10 * impact, 3)
        grade = "A" if composite >= 0.8 else "B" if composite >= 0.65 else "C" if composite >= 0.5 else "D" if composite >= 0.3 else "F"

        latest_ct = None
        for e in src_events:
            ct = e.get("collected_at")
            if ct:
                latest_ct = ct

        latency = None
        if latest_ct:
            try:
                latency = (now - datetime.fromisoformat(latest_ct.replace("Z", "+00:00"))).total_seconds()
            except (ValueError, TypeError):
                pass

        results.append(SourceReliability(
            source_id=src,
            freshness_score=round(freshness, 3),
            coverage_score=round(coverage, 3),
            accuracy_score=round(accuracy, 3),
            agreement_score=round(agreement, 3),
            latency_seconds=round(latency, 1) if latency else None,
            impact_on_signal=impact,
            composite_score=composite,
            grade=grade,
        ))

    return sorted(results, key=lambda r: r.composite_score, reverse=True)


def evaluate_alert_precision(
    alert_log: list[dict[str, Any]],
    backtest_results: list[dict[str, Any]],
) -> list[AlertPrecision]:
    results: list[AlertPrecision] = []
    by_event: dict[str, list[dict]] = {}
    for a in alert_log:
        event = a.get("event", a.get("alert_event", "unknown"))
        by_event.setdefault(event, []).append(a)

    for event_name, alerts in by_event.items():
        total = len(alerts)
        tp = sum(1 for a in alerts if a.get("outcome") == "tp" or a.get("result") == "win")
        fp = sum(1 for a in alerts if a.get("outcome") == "fp" or a.get("result") == "loss")
        missed = sum(1 for a in alerts if a.get("outcome") == "missed")

        precision = tp / max(1, tp + fp)
        recall = tp / max(1, tp + missed)

        r_vals = [a.get("r_after", a.get("r_multiple", 0)) for a in alerts if "r_after" in a or "r_multiple" in a]
        avg_r = mean(r_vals) if r_vals else 0.0

        maes = [a.get("mae_r", a.get("max_adverse_r", 0)) for a in alerts if "mae_r" in a or "max_adverse_r" in a]
        mfes = [a.get("mfe_r", a.get("max_favorable_r", 0)) for a in alerts if "mfe_r" in a or "max_favorable_r" in a]
        bars_to_target = [a.get("bars_to_target", a.get("bars_held", 0)) for a in alerts if "bars_to_target" in a or "bars_held" in a]

        results.append(AlertPrecision(
            alert_event=event_name,
            total_count=total,
            true_positives=tp,
            false_positives=fp,
            missed_moves=missed,
            precision=round(precision, 3),
            recall=round(recall, 3),
            avg_r_after=round(avg_r, 3),
            max_adverse_excursion=round(min(maes), 3) if maes else 0.0,
            max_favorable_excursion=round(max(mfes), 3) if mfes else 0.0,
            avg_bars_to_target=round(mean(bars_to_target), 1) if bars_to_target else 0,
        ))

    return sorted(results, key=lambda r: r.avg_r_after, reverse=True)


def _index_by_setup(backtest_results: list[dict]) -> dict[str, dict]:
    return {r.get("setup_id", "unknown"): r for r in backtest_results}


def _extract_features(enriched_history: list[dict]) -> list[str]:
    if not enriched_history:
        return ENRICHED_CANDLE_FEATURES
    first = enriched_history[0]
    indicators = list(first.get("indicators", {}).keys())
    smart_money = list(first.get("smart_money", {}).keys())
    scores = list(first.get("scores", {}).keys())
    return indicators + smart_money + scores


def _feature_signal_correlation(feature: str, enriched: list[dict], bt_result: dict) -> float:
    values: list[float] = []
    for candle in enriched:
        for domain in ["indicators", "smart_money", "scores"]:
            val = (candle.get(domain) or {}).get(feature)
            if val is not None:
                if isinstance(val, bool):
                    values.append(1.0 if val else 0.0)
                elif isinstance(val, (int, float)):
                    values.append(float(val))
                break

    if len(values) < 2:
        return 0.0

    avg = mean(values)
    n = len(values)
    if n < 2:
        return 0.0

    numerator = sum((v - avg) * 0.5 for v in values)
    denominator = (sum((v - avg) ** 2 for v in values) * 0.25 * n) ** 0.5
    return numerator / denominator if denominator else 0.0


def _setup_timeframe(setup_id: str) -> str:
    setup = SETUPS.get(setup_id)
    return setup.timeframe if setup else "M5"


def _simulate_ablation(setup_id: str, group_name: str, baseline: dict, enriched: list[dict]) -> float:
    base_r = baseline.get("expectancy_r", 0)
    features_in_group = FEATURE_GROUPS.get(group_name, [])

    if not enriched or not features_in_group:
        return base_r

    total_reduction = 0.0
    for f in features_in_group:
        corr = _feature_signal_correlation(f, enriched, baseline)
        total_reduction += abs(corr) * 0.2

    reduction = min(base_r * 0.4, total_reduction / max(1, len(features_in_group)))
    return base_r - reduction
