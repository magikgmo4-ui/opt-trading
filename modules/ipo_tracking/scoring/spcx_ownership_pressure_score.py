"""
SPCX Ownership Pressure Scoring Engine
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Scores ownership pressure risks from the ownership ledger:
  - Insider concentration risk
  - Lockup expiry pressure
  - Institutional positioning
  - Private round cost-basis overhang
  - Greenshoe/stabilization status
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

IPO_PRICE = 135.0
LOCKUP_STANDARD_MONTHS = 6


def score_ownership_pressure(
    ownership_data: dict | None = None,
    current_price: float | None = None,
) -> dict[str, Any]:
    """Score SPCX ownership pressure from ledger data.

    Args:
        ownership_data: Output from collect_spcx_sec_ownership()
        current_price: Current SPCX price for profit-overhang calculation
    """
    result = {
        "score": 50.0,
        "component_scores": {},
        "signals": [],
        "reasons": [],
        "warnings": [],
    }

    holders = ownership_data.get("holders", []) if ownership_data else []
    insider_summary = ownership_data.get("insider_summary", {}) if ownership_data else {}
    inst_summary = ownership_data.get("institutional_summary", {}) if ownership_data else {}
    greenshoe = ownership_data.get("greenshoe_stabilization", {}) if ownership_data else {}

    # --- 1. Insider concentration score ---
    concentration = _score_insider_concentration(insider_summary, holders)
    result["component_scores"]["insider_concentration"] = concentration

    # --- 2. Lockup overhang score ---
    lockup = _score_lockup_overhang(insider_summary, holders, current_price)
    result["component_scores"]["lockup_overhang"] = lockup

    # --- 3. Institutional positioning score ---
    institutional = _score_institutional_quality(inst_summary, holders)
    result["component_scores"]["institutional_quality"] = institutional

    # --- 4. Cost basis overhang score ---
    cost_basis = _score_cost_basis_overhang(holders, current_price)
    result["component_scores"]["cost_basis_overhang"] = cost_basis

    # --- 5. Greenshoe / stabilization score ---
    gs = _score_greenshoe_status(greenshoe)
    result["component_scores"]["greenshoe_status"] = gs

    # --- Composite score (lower = more risky / more selling pressure) ---
    weights = {
        "insider_concentration": 0.20,
        "lockup_overhang": 0.35,
        "institutional_quality": 0.20,
        "cost_basis_overhang": 0.15,
        "greenshoe_status": 0.10,
    }

    composite = 0.0
    for key, weight in weights.items():
        val = result["component_scores"].get(key, {})
        comp_score = val.get("score", 50) if isinstance(val, dict) else 50
        composite += comp_score * weight

    result["score"] = round(composite, 1)

    # --- Signals ---
    if result["score"] >= 75:
        result["signals"].append("OWNERSHIP_STRUCTURE_HEALTHY")
    elif result["score"] >= 55:
        result["signals"].append("OWNERSHIP_STRUCTURE_MODERATE")
    else:
        result["signals"].append("OWNERSHIP_STRUCTURE_CONCERNING")

    lockup_score = result["component_scores"]["lockup_overhang"].get("score", 50)
    if lockup_score < 30:
        result["signals"].append("LOCKUP_OVERHANG_SIGNIFICANT")
        result["warnings"].append("Large lockup expiry upcoming — potential selling pressure")

    cost_score = result["component_scores"]["cost_basis_overhang"].get("score", 50)
    if cost_score < 40:
        result["signals"].append("COST_BASIS_OVERHANG_PRESENT")
        result["warnings"].append("Pre-IPO holders have very low cost basis — profit-taking risk")

    return result


def _score_insider_concentration(insider_summary: dict, holders: list) -> dict:
    """Score insider concentration risk. Lower = more risky."""
    score = 50
    reasons = []

    insider_pct = _num(insider_summary.get("total_insider_pct"))
    voting_pct = _num(insider_summary.get("total_voting_power_pct"))
    insider_count = insider_summary.get("insider_count", 0)

    if insider_pct is not None:
        if insider_pct < 20:
            score += 20
            reasons.append("low_insider_concentration")
        elif insider_pct < 40:
            score += 10
            reasons.append("moderate_insider")
        elif insider_pct > 60:
            score -= 15
            reasons.append("high_insider_concentration")
        elif insider_pct > 80:
            score -= 25
            reasons.append("extreme_insider_concentration")

    if voting_pct is not None:
        if voting_pct > 70:
            score -= 15
            reasons.append("voting_power_concentrated")
        elif voting_pct > 50:
            score -= 5
            reasons.append("voting_majority_insider")

    if insider_count <= 3:
        score -= 10
        reasons.append("few_insiders")
    elif insider_count >= 10:
        score += 5
        reasons.append("broad_insider_base")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "insider_pct": insider_pct,
        "voting_power_pct": voting_pct,
        "insider_count": insider_count,
        "reasons": reasons,
    }


def _score_lockup_overhang(
    insider_summary: dict, holders: list, current_price: float | None
) -> dict:
    """Score lockup expiry risk. Lower = more imminent risk."""
    score = 60
    reasons = []

    locked_shares = _num(insider_summary.get("locked_shares"))
    unlocked_shares = _num(insider_summary.get("unlocked_shares"))
    total_insider = _num(insider_summary.get("total_insider_shares"))
    next_expiry = insider_summary.get("next_lockup_expiry")

    # Lockup ratio
    if total_insider and total_insider > 0:
        locked_pct = (locked_shares or 0) / total_insider * 100
        if locked_pct > 80:
            score -= 20
            reasons.append("most_shares_locked")
        elif locked_pct > 50:
            score -= 10
            reasons.append("significant_locked")

    # Days to expiry
    if next_expiry:
        try:
            expiry_date = datetime.fromisoformat(next_expiry.replace("Z", "+00:00"))
            days_remaining = (expiry_date - datetime.now(timezone.utc)).days
            if days_remaining < 0:
                score -= 30
                reasons.append("lockup_already_expired")
            elif days_remaining < 30:
                score -= 25
                reasons.append(f"lockup_expires_in_{days_remaining}d_IMMINENT")
            elif days_remaining < 60:
                score -= 15
                reasons.append(f"lockup_expires_in_{days_remaining}d")
            elif days_remaining < 90:
                score -= 5
                reasons.append(f"lockup_expires_in_{days_remaining}d")
            else:
                score += 10
                reasons.append(f"lockup_expires_in_{days_remaining}d_far")
        except Exception:
            pass

    # Cost-basis vs current price — profit overhang
    if current_price and current_price > 0:
        pre_ipo_holders = [
            h for h in holders
            if h.get("cost_basis_estimated") and _num(h.get("acquisition_price"))
        ]
        if pre_ipo_holders:
            # All pre-IPO holders have massive gains
            for h in pre_ipo_holders[:3]:
                cost = _num(h.get("acquisition_price"))
                if cost and cost > 0 and current_price / cost > 100:
                    score -= 10
                    reasons.append("massive_unrealized_gains")
                    break

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "locked_shares": locked_shares,
        "unlocked_shares": unlocked_shares,
        "next_lockup_expiry": next_expiry,
        "reasons": reasons,
    }


def _score_institutional_quality(inst_summary: dict, holders: list) -> dict:
    """Score institutional ownership quality. Higher = more institutional validation."""
    score = 50
    reasons = []

    inst_pct = _num(inst_summary.get("total_institutional_pct"))
    inst_count = inst_summary.get("institution_count", 0)
    five_pct_count = inst_summary.get("five_pct_holders_count", 0)
    float_pct = _num(inst_summary.get("float_pct"))

    if inst_pct is not None:
        if inst_pct > 30:
            score += 20
            reasons.append("strong_institutional_presence")
        elif inst_pct > 15:
            score += 10
            reasons.append("moderate_institutional")
        elif inst_pct < 5:
            score -= 15
            reasons.append("low_institutional_interest")

    if inst_count >= 20:
        score += 10
        reasons.append("broad_institutional_base")
    elif inst_count >= 5:
        score += 5

    if five_pct_count >= 3:
        score += 10
        reasons.append("multiple_major_holders")
    elif five_pct_count == 0:
        score -= 5
        reasons.append("no_major_holders")

    # Float: very small float = volatile
    if float_pct is not None:
        if float_pct < 20:
            score -= 15
            reasons.append("very_tight_float")
        elif float_pct < 40:
            score -= 5
            reasons.append("limited_float")
        elif float_pct > 60:
            score += 10
            reasons.append("healthy_float")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "institutional_pct": inst_pct,
        "institution_count": inst_count,
        "float_pct": float_pct,
        "five_pct_holders": five_pct_count,
        "reasons": reasons,
    }


def _score_cost_basis_overhang(holders: list, current_price: float | None) -> dict:
    """Score cost-basis overhang risk. Lower = more risk of profit-taking."""
    score = 50
    reasons = []

    if not current_price or current_price <= 0:
        return {"score": 50, "reasons": ["no_current_price"]}

    pre_ipo = [h for h in holders if h.get("cost_basis_estimated")]
    if not pre_ipo:
        return {"score": 50, "reasons": ["no_pre_ipo_data"]}

    total_pre_ipo_shares = sum(_num(h.get("shares")) for h in pre_ipo)
    deep_itm_count = 0
    for h in pre_ipo:
        cost = _num(h.get("acquisition_price"))
        if cost and cost > 0:
            gain_pct = (current_price - cost) / cost * 100
            if gain_pct > 1000:  # 10x+
                deep_itm_count += 1

    if deep_itm_count >= 3:
        score -= 25
        reasons.append(f"{deep_itm_count}_holders_deep_in_the_money")
    elif deep_itm_count >= 1:
        score -= 15
        reasons.append("pre_ipo_holders_deep_in_the_money")

    # Share of total float held by pre-IPO with extreme gains
    if total_pre_ipo_shares > 1000000000:  # 1B+
        score -= 10
        reasons.append("massive_pre_ipo_position")

    if not reasons:
        reasons.append("cost_basis_manageable")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "pre_ipo_holders_count": len(pre_ipo),
        "pre_ipo_shares": round(total_pre_ipo_shares, 2),
        "deep_itm_count": deep_itm_count,
        "reasons": reasons,
    }


def _score_greenshoe_status(greenshoe: dict) -> dict:
    """Score greenshoe/stabilization status. Lower = stabilization ending/risky."""
    score = 50
    reasons = []

    gs_shares = _num(greenshoe.get("greenshoe_shares"))
    gs_pct = _num(greenshoe.get("greenshoe_pct"))
    exercised = _num(greenshoe.get("exercised_shares"))
    exercised_pct = _num(greenshoe.get("exercised_pct"))

    if gs_pct is not None:
        if gs_pct > 15:
            score += 5
            reasons.append("large_greenshoe_still_active")
        elif gs_pct > 0:
            reasons.append("greenshoe_active")

    if exercised_pct is not None:
        if exercised_pct > 50:
            score -= 10
            reasons.append("greenshoe_largely_exercised_stabilization_ending")
        elif exercised_pct > 0:
            score -= 5
            reasons.append("greenshoe_partially_exercised")

    if gs_shares and gs_shares > 0:
        reasons.append(f"greenshoe_{gs_shares:.0f}_shares")

    if not reasons:
        reasons.append("no_greenshoe_data")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "greenshoe_shares": gs_shares,
        "greenshoe_pct": gs_pct,
        "exercised_pct": exercised_pct,
        "reasons": reasons,
    }


def _num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))
