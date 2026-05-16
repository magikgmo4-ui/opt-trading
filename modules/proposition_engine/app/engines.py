"""Query decision_engine, opportunity_ranker, probability_engine — best-effort."""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .schema import NormalizedSignal


def query_engines(signal: NormalizedSignal) -> dict:
    """Return best-effort context dict from the three trading engines."""
    ctx: dict = {}

    # --- probability_engine ---
    try:
        from modules.probability_engine.app.probability_engine import ProbabilityEngine, load_config
        pe = ProbabilityEngine(load_config())
        side_bias = 1.0 if signal.side == "BUY" else -1.0
        features = {
            "symbol": signal.ticker,
            "trend_bias": side_bias * 0.4,
            "momentum_bias": side_bias * 0.3,
        }
        prob_result = pe.score(features)
        prob_result.pop("_details", None)
        ctx["probability"] = prob_result
    except Exception as exc:
        ctx["probability"] = {"error": str(exc)}

    # --- opportunity_ranker ---
    try:
        from modules.opportunity_ranker.app.opportunity_ranker import OpportunityRanker
        ranker = OpportunityRanker()
        scanner_mock = [{"symbol": signal.ticker, "scan_score": 0.5 if signal.side == "BUY" else -0.5}]
        liq_mock = [{"symbol": signal.ticker, "liquidation_score": 0.2}]
        prob_mock = [{"symbol": signal.ticker,
                      "probability_long": ctx.get("probability", {}).get("probability_long", 0.5),
                      "probability_short": ctx.get("probability", {}).get("probability_short", 0.5),
                      "confidence": ctx.get("probability", {}).get("confidence", 0.5)}]
        merged = ranker.merge_data(scanner_mock, liq_mock, prob_mock)
        ranked = ranker.rank_opportunities(merged)
        ctx["ranker"] = ranked[0] if ranked else {}
    except Exception as exc:
        ctx["ranker"] = {"error": str(exc)}

    # --- decision_engine ---
    try:
        from modules.decision_engine.app.decision_engine import DecisionEngine
        engine = DecisionEngine()
        ranker_mock = [{"symbol": signal.ticker,
                        "opportunity_score": ctx.get("ranker", {}).get("opportunity_score", 0.5),
                        "setup_bias": "LONG" if signal.side == "BUY" else "SHORT",
                        "priority": ctx.get("ranker", {}).get("priority", "MEDIUM")}]
        prob_mock = [{"symbol": signal.ticker,
                      "probability_long": ctx.get("probability", {}).get("probability_long", 0.5),
                      "probability_short": ctx.get("probability", {}).get("probability_short", 0.5),
                      "confidence": ctx.get("probability", {}).get("confidence", 0.5)}]
        liq_mock = [{"symbol": signal.ticker, "liquidation_bias": "BALANCED", "intensity": "LOW"}]
        merged = engine.merge_data(ranker_mock, prob_mock, liq_mock)
        decisions = engine.make_decisions(merged)
        ctx["decision"] = decisions[0] if decisions else {}
    except Exception as exc:
        ctx["decision"] = {"error": str(exc)}

    return ctx
