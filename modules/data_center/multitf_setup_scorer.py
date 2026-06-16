"""
multitf_setup_scorer.py — score multi-TF setups per symbol.

Reads from multitf_analysis_input.v1 views and produces ranked setups.
3-phase architecture:
  1. Core setup detection (triggers only)
  2. Context enrichment (macro, volume, orderflow, backtest, true_value)
  3. Caps and downgrades (stale, missing, contradiction)

Produces:
  multitf_setup_score.v1 — per-symbol setup scores, probabilities, grades
  Writes to: data/data_center/views/multitf_setup_score.v1/by_symbol/{SYM}.json
             data/data_center/views/multitf_setup_score.v1/latest.json

Usage:
    python -m modules.data_center.multitf_setup_scorer

Invariants:
  - Read-only consumer of multitf_analysis_input.v1
  - No execution, no broker, no order
  - Monitor-only
  - Core trigger required for grade >= B
  - Enrichment can boost but cannot create setups
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_INPUT_DIR = _VIEWS_DIR / "multitf_analysis_input.v1" / "by_symbol"
_TRANSITION_LOG = _PROJECT_ROOT / "outputs" / "multitf_signal_calibration" / "grade_transitions.jsonl"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
# Asset class weight profiles
# ═══════════════════════════════════════════════════════════════

ASSET_PROFILES = {
    "crypto_perp": {
        "weights": {"htf_alignment": 14, "ltf_trigger": 18, "vwap_level_quality": 16,
                     "volume_orderflow": 18, "macro_alignment": 8, "freshness_source": 12,
                     "risk_reward": 8, "backtest_edge": 6},
        "triggers": ["vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low",
                      "liquidity_sweep_high", "liquidity_sweep_low", "bos_bull", "bos_bear"],
        "base_probability": {"vwap_rejection": 52, "vwap_reclaim": 54, "structure_break_short": 48,
                             "structure_break_long": 48, "orb_break_short": 55, "orb_break_long": 55,
                             "liquidity_sweep_short": 58, "liquidity_sweep_long": 58, "support_watch": 35},
    },
    "forex_cfd": {
        "weights": {"htf_alignment": 12, "ltf_trigger": 14, "vwap_level_quality": 14,
                     "volume_orderflow": 8, "macro_alignment": 18, "freshness_source": 14,
                     "risk_reward": 10, "backtest_edge": 10},
        "triggers": ["vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low",
                      "liquidity_sweep_high", "liquidity_sweep_low"],
        "base_probability": {"vwap_rejection": 50, "vwap_reclaim": 52, "support_watch": 33},
    },
    "stock": {
        "weights": {"htf_alignment": 14, "ltf_trigger": 16, "vwap_level_quality": 16,
                     "volume_orderflow": 16, "macro_alignment": 10, "freshness_source": 12,
                     "risk_reward": 8, "backtest_edge": 8},
        "triggers": ["vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low",
                      "volume_spike"],
        "base_probability": {"vwap_rejection": 50, "vwap_reclaim": 52, "orb_break_short": 52,
                             "orb_break_long": 52, "support_watch": 35},
    },
    "ipo": {
        "weights": {"htf_alignment": 12, "ltf_trigger": 16, "vwap_level_quality": 18,
                     "volume_orderflow": 18, "macro_alignment": 8, "freshness_source": 14,
                     "risk_reward": 8, "backtest_edge": 6},
        "triggers": ["vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low",
                      "volume_spike"],
        "base_probability": {"vwap_reclaim": 56, "vwap_rejection": 50, "orb_break_long": 55,
                             "orb_break_short": 50, "support_watch": 38},
    },
    "index": {
        "weights": {"htf_alignment": 12, "ltf_trigger": 12, "vwap_level_quality": 12,
                     "volume_orderflow": 10, "macro_alignment": 20, "freshness_source": 14,
                     "risk_reward": 10, "backtest_edge": 10},
        "triggers": ["vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low"],
        "base_probability": {"vwap_reclaim": 50, "vwap_rejection": 48, "support_watch": 33},
    },
    "commodity": {
        "weights": {"htf_alignment": 12, "ltf_trigger": 12, "vwap_level_quality": 12,
                     "volume_orderflow": 8, "macro_alignment": 20, "freshness_source": 14,
                     "risk_reward": 12, "backtest_edge": 10},
        "triggers": ["vwap_reclaim", "vwap_loss"],
        "base_probability": {"vwap_reclaim": 50, "vwap_rejection": 48, "support_watch": 33},
    },
}

_FALLBACK_PROFILE = ASSET_PROFILES["crypto_perp"]


# ═══════════════════════════════════════════════════════════════
# Trigger quality scoring
# ═══════════════════════════════════════════════════════════════

def _score_trigger_quality(entry: dict, signal_events: list) -> dict:
    """Score the quality of CDP triggers: freshness, strength, confirmation."""
    now = datetime.now(timezone.utc)
    best_age = 999
    has_volume_spike = "volume_spike" in signal_events
    signal_count = len([e for e in entry.get("signals", [])
                        if isinstance(e, dict) and e.get("source") == "tradingview_cdp"])
    triggers = [e for e in signal_events if e in (
        "vwap_reclaim", "vwap_loss", "orb_break_high", "orb_break_low",
        "liquidity_sweep_high", "liquidity_sweep_low", "bos_bull", "bos_bear")]

    for sig in entry.get("signals", []):
        if isinstance(sig, dict) and sig.get("source") == "tradingview_cdp":
            ts = sig.get("timestamp", "")
            if ts:
                try:
                    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    age = (now - t).total_seconds() / 60
                    best_age = min(best_age, age)
                except Exception:
                    pass

    # Age decay
    if best_age <= 5:
        age_score = 100
        strength = "strong"
        decay_factor = 1.0
    elif best_age <= 15:
        age_score = 85
        strength = "strong"
        decay_factor = 0.90
    elif best_age <= 30:
        age_score = 65
        strength = "moderate"
        decay_factor = 0.75
    elif best_age <= 60:
        age_score = 40
        strength = "weak"
        decay_factor = 0.50
    elif best_age < 999:
        age_score = 15
        strength = "stale"
        decay_factor = 0.25
    else:
        age_score = 0
        strength = "none"
        decay_factor = 0.0

    # Volume confirmation
    if has_volume_spike:
        age_score = min(100, age_score + 10)
        if strength == "strong":
            strength = "strong_confirmed"

    # Multi-signal bonus
    if signal_count >= 3:
        age_score = min(100, age_score + 5)
    if len(triggers) >= 2:
        age_score = min(100, age_score + 8)
        strength = "strong_confirmed" if strength == "strong" else strength + "_multi"

    return {
        "trigger_quality_score": age_score,
        "trigger_age_minutes": int(best_age) if best_age < 999 else None,
        "trigger_strength": strength,
        "trigger_count": signal_count,
        "decay_factor": decay_factor,
    }


# ═══════════════════════════════════════════════════════════════
# Probability computation
# ═══════════════════════════════════════════════════════════════

def _compute_probability(setup_type: str, profile: dict, score: int,
                         tq: dict, freshness: str, missing_count: int) -> int:
    """Probability = base_rate + confluence_adj + adjustment - penalty."""
    base = profile.get("base_probability", {}).get(setup_type, 45)
    # Confluence: score above 60 adds bonus
    confluence = max(0, (score - 50) // 3)
    # Trigger quality adjustment
    tq_adj = (tq["trigger_quality_score"] - 50) // 8 if tq["trigger_quality_score"] > 0 else -5
    # Freshness
    fresh_adj = 3 if freshness == "fresh" else -5 if freshness == "stale" else 0
    # Missing penalty
    missing_penalty = min(10, missing_count * 2)
    proba = base + confluence + tq_adj + fresh_adj - missing_penalty
    return max(25, min(85, proba))


def _compute_confidence(freshness: str, completeness_pct: int, tq: dict, has_contradiction: bool) -> int:
    """Confidence = source quality + completeness + freshness + agreement."""
    base = 60
    if freshness == "fresh":
        base += 10
    elif freshness == "stale":
        base -= 20
    base += max(0, (completeness_pct - 40) // 4)
    if tq["trigger_strength"] in ("strong", "strong_confirmed"):
        base += 8
    elif tq["trigger_strength"] == "none":
        base -= 10
    if has_contradiction:
        base -= 15
    return max(30, min(85, base))


# ═══════════════════════════════════════════════════════════════
# Grade transition logger
# ═══════════════════════════════════════════════════════════════

def _log_grade_transition(sym: str, new_setup: dict) -> None:
    """Log every grade to JSONL for later accuracy tracking."""
    prev = _load_json(_VIEWS_DIR / "multitf_setup_score.v1" / "by_symbol" / f"{sym}.json")
    old_grade = None
    old_score = None
    if prev and prev.get("setups"):
        old_grade = prev["setups"][0].get("grade")
        old_score = prev["setups"][0].get("score")

    if old_grade == new_setup.get("grade") and old_score == new_setup.get("score"):
        return  # No change

    entry = {
        "symbol": sym,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "old_grade": old_grade,
        "old_score": old_score,
        "new_grade": new_setup.get("grade"),
        "new_score": new_setup.get("score"),
        "setup_type": new_setup.get("setup_type"),
        "core_evidence": new_setup.get("core_evidence", []),
        "downgrade_reasons": new_setup.get("downgrade_reasons", []),
        "trigger_strength": new_setup.get("trigger_strength"),
        "trigger_age_minutes": new_setup.get("trigger_age_minutes"),
    }
    _TRANSITION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(_TRANSITION_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


def _score_to_grade(score: int) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "A-"
    if score >= 60: return "B+"
    if score >= 50: return "B"
    if score >= 40: return "B-"
    if score >= 30: return "C"
    return "REJECT"


# ═══════════════════════════════════════════════════════════════
# PHASE 1 — Core setup detection (triggers only)
# ═══════════════════════════════════════════════════════════════

def _detect_core_setups(entry: dict) -> list[dict]:
    """Detect setups from core triggers: VWAP, ORB, liquidity sweeps, BOS/CHoCH.
    
    Returns list of setup dicts with core_evidence populated.
    Enrichment and caps are applied in later phases.
    """
    setups = []
    sym = entry.get("symbol", "")
    price = entry.get("price")
    levels = entry.get("levels", {})
    signals = entry.get("signals", [])
    tfs = entry.get("timeframes", {})
    freshness = entry.get("freshness_state", "unknown")

    vwap = levels.get("vwap")
    supports = levels.get("support_levels", [])
    resistances = levels.get("resistance_levels", [])
    signal_events = [s.get("event", "") for s in signals if isinstance(s, dict)]
    has_vwap_loss = "vwap_loss" in signal_events
    has_vwap_reclaim = "vwap_reclaim" in signal_events
    has_orb_break_high = "orb_break_high" in signal_events
    has_orb_break_low = "orb_break_low" in signal_events
    has_liquidity_sweep_high = "liquidity_sweep_high" in signal_events
    has_liquidity_sweep_low = "liquidity_sweep_low" in signal_events
    has_bos_bull = "bos_bull" in signal_events
    has_bos_bear = "bos_bear" in signal_events
    has_volume_spike = "volume_spike" in signal_events

    # Trend detection — CDP signal overrides absent trend
    h4_trend = tfs.get("H4", {}).get("indicators", {}).get("trend", "")
    m15_trend = tfs.get("M15", {}).get("indicators", {}).get("trend", "")
    any_cdp = has_vwap_loss or has_vwap_reclaim or has_orb_break_low or has_orb_break_high
    if not h4_trend and any_cdp:
        h4_trend = "neutral"
    if not m15_trend and any_cdp:
        m15_trend = "neutral"

    # ── Setup: VWAP rejection (short) ──
    if has_vwap_loss and price and h4_trend in ("bearish", "neutral"):
        core_evidence = [f"CDP vwap_loss @ {price}"]
        if h4_trend == "bearish":
            core_evidence.append("H4 bearish aligned")
        if vwap and price < vwap:
            core_evidence.append(f"price below VWAP ({vwap})")
        setups.append(_build_core_setup(sym, "vwap_rejection", "short", core_evidence, price, vwap, supports, resistances))

    # ── Setup: VWAP reclaim (long) ──
    if has_vwap_reclaim and price and h4_trend in ("bullish", "neutral"):
        core_evidence = [f"CDP vwap_reclaim @ {price}"]
        if h4_trend == "bullish":
            core_evidence.append("H4 bullish aligned")
        if vwap and price > vwap:
            core_evidence.append(f"price above VWAP ({vwap})")
        setups.append(_build_core_setup(sym, "vwap_reclaim", "long", core_evidence, price, vwap, supports, resistances))

    # ── Setup: ORB break high (long) ──
    if has_orb_break_high and price:
        orb_high = levels.get("orb_high")
        core_evidence = [f"CDP orb_break_high @ {price}"]
        if orb_high and price > orb_high:
            core_evidence.append(f"price above ORB high ({orb_high})")
        if has_volume_spike:
            core_evidence.append("volume_spike confirmation")
        setups.append(_build_core_setup(sym, "orb_break_long", "long", core_evidence, price, vwap, supports, resistances))

    # ── Setup: ORB break low (short) ──
    if has_orb_break_low and price:
        orb_low = levels.get("orb_low")
        core_evidence = [f"CDP orb_break_low @ {price}"]
        if orb_low and price < orb_low:
            core_evidence.append(f"price below ORB low ({orb_low})")
        if has_volume_spike:
            core_evidence.append("volume_spike confirmation")
        setups.append(_build_core_setup(sym, "orb_break_short", "short", core_evidence, price, vwap, supports, resistances))

    # ── Setup: Liquidity sweep (high = short trap, low = long trap) ──
    if has_liquidity_sweep_high and price:
        core_evidence = [f"CDP liquidity_sweep_high @ {price}"]
        setups.append(_build_core_setup(sym, "liquidity_sweep_short", "short", core_evidence, price, vwap, supports, resistances))

    if has_liquidity_sweep_low and price:
        core_evidence = [f"CDP liquidity_sweep_low @ {price}"]
        setups.append(_build_core_setup(sym, "liquidity_sweep_long", "long", core_evidence, price, vwap, supports, resistances))

    # ── Setup: Structure break (BOS/CHoCH) ──
    if has_bos_bear and h4_trend in ("bearish", "neutral") and price:
        core_evidence = [f"CDP bos_bear", f"H4 {h4_trend}"]
        setups.append(_build_core_setup(sym, "structure_break_short", "short", core_evidence, price, vwap, supports, resistances))

    if has_bos_bull and h4_trend in ("bullish", "neutral") and price:
        core_evidence = [f"CDP bos_bull", f"H4 {h4_trend}"]
        setups.append(_build_core_setup(sym, "structure_break_long", "long", core_evidence, price, vwap, supports, resistances))

    # ── Fallback: Support watch ──
    ref_price = price if price else (supports[0] if supports else None)
    if not setups and supports and ref_price:
        core_evidence = [f"Near support {supports[0]}", "No CDP trigger — monitor only"]
        setups.append(_build_core_setup(sym, "support_watch", "monitor_only", core_evidence, ref_price, vwap, supports, resistances))

    return setups


def _build_core_setup(sym: str, setup_type: str, direction: str,
                      core_evidence: list, price, vwap, supports: list, resistances: list) -> dict:
    """Build a core setup dict with evidence but no enrichment yet."""
    setup_id = f"{sym.lower()}_{setup_type}"
    entry_zone = []
    inval = 0
    targets = []

    if direction == "short":
        entry_zone = [price * 1.002, price * 1.005] if price else []
        inval = resistances[0] if resistances else (price * 1.01 if price else 0)
        targets = [supports[0]] if supports else [price * 0.98 if price else 0]
    elif direction == "long":
        entry_zone = [price * 0.995, price * 0.998] if price else []
        inval = supports[0] if supports else (price * 0.99 if price else 0)
        targets = [resistances[0]] if resistances else [price * 1.02 if price else 0]
    else:
        sup = supports[0] if supports else price
        entry_zone = [sup * 0.99, sup * 1.01] if sup else []
        inval = sup * 0.97 if sup else 0
        targets = [sup * 1.03] if sup else []

    rr = 0
    if inval and entry_zone and targets:
        risk = abs(entry_zone[0] - inval)
        reward = abs(targets[0] - inval)
        rr = round(reward / max(risk, 0.01), 1)

    return {
        "setup_id": setup_id,
        "direction": "monitor_only",
        "setup_type": setup_type,
        "core_evidence": core_evidence,
        "enrichment_evidence": [],
        "downgrade_reasons": [],
        "entry_zone": entry_zone,
        "invalidation": inval,
        "targets": targets,
        "risk_reward": rr,
    }


# ═══════════════════════════════════════════════════════════════
# PHASE 2 — Context enrichment
# ═══════════════════════════════════════════════════════════════

def _apply_enrichment(setup: dict, entry: dict, has_cdp_trigger: bool,
                      profile: dict, tq: dict) -> dict:
    """Apply context enrichment boosts. Cannot create setups — only boost existing ones."""
    enrichment = setup.setdefault("enrichment_evidence", [])
    score_bd = {}

    freshness = entry.get("freshness_state", "unknown")
    levels = entry.get("levels", {})
    macro = entry.get("macro_context") or {}
    orderflow = entry.get("orderflow") or {}
    sq = entry.get("source_quality") or {}
    tfs = entry.get("timeframes", {})
    h4_trend = tfs.get("H4", {}).get("indicators", {}).get("trend", "")

    # ── HTF alignment (use profile max as ceiling) ──
    w = profile["weights"]
    is_bearish_aligned = h4_trend == "bearish" and setup["setup_type"] in ("vwap_rejection", "orb_break_short", "structure_break_short", "liquidity_sweep_short")
    is_bullish_aligned = h4_trend == "bullish" and setup["setup_type"] in ("vwap_reclaim", "orb_break_long", "structure_break_long", "liquidity_sweep_long")
    if is_bearish_aligned or is_bullish_aligned:
        score_bd["htf_alignment"] = w.get("htf_alignment", 14)
        if h4_trend == "bearish": enrichment.append("H4 bearish aligned with short setup")
        else: enrichment.append("H4 bullish aligned with long setup")
    elif h4_trend:
        score_bd["htf_alignment"] = max(5, w.get("htf_alignment", 14) // 2)
        enrichment.append(f"H4 {h4_trend} (partial alignment)")
    else:
        score_bd["htf_alignment"] = max(3, w.get("htf_alignment", 14) // 3)

    # ── LTF trigger quality ──
    if has_cdp_trigger:
        score_bd["ltf_trigger"] = w.get("ltf_trigger", 15)
        cdp_events = [s.get("event") for s in entry.get("signals", []) if s.get("source") == "tradingview_cdp"]
        if cdp_events:
            enrichment.append(f"CDP trigger: {', '.join(cdp_events[:2])}")
        # Apply trigger quality decay
        score_bd["ltf_trigger"] = int(score_bd["ltf_trigger"] * tq["decay_factor"])
        if tq["trigger_strength"] in ("weak", "stale"):
            enrichment.append(f"Trigger {tq['trigger_strength']} — decay applied")
    else:
        score_bd["ltf_trigger"] = max(3, w.get("ltf_trigger", 15) // 3)

    # ── VWAP / level quality ──
    vwap = levels.get("vwap")
    w_max = w.get("vwap_level_quality", 15)
    if vwap:
        score_bd["vwap_level_quality"] = w_max
        enrichment.append(f"VWAP @ {vwap}")
    elif has_cdp_trigger:
        score_bd["vwap_level_quality"] = max(5, w_max * 2 // 3)
        enrichment.append("VWAP confirmed by CDP (raw value missing)")
    else:
        score_bd["vwap_level_quality"] = 0

    # ── Volume / orderflow ──
    w_max = w.get("volume_orderflow", 15)
    of_score = w_max // 2
    rvol = orderflow.get("relative_volume") or entry.get("timeframes", {}).get("M15", {}).get("indicators", {}).get("relative_volume")
    if rvol and isinstance(rvol, (int, float)) and rvol > 1.5:
        of_score = w_max
        enrichment.append(f"Relative volume elevated ({rvol:.1f}x)")
    cvd = orderflow.get("cvd_trend")
    if cvd and cvd != "unknown":
        of_score = max(of_score, int(w_max * 0.8))
        enrichment.append(f"CVD {cvd}")
    score_bd["volume_orderflow"] = of_score

    # ── Macro alignment ──
    w_max = w.get("macro_alignment", 10)
    macro_score = w_max // 2
    risk_regime = macro.get("risk_regime", "")
    if risk_regime == "risk_off" and setup["setup_type"] in ("vwap_rejection", "orb_break_short", "structure_break_short"):
        macro_score = w_max
        enrichment.append("Risk-off regime supports short")
    elif risk_regime == "risk_on" and setup["setup_type"] in ("vwap_reclaim", "orb_break_long", "structure_break_long"):
        macro_score = w_max
        enrichment.append("Risk-on regime supports long")
    dxy = macro.get("dxy_trend", "")
    if dxy == "bullish" and setup["setup_type"] in ("vwap_rejection", "orb_break_short"):
        macro_score = max(macro_score, int(w_max * 0.8))
        enrichment.append("DXY bullish supports short")
    score_bd["macro_alignment"] = macro_score

    # ── Freshness / source quality ──
    w_max = w.get("freshness_source", 12)
    if freshness == "fresh":
        score_bd["freshness_source"] = w_max
        enrichment.append("Data fresh")
    elif freshness == "stale":
        score_bd["freshness_source"] = w_max // 3
    else:
        score_bd["freshness_source"] = w_max // 2

    # ── Risk-reward ──
    w_max = w.get("risk_reward", 10)
    rr = setup.get("risk_reward", 0)
    if rr >= 2.0:
        score_bd["risk_reward"] = w_max
        enrichment.append(f"R:R {rr} favorable")
    elif rr >= 1.5:
        score_bd["risk_reward"] = int(w_max * 0.7)
    elif rr > 0:
        score_bd["risk_reward"] = int(w_max * 0.5)
    else:
        score_bd["risk_reward"] = max(1, w_max // 5)

    # ── Backtest edge (Lab feedback loop) ──
    w_max = w.get("backtest_edge", 10)
    # Try Lab edge scores first
    lab_edge = _load_lab_edge(entry.get("symbol", ""), setup["setup_type"])
    if lab_edge and lab_edge.get("sample_size", 0) >= 20:
        edge_score = lab_edge.get("edge_score", 0)
        rec = lab_edge.get("recommendation", "neutral")
        if rec == "supportive":
            score_bd["backtest_edge"] = min(w_max, max(3, int(edge_score * w_max / 100)))
            enrichment.append(f"Lab backtest supportive: WR {lab_edge.get('win_rate',0):.0%}, avgR {lab_edge.get('avg_r',0):.1f}, n={lab_edge.get('sample_size',0)}")
        elif rec == "negative":
            score_bd["backtest_edge"] = max(1, int(edge_score * w_max / 200))
            enrichment.append(f"Lab backtest negative: WR {lab_edge.get('win_rate',0):.0%} — edge reduced")
        else:
            score_bd["backtest_edge"] = max(1, int(edge_score * w_max / 150))
            enrichment.append(f"Lab backtest neutral: n={lab_edge.get('sample_size',0)}")
    else:
        # Fallback: entry-level backtest or baseline
        backtest = entry.get("backtest") or {}
        if backtest.get("win_rate") and backtest.get("sample_size", 0) >= 20:
            wr = backtest["win_rate"]
            score_bd["backtest_edge"] = min(w_max, int(wr * w_max * 1.2))
            enrichment.append(f"Backtest: {backtest['sample_size']} samples, WR {wr:.0%}")
        else:
            score_bd["backtest_edge"] = max(1, w_max // 3)

    # ── True value enrichment (SPCX only) ──
    tv_file = _VIEWS_DIR / "spacex_true_value.v1" / "by_symbol" / f"{entry.get('symbol', '')}.json"
    tv_data = _load_json(tv_file)
    if tv_data and isinstance(tv_data, dict):
        grade_tv = tv_data.get("final_grade", "")
        if grade_tv in ("A+", "A", "A-"):
            score_bd["backtest_edge"] = max(score_bd["backtest_edge"], 7)
            enrichment.append(f"True value grade {grade_tv} supportive")
        tv_score = tv_data.get("true_value_score", 0)
        if isinstance(tv_score, (int, float)) and tv_score > 60:
            enrichment.append(f"True value score {tv_score:.0f}")

    setup["score_breakdown"] = score_bd
    setup["score"] = sum(score_bd.values())
    return setup


# ═══════════════════════════════════════════════════════════════
# Lab feedback loop helpers
# ═══════════════════════════════════════════════════════════════

_LAB_RESULTS = _PROJECT_ROOT / "outputs" / "lab_backtest" / "results" / "setup_edge_scores.jsonl"
_lab_cache: dict | None = None


def _load_lab_edges() -> dict:
    """Load Lab edge scores, keyed by (symbol, setup_type)."""
    global _lab_cache
    if _lab_cache is not None:
        return _lab_cache
    _lab_cache = {}
    if not _LAB_RESULTS.exists():
        return _lab_cache
    try:
        for line in _LAB_RESULTS.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = (d.get("symbol", ""), d.get("setup_type", ""))
            if key not in _lab_cache:
                _lab_cache[key] = d
    except Exception:
        pass
    return _lab_cache


def _load_lab_edge(symbol: str, setup_type: str) -> dict | None:
    edges = _load_lab_edges()
    return edges.get((symbol, setup_type))


# ═══════════════════════════════════════════════════════════════
# PHASE 3 — Caps and downgrades
# ═══════════════════════════════════════════════════════════════

def _apply_caps_and_downgrades(setup: dict, entry: dict, has_cdp_trigger: bool) -> dict:
    """Apply caps and downgrades. Stale, missing, contradiction — cannot be overridden by enrichment."""
    downgrades = setup.setdefault("downgrade_reasons", [])
    score = setup.get("score", 0)
    freshness = entry.get("freshness_state", "unknown")
    tfs = entry.get("timeframes", {})
    h4_trend = tfs.get("H4", {}).get("indicators", {}).get("trend", "")
    m15_trend = tfs.get("M15", {}).get("indicators", {}).get("trend", "")

    # Règle 1: Pas de trigger CDP → cap C+ (max 39)
    if not has_cdp_trigger and setup["setup_type"] == "support_watch":
        score = min(score, 39)
        downgrades.append("No CDP trigger — grade capped at C+")

    # Règle 2: Stale → downgrade
    if freshness == "stale":
        score = max(score - 15, 10)
        downgrades.append("Data stale — score reduced by 15")
    elif freshness not in ("fresh",):
        score = max(score - 5, 15)
        downgrades.append(f"Freshness {freshness} — score reduced")

    # Règle 3: Contradiction HTF/LTF → cap B max (59)
    if h4_trend and m15_trend and h4_trend != m15_trend and h4_trend != "neutral" and m15_trend != "neutral":
        score = min(score, 59)
        downgrades.append(f"HTF/LTF contradiction ({h4_trend} vs {m15_trend}) — grade capped at B")

    # Règle 4: Missing critical fields → cap
    missing = entry.get("missing", [])
    critical_missing = [m for m in missing if m in ("price", "H4")]
    if critical_missing:
        score = min(score, 59)
        downgrades.append(f"Critical fields missing: {', '.join(critical_missing)} — grade capped at B")

    # Règle 5: Low completeness → confidence reduction
    sq = entry.get("source_quality") or {}
    completeness = sq.get("completeness_score", 1.0)
    if completeness < 0.4:
        downgrades.append(f"Low completeness ({completeness:.0%}) — confidence reduced")

    # Règle 6: Lab backtest negative → cap grade
    lab_edge = _load_lab_edge(entry.get("symbol", ""), setup["setup_type"])
    if lab_edge and lab_edge.get("recommendation") == "negative":
        score = min(score, 59)
        downgrades.append(f"Lab backtest negative (WR {lab_edge.get('win_rate',0):.0%}, n={lab_edge.get('sample_size',0)}) — grade capped at B")
    elif lab_edge and lab_edge.get("recommendation") == "insufficient_sample":
        downgrades.append(f"Lab backtest: insufficient sample ({lab_edge.get('sample_size',0)}) — no boost")

    setup["score"] = max(0, score)
    setup["grade"] = _score_to_grade(setup["score"])
    setup["probability_pct"] = min(75, max(30, setup["score"] - 8))
    setup["confidence_pct"] = min(80, max(40, 70 if freshness == "fresh" else 50))
    setup["missing"] = list(entry.get("missing", []))

    if not setup.get("reason"):
        setup["reason"] = setup["core_evidence"][:3]
    return setup


# ═══════════════════════════════════════════════════════════════
# Pipeline orchestrator
# ═══════════════════════════════════════════════════════════════

def _score_setups(entry: dict) -> list[dict]:
    """Full 3-phase pipeline: core → enrich → caps."""
    # Phase 1
    core_setups = _detect_core_setups(entry)
    if not core_setups:
        return []

    signals = entry.get("signals", [])
    signal_events = [s.get("event", "") for s in signals if isinstance(s, dict)]
    has_cdp = any(s.get("source") == "tradingview_cdp" for s in signals if isinstance(s, dict))

    # Asset class profile
    asset_class = entry.get("asset_class", "crypto_perp")
    profile = ASSET_PROFILES.get(asset_class, _FALLBACK_PROFILE)

    # Trigger quality
    tq = _score_trigger_quality(entry, signal_events)

    # Derive freshness + completeness for probability/confidence
    freshness = entry.get("freshness_state", "unknown")
    sq = entry.get("source_quality") or {}
    completeness_pct = int(sq.get("completeness_score", 0.5) * 100)

    final_setups = []
    for setup in core_setups:
        # Phase 2 — enrichment with profile weights
        setup = _apply_enrichment(setup, entry, has_cdp, profile, tq)
        # Phase 3 — caps and downgrades
        setup = _apply_caps_and_downgrades(setup, entry, has_cdp)

        # Compute proper probability and confidence
        missing_count = len(setup.get("missing", []))
        has_contradiction = any("contradiction" in r.lower() for r in setup.get("downgrade_reasons", []))
        setup["probability_pct"] = _compute_probability(
            setup["setup_type"], profile, setup["score"], tq, freshness, missing_count)
        setup["confidence_pct"] = _compute_confidence(
            freshness, completeness_pct, tq, has_contradiction)

        # Trigger quality fields
        setup["trigger_quality_score"] = tq["trigger_quality_score"]
        setup["trigger_age_minutes"] = tq["trigger_age_minutes"]
        setup["trigger_strength"] = tq["trigger_strength"]

        final_setups.append(setup)

    # Sort by score desc
    final_setups.sort(key=lambda s: s["score"], reverse=True)
    return final_setups


def produce_multitf_setup_scores() -> dict:
    """Read multitf_analysis_input.v1 and produce scored setups."""
    now = datetime.now(timezone.utc).isoformat()
    written = []

    if not _INPUT_DIR.exists():
        return {"error": "multitf_analysis_input.v1 views not found", "symbols": 0}

    for input_file in sorted(_INPUT_DIR.glob("*.json")):
        sym = input_file.stem
        entry = _load_json(input_file)
        if not isinstance(entry, dict):
            continue

        price = entry.get("price")
        freshness = entry.get("freshness_state", "unknown")
        tfs = entry.get("timeframes", {})
        h4_trend = tfs.get("H4", {}).get("indicators", {}).get("trend", "")
        m15_trend = tfs.get("M15", {}).get("indicators", {}).get("trend", "")
        tfs_with_data = [k for k, v in tfs.items() if v.get("indicators", {}).get("trend")]
        tfs_missing = [t for t in ["W1", "D1", "H4", "H1", "M15", "M5"] if t not in tfs_with_data]

        # 3-phase pipeline
        setups = _score_setups(entry)
        if not setups:
            continue

        # Bias
        bias = {
            "htf": h4_trend if h4_trend else "neutral",
            "ltf": m15_trend if m15_trend else "neutral",
            "alignment": "aligned" if h4_trend == m15_trend else "divergent" if h4_trend and m15_trend else "neutral",
            "reason": f"H4 {h4_trend}, M15 {m15_trend}" if h4_trend or m15_trend else "Insufficient trend data",
        }

        global_missing = list(entry.get("missing", []))
        if not price:
            global_missing.append("price")

        best = setups[0]["setup_id"]
        next_action = []
        if setups[0].get("downgrade_reasons"):
            next_action.append("Verifier downgrades: " + "; ".join(setups[0]["downgrade_reasons"][:2]))
        if "vwap" in best.lower():
            next_action.append("Surveiller VWAP")
        if "support" in best.lower():
            next_action.append("Surveiller test support — attendre trigger CDP")
        if freshness != "fresh":
            next_action.append("Verifier freshness des sources")
        if not next_action:
            next_action.append("Aucune action immediate")

        output = {
            "output_class": "multitf_setup_score.v1",
            "symbol": sym,
            "as_of": now,
            "bias": bias,
            "setups": setups,
            "top_setup": best,
            "next_action": next_action,
            "missing": global_missing,
            "source_quality": {
                "input_freshness": freshness,
                "timeframes_with_data": tfs_with_data,
                "timeframes_missing": tfs_missing,
                "completeness_pct": round(100 * len(tfs_with_data) / max(1, len(tfs_with_data) + len(tfs_missing))),
            },
        }

        out_path = _VIEWS_DIR / "multitf_setup_score.v1" / "by_symbol" / f"{sym}.json"
        _atomic_write(out_path, output)
        # Log grade transition for accuracy tracking
        if setups:
            _log_grade_transition(sym, setups[0])
        written.append(sym)

    # Global latest
    global_payload = {
        "output_class": "multitf_setup_score.v1",
        "provider_id": "multitf_setup_scorer",
        "produced_at": now,
        "symbols": written,
        "total_symbols": len(written),
    }
    _atomic_write(_VIEWS_DIR / "multitf_setup_score.v1" / "latest.json", global_payload)

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write(
        producer_id="multitf_setup_scorer",
        contract_class="multitf_setup_score.v1",
        output_path=str(_VIEWS_DIR / "multitf_setup_score.v1" / "latest.json"),
        status="ok",
        evidence={"symbols": len(written)},
    )

    return {"produced_at": now, "symbols": len(written)}


if __name__ == "__main__":
    r = produce_multitf_setup_scores()
    if "error" in r:
        print("ERROR:", r["error"])
    else:
        print(f"multitf_setup_score.v1: {r['symbols']} symbols")
