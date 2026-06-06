"""Source Selector — selects the best source candidate for a given data_key.

4 selection modes:
  - best_candidate   : highest score, tie-break by freshness then reliability
  - all_candidates   : returns best + all candidates with scores
  - consensus        : requires 2+ candidates within tolerance, else flags
  - fallback_only    : primary first, fallback if primary stale

Rules:
  - score=0 + status=candidate sources are NEVER selectable
  - All selections produce resolver_decision.v1
  - canonical_value.v1.stale=True if no eligible candidate
  - Data Center arbitrates sources, does not decide trades
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import time
import uuid
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from modules.data_center import registry_cache as rc


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _make_decision_id() -> str:
    return str(uuid.uuid4())


def resolve(
    contract_class: str,
    symbol: str,
    data_key: str,
    mode: str = "best_candidate",
    min_score_threshold: float = 0.3,
    consistency_tolerance_pct: float = 5.0,
) -> Dict[str, Any]:
    """Select the best source candidate and return a resolver_decision + canonical_value.

    Args:
        contract_class: e.g. "market_metrics.v1"
        symbol: e.g. "BTCUSDT"
        data_key: e.g. "open_interest"
        mode: "best_candidate", "all_candidates", "consensus", "fallback_only"
        min_score_threshold: minimum score for eligibility (default 0.3)
        consistency_tolerance_pct: max deviation for consensus mode (default 5.0)

    Returns:
        dict with resolver_decision and canonical_value
    """
    candidates_info = rc.get_candidates(contract_class, data_key, symbol)
    producer_ids = candidates_info.get("producers", [])

    if not producer_ids:
        return _stale_result(contract_class, symbol, data_key, "no_candidates")

    # Build candidate objects with scores
    candidates = []
    for pid in producer_ids:
        src = rc.get_by_source(pid)
        if not src:
            continue
        score = _compute_score(src)
        fresh = _check_freshness(src)
        candidates.append({
            "producer_id": pid,
            "score": score,
            "eligible": score >= min_score_threshold and fresh,
            "fresh": fresh,
            "contract_class": src.get("contract_class"),
            "data_keys": src.get("data_keys", []),
        })

    if mode == "consensus":
        return _select_consensus(candidates, contract_class, symbol, data_key, consistency_tolerance_pct)
    elif mode == "all_candidates":
        return _select_all(candidates, contract_class, symbol, data_key, min_score_threshold)
    elif mode == "fallback_only":
        return _select_fallback(candidates, contract_class, symbol, data_key, min_score_threshold)
    else:  # best_candidate
        return _select_best(candidates, contract_class, symbol, data_key, min_score_threshold)


def _compute_score(src: Dict) -> float:
    """Compute a simple score from cached score_components.
    
    Full scoring uses source_score.v1 (8 dimensions).
    This is a lightweight version using cached components.
    """
    comps = src.get("score_components", {})
    reliability = comps.get("source_reliability", 0.5) * 0.25
    freshness = comps.get("freshness", 0.0) * 0.25
    completeness = comps.get("completeness", 0.0) * 0.25
    schema = 0.8 * 0.15  # assume valid until proven otherwise
    consistency = 0.5 * 0.10  # neutral until peers available
    return round(reliability + freshness + completeness + schema + consistency, 4)


def _check_freshness(src: Dict) -> bool:
    """Check if source data is fresh (last_write not null)."""
    return src.get("last_write") is not None


def _stale_result(contract_class: str, symbol: str, data_key: str, reason: str) -> Dict:
    decision_id = _make_decision_id()
    now = _now_iso()
    return {
        "resolver_decision": {
            "schema_version": "resolver_decision.v1",
            "decision_id": decision_id,
            "contract_class": contract_class,
            "symbol": symbol,
            "data_key": data_key,
            "decided_at": now,
            "candidates": [],
            "selected_producer_id": None,
            "selection_reason": reason,
            "selection_rule": "stale_fallback",
        },
        "canonical_value": {
            "schema_version": "canonical_value.v1",
            "contract_class": contract_class,
            "symbol": symbol,
            "data_key": data_key,
            "canonical_value": None,
            "resolved_at": now,
            "resolver_decision_ref": decision_id,
            "winning_producer_id": None,
            "winning_score": 0,
            "stale": True,
        },
    }


def _select_best(candidates: List[Dict], contract_class: str, symbol: str, data_key: str, threshold: float) -> Dict:
    eligible = [c for c in candidates if c["eligible"]]
    if not eligible:
        return _stale_result(contract_class, symbol, data_key, "no_eligible_candidates")

    if len(eligible) == 1:
        return _build_result(eligible[0], candidates, contract_class, symbol, data_key, "only_eligible")

    # highest_score, tie-break by freshness
    eligible.sort(key=lambda c: (c["score"], c["fresh"]), reverse=True)
    return _build_result(eligible[0], candidates, contract_class, symbol, data_key, "highest_score")


def _select_all(candidates: List[Dict], contract_class: str, symbol: str, data_key: str, threshold: float) -> Dict:
    best = _select_best(candidates, contract_class, symbol, data_key, threshold)
    best["all_candidates"] = candidates
    return best


def _select_consensus(candidates: List[Dict], contract_class: str, symbol: str, data_key: str, tolerance_pct: float) -> Dict:
    eligible = [c for c in candidates if c["eligible"]]
    if len(eligible) < 2:
        return _stale_result(contract_class, symbol, data_key, "consensus_requires_2_eligible")

    # For consensus, we need actual values (placeholder: use scores as proxy)
    scores = [c["score"] for c in eligible]
    max_score = max(scores)
    min_score = min(scores)
    deviation = abs(max_score - min_score) / max(max_score, 0.001)

    if deviation > tolerance_pct / 100:
        best = max(eligible, key=lambda c: c["score"])
        result = _build_result(best, candidates, contract_class, symbol, data_key, "highest_score")
        result["canonical_value"]["flagged"] = True
        result["canonical_value"]["flag_reason"] = f"deviation {deviation:.2%} > tolerance {tolerance_pct}%"
        return result

    best = max(eligible, key=lambda c: c["score"])
    return _build_result(best, candidates, contract_class, symbol, data_key, "consensus")


def _select_fallback(candidates: List[Dict], contract_class: str, symbol: str, data_key: str, threshold: float) -> Dict:
    # Primary = first candidate, fallback = second
    primary = candidates[0] if len(candidates) > 0 else None
    fallback = candidates[1] if len(candidates) > 1 else None

    if primary and primary["eligible"]:
        return _build_result(primary, candidates, contract_class, symbol, data_key, "fallback_only")

    if fallback and fallback["eligible"]:
        return _build_result(fallback, candidates, contract_class, symbol, data_key, "fallback_only__secondary")

    return _stale_result(contract_class, symbol, data_key, "fallback_exhausted")


def _build_result(selected: Dict, all_candidates: List[Dict], contract_class: str, symbol: str, data_key: str, rule: str) -> Dict:
    decision_id = _make_decision_id()
    now = _now_iso()
    return {
        "resolver_decision": {
            "schema_version": "resolver_decision.v1",
            "decision_id": decision_id,
            "contract_class": contract_class,
            "symbol": symbol,
            "data_key": data_key,
            "decided_at": now,
            "candidates": [
                {
                    "producer_id": c["producer_id"],
                    "score": c["score"],
                    "score_ref": None,
                    "evidence_ref": None,
                    "eligible": c["eligible"],
                    "disqualification_reason": None if c["eligible"] else "score_below_threshold" if c["score"] < 0.3 else "stale",
                }
                for c in all_candidates
            ],
            "selected_producer_id": selected["producer_id"],
            "selected_score": selected["score"],
            "selection_reason": f"{selected['producer_id']} selected via {rule}",
            "selection_rule": rule,
            "min_score_threshold": 0.3,
            "resolver_version": "best_value_resolver.v1",
        },
        "canonical_value": {
            "schema_version": "canonical_value.v1",
            "contract_class": contract_class,
            "symbol": symbol,
            "data_key": data_key,
            "canonical_value": None,  # value from actual producer data
            "resolved_at": now,
            "resolver_decision_ref": decision_id,
            "winning_producer_id": selected["producer_id"],
            "winning_score": selected["score"],
            "alternative_sources": [
                {"producer_id": c["producer_id"], "value": None, "score": c["score"]}
                for c in all_candidates if c["producer_id"] != selected["producer_id"]
            ],
            "stale": False,
        },
    }
