"""Tests for SPCX V2 setup detector — all 4 gates + classification."""

import pytest
from modules.spcx_v2.config import MarketSnapshot
from modules.spcx_v2.setup_detector import (
    check_gate_0_data_validity,
    check_gate_1_market_safety,
    check_gate_2_setup_detected,
    check_gate_3_score_validation,
    compute_scores,
    classify_grade,
    detect,
)


# ── Gate 0: Data Validity ────────────────────────────────────────────
def test_gate0_all_pass():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is True
    assert result.reason_codes == []


def test_gate0_price_not_live():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="delayed", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is False
    assert "PRICE_NOT_LIVE" in result.reason_codes


def test_gate0_no_bars():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=0, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is False
    assert "NO_BARS" in result.reason_codes


def test_gate0_no_volume():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=0, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is False
    assert "NO_VOLUME" in result.reason_codes


def test_gate0_low_trust():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=0, source_count=3, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is False
    assert "PRICE_TRUST_LOW" in result.reason_codes


def test_gate0_no_source():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=0, spread_pct=0.5, dollar_volume=1e6)
    result = check_gate_0_data_validity(snap)
    assert result.passed is False
    assert "NO_SOURCE" in result.reason_codes


# ── Gate 1: Market Safety ────────────────────────────────────────────
def test_gate1_all_pass():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, halt_active=False, nasdaq_contradiction=False, yahoo_contradiction=False)
    result = check_gate_1_market_safety(snap)
    assert result.passed is True


def test_gate1_spread_too_wide():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=3.0, dollar_volume=1e6)
    result = check_gate_1_market_safety(snap)
    assert result.passed is False
    assert "SPREAD_TOO_WIDE" in result.reason_codes


def test_gate1_volume_insufficient():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=100_000)
    result = check_gate_1_market_safety(snap)
    assert result.passed is False
    assert "VOLUME_INSUFFICIENT" in result.reason_codes


def test_gate1_halt_active():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, halt_active=True)
    result = check_gate_1_market_safety(snap)
    assert result.passed is False
    assert "HALT_ACTIVE" in result.reason_codes


def test_gate1_source_contradiction():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, nasdaq_contradiction=True)
    result = check_gate_1_market_safety(snap)
    assert result.passed is False
    assert "SOURCE_CONTRADICTION" in result.reason_codes


# ── Gate 2: Setup Detected ───────────────────────────────────────────
def test_gate2_vwap_hold():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=43.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, vwap=42.0)
    gate, matches = check_gate_2_setup_detected(snap)
    assert gate.passed is True
    assert any(m.setup_id == "VWAP_HOLD_LONG" for m in matches)


def test_gate2_vwap_reject():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=41.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, vwap=42.0)
    gate, matches = check_gate_2_setup_detected(snap)
    assert gate.passed is True
    assert any(m.setup_id == "VWAP_REJECT" for m in matches)


def test_gate2_smc_fvg_bullish():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, smc_structures=[{"type": "FVG_BULLISH"}])
    gate, matches = check_gate_2_setup_detected(snap)
    assert any(m.setup_id == "FVG_BULLISH_RECLAIM" for m in matches)


def test_gate2_smc_bos():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, smc_structures=[{"type": "BOS"}])
    gate, matches = check_gate_2_setup_detected(snap)
    assert any(m.setup_id == "BOS_CONTINUATION" for m in matches)


def test_gate2_no_setup():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, vwap=None, smc_structures=[])
    gate, matches = check_gate_2_setup_detected(snap)
    assert gate.passed is False


def test_gate2_news_positive():
    snap = MarketSnapshot(symbol="SPCX", timestamp="t", price=42.0, price_status="live", bars_count=10, volume=5000, price_trust=80, source_count=3, spread_pct=0.5, dollar_volume=1e6, news_headline="NASA contract won", news_sentiment="positive")
    gate, matches = check_gate_2_setup_detected(snap)
    assert any(m.setup_id == "NEWS_CATALYST_BREAKOUT" for m in matches)


# ── Gate 3: Score Validation ─────────────────────────────────────────
def test_gate3_all_pass():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=80, liquidity=75, risk=30, smart_money=70, catalyst=60)
    result = check_gate_3_score_validation(scores)
    assert result.passed is True


def test_gate3_trade_ready_too_low():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=30, liquidity=75, risk=30, smart_money=70, catalyst=60)
    result = check_gate_3_score_validation(scores)
    assert result.passed is False
    assert "TRADE_READY_TOO_LOW" in result.reason_codes


def test_gate3_risk_too_high():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=80, liquidity=75, risk=70, smart_money=70, catalyst=60)
    result = check_gate_3_score_validation(scores)
    assert result.passed is False
    assert "RISK_TOO_HIGH" in result.reason_codes


# ── Grade Classification ─────────────────────────────────────────────
def test_classify_a_plus():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=80, liquidity=70, risk=25, smart_money=65, catalyst=60)
    assert classify_grade(scores, 4) == "A+"


def test_classify_a():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=65, liquidity=50, risk=50, smart_money=55, catalyst=50)
    assert classify_grade(scores, 4) == "A"


def test_classify_b():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=45, liquidity=50, risk=50, smart_money=40, catalyst=30)
    assert classify_grade(scores, 4) == "B"


def test_classify_reject_not_enough_gates():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=80, liquidity=70, risk=25, smart_money=65, catalyst=60)
    assert classify_grade(scores, 3) == "reject"


def test_classify_reject_low_scores():
    from modules.spcx_v2.config import ScoreSet
    scores = ScoreSet(trade_ready=35, liquidity=30, risk=70, smart_money=20, catalyst=10)
    assert classify_grade(scores, 4) == "reject"


# ── Full pipeline ────────────────────────────────────────────────────
def test_detect_valid_live_setup():
    snap = MarketSnapshot(
        symbol="SPCX", timestamp="2026-06-12T14:30:00Z", price=43.0,
        price_status="live", bars_count=10, volume=5000, price_trust=80,
        source_count=3, spread_pct=0.5, dollar_volume=1e6,
        vwap=42.0, smc_structures=[{"type": "BOS"}],
        halt_active=False, nasdaq_contradiction=False, yahoo_contradiction=False,
    )
    candidate = detect(snap)
    assert candidate is not None
    assert candidate.grade != "reject"
    assert candidate.setup_type != "NONE"


def test_detect_reject_no_live_price():
    snap = MarketSnapshot(
        symbol="SPCX", timestamp="t", price=42.0,
        price_status="delayed", bars_count=10, volume=5000, price_trust=80,
        source_count=3, spread_pct=0.5, dollar_volume=1e6,
        vwap=42.0, smc_structures=[], halt_active=False,
        nasdaq_contradiction=False, yahoo_contradiction=False,
    )
    candidate = detect(snap)
    assert candidate is not None
    assert candidate.grade == "reject"
    assert "PRICE_NOT_LIVE" in candidate.reason_codes


def test_detect_reject_halt():
    snap = MarketSnapshot(
        symbol="SPCX", timestamp="t", price=42.0,
        price_status="live", bars_count=10, volume=5000, price_trust=80,
        source_count=3, spread_pct=0.5, dollar_volume=1e6,
        vwap=42.0, smc_structures=[], halt_active=True,
        nasdaq_contradiction=False, yahoo_contradiction=False,
    )
    candidate = detect(snap)
    assert candidate is not None
    assert candidate.grade == "reject"
    assert "HALT_ACTIVE" in candidate.reason_codes


def test_compute_scores_with_news():
    snap = MarketSnapshot(
        symbol="SPCX", timestamp="t", price=43.0,
        price_status="live", bars_count=10, volume=5000, price_trust=85,
        source_count=3, spread_pct=0.3, dollar_volume=2e6,
        vwap=42.0, smc_structures=[{"type": "BOS"}, {"type": "FVG_BULLISH"}],
        news_headline="Major contract awarded", news_sentiment="positive",
        halt_active=False, nasdaq_contradiction=False, yahoo_contradiction=False,
    )
    from modules.spcx_v2.setup_detector import check_gate_2_setup_detected
    _, matches = check_gate_2_setup_detected(snap)
    scores = compute_scores(snap, matches)
    assert scores.trade_ready >= 50
    assert scores.liquidity >= 50
    assert scores.catalyst >= 50
    assert scores.smart_money >= 50
