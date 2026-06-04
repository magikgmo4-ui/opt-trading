import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .btc_core_producer import produce_btc_core
from .macro_producer import produce_macro
from .verdict_schema import AnalysisVerdict, VerdictComposite, VerdictChecklistItem


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VERDICT_OUTPUT = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "analysis_verdict" / "latest.json"

_BIAS_SCORE = {"BULLISH": 75, "BEARISH": 25, "NEUTRAL": 50, "UNKNOWN": 50}
_REGIME_SCORE_BONUS = {
    "RISK_ON": 10,
    "RISK_ON_BROADENING": 5,
    "RISK_OFF": -10,
    "UNKNOWN": 0,
}


def _determine_alignment(btc_bias: str, macro_regime: str) -> str:
    if btc_bias == "UNKNOWN" or macro_regime == "UNKNOWN":
        return "UNKNOWN"
    if btc_bias == "BULLISH" and macro_regime in ("RISK_ON", "RISK_ON_BROADENING"):
        return "ALIGNED"
    if btc_bias == "BEARISH" and macro_regime == "RISK_OFF":
        return "ALIGNED"
    return "DIVERGENT"


def _determine_overall_bias(
    btc_bias: str,
    alignment: str,
) -> str:
    if alignment == "ALIGNED":
        return btc_bias
    if alignment == "DIVERGENT":
        return "NEUTRAL"
    return "UNKNOWN"


def _compute_confidence(
    btc_freshness: str,
    macro_freshness: str,
    btc_confidence: str,
    alignment: str,
    btc_bias: str,
    macro_regime: str,
) -> str:
    if btc_bias == "UNKNOWN" or macro_regime == "UNKNOWN":
        return "UNKNOWN"
    if btc_freshness == "STALE" or macro_freshness == "STALE":
        return "LOW"
    if alignment == "DIVERGENT":
        return "LOW"
    if btc_confidence == "HIGH" and alignment == "ALIGNED":
        return "HIGH"
    if btc_confidence in ("HIGH", "MEDIUM") and alignment == "ALIGNED":
        return "MEDIUM"
    if alignment == "ALIGNED":
        return "MEDIUM"
    return "LOW"


def _compute_score(btc_bias: str, macro_regime: str, alignment: str) -> int:
    base = _BIAS_SCORE.get(btc_bias, 50)
    bonus = _REGIME_SCORE_BONUS.get(macro_regime, 0)
    if alignment == "DIVERGENT":
        bonus = bonus - 15
    if alignment == "ALIGNED":
        bonus = bonus + 10
    return max(0, min(100, base + bonus))


def _build_checklist(btc_bias: str, macro_regime: str, alignment: str, warnings: list[str]) -> list[dict]:
    items = [
        {"item": "BTC bias determined", "status": "WARN" if btc_bias == "UNKNOWN" else "OK"},
        {"item": "Macro regime determined", "status": "WARN" if macro_regime == "UNKNOWN" else "OK"},
    ]

    if btc_bias != "UNKNOWN" and macro_regime != "UNKNOWN":
        if alignment == "ALIGNED":
            items.append({"item": "BTC/macro alignment", "status": "OK"})
        else:
            items.append({"item": "BTC/macro alignment", "status": "WARN"})

    items.append({"item": "BTC Coinglass OI/Funding check", "status": "N/A"})
    items.append({"item": "Telegram signal confirmation", "status": "N/A"})
    items.append({"item": "No conflicting news/events", "status": "N/A"})

    if warnings:
        items.append({"item": "Warnings present — review", "status": "WARN"})

    return items


def produce_verdict(
    btc_bundle: Optional[dict] = None,
    macro_bundle: Optional[dict] = None,
) -> AnalysisVerdict:
    now = datetime.now(timezone.utc).isoformat()

    if btc_bundle is None:
        btc = produce_btc_core()
        btc_bundle = btc.to_dict()
    if macro_bundle is None:
        macro = produce_macro()
        macro_bundle = macro.to_dict()

    btc_analysis = btc_bundle.get("analysis", {})
    macro_analysis = macro_bundle.get("analysis", {})

    btc_bias = btc_analysis.get("bias_short_term", "UNKNOWN")
    macro_regime = macro_analysis.get("regime", "UNKNOWN")
    btc_confidence = btc_analysis.get("confidence", "UNKNOWN")

    alignment = _determine_alignment(btc_bias, macro_regime)
    overall_bias = _determine_overall_bias(btc_bias, alignment)
    score = _compute_score(btc_bias, macro_regime, alignment)

    warnings = []
    missing = []
    source_refs = []

    btc_freshness = btc_bundle.get("freshness_state", "UNKNOWN")
    macro_freshness = macro_bundle.get("freshness_state", "UNKNOWN")

    if btc_freshness == "STALE":
        warnings.append("BTC bundle stale — analysis may be unreliable")
    if macro_freshness == "STALE":
        warnings.append("Macro bundle stale — analysis may be unreliable")

    missing.extend(btc_bundle.get("missing_inputs", []))
    missing.extend(macro_bundle.get("missing_inputs", []))

    source_refs.extend(btc_bundle.get("source_refs", []))
    source_refs.extend(macro_bundle.get("source_refs", []))

    confidence = _compute_confidence(
        btc_freshness, macro_freshness, btc_confidence,
        alignment, btc_bias, macro_regime,
    )

    freshness = "FRESH"
    if btc_freshness == "STALE" or macro_freshness == "STALE":
        freshness = "STALE"
    if btc_freshness == "UNKNOWN" and macro_freshness == "UNKNOWN":
        freshness = "UNKNOWN"

    checklist = _build_checklist(btc_bias, macro_regime, alignment, warnings)

    return AnalysisVerdict(
        contract="analysis_verdict.v1",
        verdict_id=f"verdict_{now[:19].replace(':', '')}_{str(uuid.uuid4())[:8]}",
        produced_at=now,
        freshness_state=freshness,
        bundles_used=["btc.core.v1", "macro.v1"],
        composite=VerdictComposite(
            btc_bias=btc_bias,
            macro_regime=macro_regime,
            alignment=alignment,
            overall_bias=overall_bias,
            confidence=confidence,
            score=score,
        ).to_dict(),
        checklist=checklist,
        warnings=warnings,
        missing_inputs=missing,
        source_refs=source_refs,
    )


def consume_and_write(
    btc_bundle: Optional[dict] = None,
    macro_bundle: Optional[dict] = None,
    output_path: Optional[Path] = None,
) -> AnalysisVerdict:
    """Produce verdict and write to disk. Returns the verdict."""
    verdict = produce_verdict(btc_bundle=btc_bundle, macro_bundle=macro_bundle)
    path = output_path or _VERDICT_OUTPUT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(verdict.to_dict(), indent=2, default=str), encoding="utf-8")
    return verdict
