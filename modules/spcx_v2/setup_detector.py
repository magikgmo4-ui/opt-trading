"""SPCX V2 — Setup detector: applies 4 gates to classify trading setups."""

from typing import Optional

from modules.spcx_v2.config import (
    GATE_0_THRESHOLDS,
    GATE_1_THRESHOLDS,
    GATE_3_THRESHOLDS,
    MarketSnapshot,
    GateResult,
    SetupMatch,
    ScoreSet,
    SetupCandidate,
)


# ── Gate 0: Data Validity ────────────────────────────────────────────
def check_gate_0_data_validity(snapshot: MarketSnapshot) -> GateResult:
    reasons = []
    details = {}

    price_ok = snapshot.price_status == "live"
    bars_ok = snapshot.bars_count > GATE_0_THRESHOLDS["min_bars_count"]
    volume_ok = snapshot.volume > GATE_0_THRESHOLDS["min_volume"]
    trust_ok = snapshot.price_trust > GATE_0_THRESHOLDS["min_price_trust"]
    source_ok = snapshot.source_count >= GATE_0_THRESHOLDS["min_source_count"]

    details["price_status"] = snapshot.price_status
    details["bars_count"] = snapshot.bars_count
    details["volume"] = snapshot.volume
    details["price_trust"] = snapshot.price_trust
    details["source_count"] = snapshot.source_count

    if not price_ok:
        reasons.append("PRICE_NOT_LIVE")
    if not bars_ok:
        reasons.append("NO_BARS")
    if not volume_ok:
        reasons.append("NO_VOLUME")
    if not trust_ok:
        reasons.append("PRICE_TRUST_LOW")
    if not source_ok:
        reasons.append("NO_SOURCE")

    passed = price_ok and bars_ok and volume_ok and trust_ok and source_ok
    return GateResult(
        gate_name="gate_0_data_validity",
        passed=passed,
        reason_codes=reasons,
        details=details,
    )


# ── Gate 1: Market Safety ────────────────────────────────────────────
def check_gate_1_market_safety(snapshot: MarketSnapshot) -> GateResult:
    reasons = []
    details = {}

    spread_ok = snapshot.spread_pct <= GATE_1_THRESHOLDS["max_spread_pct"]
    volume_ok = snapshot.dollar_volume >= GATE_1_THRESHOLDS["min_dollar_volume"]
    halt_ok = not snapshot.halt_active
    no_contradiction = not snapshot.nasdaq_contradiction and not snapshot.yahoo_contradiction

    details["spread_pct"] = snapshot.spread_pct
    details["dollar_volume"] = snapshot.dollar_volume
    details["halt_active"] = snapshot.halt_active
    details["nasdaq_contradiction"] = snapshot.nasdaq_contradiction
    details["yahoo_contradiction"] = snapshot.yahoo_contradiction

    if not spread_ok:
        reasons.append("SPREAD_TOO_WIDE")
    if not volume_ok:
        reasons.append("VOLUME_INSUFFICIENT")
    if not halt_ok:
        reasons.append("HALT_ACTIVE")
    if not no_contradiction:
        reasons.append("SOURCE_CONTRADICTION")

    passed = spread_ok and volume_ok and halt_ok and no_contradiction
    return GateResult(
        gate_name="gate_1_market_safety",
        passed=passed,
        reason_codes=reasons,
        details=details,
    )


# ── Gate 2: Setup Detected ───────────────────────────────────────────
def check_gate_2_setup_detected(snapshot: MarketSnapshot) -> tuple[GateResult, list[SetupMatch]]:
    matches = []
    reasons = []

    if snapshot.vwap is not None:
        if snapshot.price > snapshot.vwap:
            matches.append(SetupMatch(setup_id="VWAP_HOLD_LONG", category="vwap", confidence=70, trigger_event="price above VWAP"))
        else:
            matches.append(SetupMatch(setup_id="VWAP_REJECT", category="vwap", confidence=50, trigger_event="price below VWAP"))

    for struct in snapshot.smc_structures:
        struct_type = struct.get("type", "")
        if struct_type == "FVG_BULLISH":
            matches.append(SetupMatch(setup_id="FVG_BULLISH_RECLAIM", category="smc", confidence=60, trigger_event="FVG bullish detected"))
        elif struct_type == "FVG_BEARISH":
            matches.append(SetupMatch(setup_id="FVG_BEARISH_REJECT", category="smc", confidence=60, trigger_event="FVG bearish detected"))
        elif struct_type == "BOS":
            matches.append(SetupMatch(setup_id="BOS_CONTINUATION", category="smc", confidence=65, trigger_event="break of structure"))
        elif struct_type == "CHOCH":
            matches.append(SetupMatch(setup_id="CHOCH_REVERSAL", category="smc", confidence=65, trigger_event="change of character"))
        elif struct_type == "LIQUIDITY_SWEEP_LOW":
            matches.append(SetupMatch(setup_id="LIQUIDITY_SWEEP_LOW_RECLAIM", category="smc", confidence=55, trigger_event="liquidity sweep lows"))
        elif struct_type == "LIQUIDITY_SWEEP_HIGH":
            matches.append(SetupMatch(setup_id="LIQUIDITY_SWEEP_HIGH_REJECT", category="smc", confidence=55, trigger_event="liquidity sweep highs"))
        elif struct_type == "ORDER_BLOCK":
            matches.append(SetupMatch(setup_id="ORDER_BLOCK_RETEST", category="smc", confidence=55, trigger_event="order block retest"))

    if snapshot.news_headline:
        sentiment = snapshot.news_sentiment or "neutral"
        if sentiment == "positive":
            matches.append(SetupMatch(setup_id="NEWS_CATALYST_BREAKOUT", category="news", confidence=50, trigger_event=f"news: {snapshot.news_headline[:40]}"))
        elif sentiment == "negative":
            matches.append(SetupMatch(setup_id="NEGATIVE_HEADLINE_RISK_OFF", category="news", confidence=50, trigger_event=f"news: {snapshot.news_headline[:40]}"))

    passed = len(matches) > 0
    if not passed:
        reasons.append("NO_SETUP_DETECTED")

    return GateResult(
        gate_name="gate_2_setup_detected",
        passed=passed,
        reason_codes=reasons,
        details={"matches_count": len(matches)},
    ), matches


# ── Gate 3: Score Validation ─────────────────────────────────────────
def compute_scores(snapshot: MarketSnapshot, matches: list[SetupMatch]) -> ScoreSet:
    trade_ready = 50
    liquidity = 50
    risk = 50
    smart_money = 50
    catalyst = 50

    if snapshot.price_status == "live":
        trade_ready += 15
    if snapshot.bars_count >= 5:
        trade_ready += 10
    if snapshot.volume > 1000:
        trade_ready += 10
    if snapshot.price_trust >= 70:
        trade_ready += 10
    trade_ready = min(trade_ready, 100)

    if snapshot.spread_pct < 0.5:
        liquidity += 20
    elif snapshot.spread_pct < 1.0:
        liquidity += 10
    if snapshot.dollar_volume > 1_000_000:
        liquidity += 20
    elif snapshot.dollar_volume > 500_000:
        liquidity += 10
    liquidity = min(liquidity, 100)

    if snapshot.halt_active:
        risk += 30
    if snapshot.spread_pct > 1.5:
        risk += 20
    if snapshot.nasdaq_contradiction or snapshot.yahoo_contradiction:
        risk += 20
    risk = min(risk, 100)

    smc_count = sum(1 for m in matches if m.category == "smc")
    if smc_count >= 2:
        smart_money += 30
    elif smc_count == 1:
        smart_money += 15
    if snapshot.vwap is not None and snapshot.price > snapshot.vwap:
        smart_money += 10
    smart_money = min(smart_money, 100)

    if snapshot.news_headline:
        if snapshot.news_sentiment == "positive":
            catalyst += 25
        elif snapshot.news_sentiment == "negative":
            catalyst += 5
        else:
            catalyst += 10
    catalyst = min(catalyst, 100)

    return ScoreSet(
        trade_ready=trade_ready,
        liquidity=liquidity,
        risk=risk,
        smart_money=smart_money,
        catalyst=catalyst,
    )


def check_gate_3_score_validation(scores: ScoreSet) -> GateResult:
    reasons = []

    t = GATE_3_THRESHOLDS
    trade_ok = scores.trade_ready >= t["trade_ready_B"]
    liquidity_ok = scores.liquidity >= t["liquidity_B"]
    risk_ok = scores.risk <= t["risk_max_for_trade"]

    if not trade_ok:
        reasons.append("TRADE_READY_TOO_LOW")
    if not liquidity_ok:
        reasons.append("LIQUIDITY_TOO_LOW")
    if not risk_ok:
        reasons.append("RISK_TOO_HIGH")

    passed = trade_ok and liquidity_ok and risk_ok
    return GateResult(
        gate_name="gate_3_score_validation",
        passed=passed,
        reason_codes=reasons,
        details={"scores": {k: getattr(scores, k) for k in ["trade_ready", "liquidity", "risk", "smart_money", "catalyst"]}},
    )


# ── Grade Classification ─────────────────────────────────────────────
def classify_grade(scores: ScoreSet, gates_passed: int) -> str:
    if gates_passed < 4:
        return "reject"

    t = GATE_3_THRESHOLDS
    if scores.trade_ready >= t["trade_ready_A_plus"] and scores.liquidity >= t["liquidity_A"] and scores.risk <= 30 and scores.smart_money >= t["smart_money_A"]:
        return "A+"
    elif scores.trade_ready >= t["trade_ready_A"] and scores.liquidity >= t["liquidity_B"] and scores.risk <= t["risk_max_for_trade"]:
        return "A"
    elif scores.trade_ready >= t["trade_ready_B"]:
        return "B"

    return "reject"


# ── Main detection pipeline ──────────────────────────────────────────
def detect(snapshot: MarketSnapshot) -> Optional[SetupCandidate]:
    gate0 = check_gate_0_data_validity(snapshot)
    if not gate0.passed:
        return SetupCandidate(
            symbol=snapshot.symbol,
            ts=snapshot.timestamp,
            setup_type="NONE",
            grade="reject",
            status="paper_only",
            gates={gate0.gate_name: {"passed": gate0.passed, "reasons": gate0.reason_codes}},
            reason_codes=gate0.reason_codes,
        )

    gate1 = check_gate_1_market_safety(snapshot)
    if not gate1.passed:
        return SetupCandidate(
            symbol=snapshot.symbol,
            ts=snapshot.timestamp,
            setup_type="NONE",
            grade="reject",
            status="paper_only",
            gates={
                gate0.gate_name: {"passed": gate0.passed, "reasons": gate0.reason_codes},
                gate1.gate_name: {"passed": gate1.passed, "reasons": gate1.reason_codes},
            },
            reason_codes=gate0.reason_codes + gate1.reason_codes,
        )

    gate2, matches = check_gate_2_setup_detected(snapshot)
    if not gate2.passed:
        return SetupCandidate(
            symbol=snapshot.symbol,
            ts=snapshot.timestamp,
            setup_type="NONE",
            grade="reject",
            status="paper_only",
            gates={
                gate0.gate_name: {"passed": gate0.passed, "reasons": gate0.reason_codes},
                gate1.gate_name: {"passed": gate1.passed, "reasons": gate1.reason_codes},
                gate2.gate_name: {"passed": gate2.passed, "reasons": gate2.reason_codes},
            },
            reason_codes=gate0.reason_codes + gate1.reason_codes + gate2.reason_codes,
        )

    scores = compute_scores(snapshot, matches)
    gate3 = check_gate_3_score_validation(scores)

    all_passed = gate0.passed and gate1.passed and gate2.passed and gate3.passed
    gates_passed = sum([gate0.passed, gate1.passed, gate2.passed, gate3.passed])
    grade = classify_grade(scores, gates_passed)

    best_match = max(matches, key=lambda m: m.confidence) if matches else None
    setup_type = best_match.setup_id if best_match else "UNKNOWN"

    all_reasons = []
    for g in [gate0, gate1, gate2, gate3]:
        all_reasons.extend(g.reason_codes)

    return SetupCandidate(
        symbol=snapshot.symbol,
        ts=snapshot.timestamp,
        setup_type=setup_type,
        grade=grade,
        status="paper_only",
        gates={
            "gate_0_data_validity": {"passed": gate0.passed, "reasons": gate0.reason_codes},
            "gate_1_market_safety": {"passed": gate1.passed, "reasons": gate1.reason_codes},
            "gate_2_setup_detected": {"passed": gate2.passed, "reasons": gate2.reason_codes},
            "gate_3_score_validation": {"passed": gate3.passed, "reasons": gate3.reason_codes},
        },
        scores=scores,
        reason_codes=all_reasons,
        entry_zone="above ORB high + VWAP hold" if grade in ("A+", "A") else "",
        invalidation="below VWAP or ORB midpoint" if grade in ("A+", "A") else "",
        tp_logic=["TP1 1R", "TP2 2R", "runner VWAP/trend"] if grade in ("A+", "A", "B") else [],
    )
