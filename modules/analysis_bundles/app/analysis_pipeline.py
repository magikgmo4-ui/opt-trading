"""
analysis_pipeline — 3-step pipeline: Ingest → Normalize → Analyze

Step 1 — Ingest: read all vision analysis + coinglass OCR + data_center coverage
Step 2 — Normalize: per-asset tickets into unified schema
Step 3 — Analyze: cross-asset correlations, regime consensus, alerts
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .vision_analysis_reader import list_available_symbols, extract_signals_from_vision
from .asset_selector import _ASSET_CLASSIFICATION, produce_all_tickets
from .data_center_router import produce_data_center_coverage

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_REPORT_OUTPUT = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "analysis_report" / "latest.json"


# ── Step 1: Ingest ──────────────────────────────────────────────────────────

@dataclass
class IngestedSource:
    source_id: str
    symbol_count: int
    freshness: str
    provenance: str
    ingested_at: str
    files: list[str] = field(default_factory=list)


def step_ingest() -> dict:
    """Read all available data sources and return raw ingested data."""
    now = datetime.now(timezone.utc).isoformat()

    # Vision analysis — per symbol raw
    symbols = list_available_symbols()
    vision_raw = {}
    for sym in symbols:
        sig = extract_signals_from_vision(sym)
        vision_raw[sym] = sig

    # Coinglass OCR
    cg_path = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json"
    coinglass_raw = None
    if cg_path.exists():
        try:
            coinglass_raw = json.loads(cg_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Data center coverage
    coverage = produce_data_center_coverage()

    sources = [
        IngestedSource(
            source_id="vision_analysis",
            symbol_count=len(symbols),
            freshness="FRESH" if symbols else "MISSING",
            provenance=coverage["sources"]["vision_analysis"]["provenance"],
            ingested_at=now,
            files=symbols,
        ),
        IngestedSource(
            source_id="coinglass_ocr",
            symbol_count=1 if coinglass_raw else 0,
            freshness="FRESH" if coinglass_raw else "MISSING",
            provenance=coverage["sources"]["coinglass_ocr"]["provenance"],
            ingested_at=now,
            files=[str(cg_path)] if coinglass_raw else [],
        ),
    ]

    return {
        "pipeline_step": "INGEST",
        "executed_at": now,
        "total_sources": len(sources),
        "sources": [asdict(s) for s in sources],
        "vision_raw": vision_raw,
        "coinglass_raw": coinglass_raw,
    }


# ── Step 2: Normalize ───────────────────────────────────────────────────────

@dataclass
class NormalizedTicket:
    symbol: str
    asset: str
    asset_class: str
    product: str
    bias: Optional[str]
    timeframe: Optional[str]
    freshness: str
    analysis_ts: Optional[str]
    supports: list[dict] = field(default_factory=list)
    resistances: list[dict] = field(default_factory=list)
    plan: Optional[str] = None
    invalidation: Optional[str] = None
    screen_type: Optional[str] = None


def step_normalize(vision_raw: Optional[dict] = None) -> dict:
    """Normalize raw vision analysis into per-asset tickets."""
    now = datetime.now(timezone.utc).isoformat()

    if vision_raw is None:
        ingest = step_ingest()
        vision_raw = ingest["vision_raw"]

    tickets = {}
    for symbol, raw in vision_raw.items():
        classification = _ASSET_CLASSIFICATION.get(symbol, {
            "asset": symbol, "class": "UNKNOWN", "product": "UNKNOWN"
        })

        bias = raw.get("bias")
        # Infer bias from summary if not already set
        if bias is None and raw.get("available"):
            summary_text = ""
            if raw.get("plan"):
                summary_text += raw["plan"] + " "
            if raw.get("invalidation"):
                summary_text += raw["invalidation"]
            if "short" in summary_text.lower() or "vendre" in summary_text.lower():
                bias = "BEARISH"
            elif "long" in summary_text.lower() or "achat" in summary_text.lower() or "acheter" in summary_text.lower():
                bias = "BULLISH"

        ticket = NormalizedTicket(
            symbol=symbol,
            asset=classification["asset"],
            asset_class=classification["class"],
            product=classification["product"],
            bias=bias,
            timeframe=raw.get("timeframe"),
            freshness=raw.get("freshness", "UNKNOWN"),
            analysis_ts=raw.get("analysis_ts"),
            supports=raw.get("supports", []),
            resistances=raw.get("resistances", []),
            plan=raw.get("plan"),
            invalidation=raw.get("invalidation"),
            screen_type=raw.get("screen_type"),
        )
        tickets[symbol] = ticket

    return {
        "pipeline_step": "NORMALIZE",
        "executed_at": now,
        "total_tickets": len(tickets),
        "tickets": {k: asdict(v) for k, v in tickets.items()},
    }


# ── Step 3: Analyze ─────────────────────────────────────────────────────────

def step_analyze(normalized: Optional[dict] = None, ingest: Optional[dict] = None) -> dict:
    """Analyze normalized tickets — cross-asset correlations, regime, alerts."""
    now = datetime.now(timezone.utc).isoformat()

    if normalized is None:
        if ingest is None:
            ingest = step_ingest()
        normalized = step_normalize(vision_raw=ingest["vision_raw"])

    tickets = normalized["tickets"]

    # Group by class
    by_class: dict[str, list[dict]] = {}
    for sym, t in tickets.items():
        cls = t["asset_class"]
        if cls not in by_class:
            by_class[cls] = []
        by_class[cls].append(t)

    # Compute class-level biases
    class_bias = {}
    for cls, items in by_class.items():
        biases = [t["bias"] for t in items if t["bias"]]
        bullish = sum(1 for b in biases if b == "BULLISH")
        bearish = sum(1 for b in biases if b == "BEARISH")
        total = len(biases)
        if total == 0:
            consensus = "UNKNOWN"
        elif bullish > bearish:
            consensus = "BULLISH"
        elif bearish > bullish:
            consensus = "BEARISH"
        else:
            consensus = "NEUTRAL"
        class_bias[cls] = {
            "total": len(items),
            "with_bias": total,
            "bullish": bullish,
            "bearish": bearish,
            "consensus": consensus,
            "assets": [t["asset"] for t in items],
        }

    # Macro regime consensus
    macro_classes = ("MACRO_EQUITY", "MACRO_FX", "MACRO_COMMODITY", "MACRO_VOL", "MACRO_RATES")
    macro_biases = []
    for cls in macro_classes:
        if cls in class_bias:
            macro_biases.append(class_bias[cls]["consensus"])
    macro_bullish = sum(1 for b in macro_biases if b == "BULLISH")
    macro_bearish = sum(1 for b in macro_biases if b == "BEARISH")
    if macro_bullish > macro_bearish:
        macro_regime = "RISK_ON"
    elif macro_bearish > macro_bullish:
        macro_regime = "RISK_OFF"
    else:
        macro_regime = "MIXED"

    # Crypto regime
    crypto_classes = ("CRYPTO_MAJOR", "CRYPTO_ALT_L1", "CRYPTO_MEME", "CRYPTO_MARKET")
    crypto_biases = []
    for cls in crypto_classes:
        if cls in class_bias:
            crypto_biases.append(class_bias[cls]["consensus"])
    crypto_bullish = sum(1 for b in crypto_biases if b == "BULLISH")
    crypto_bearish = sum(1 for b in crypto_biases if b == "BEARISH")
    if crypto_bullish > crypto_bearish:
        crypto_regime = "BULLISH"
    elif crypto_bearish > crypto_bullish:
        crypto_regime = "BEARISH"
    else:
        crypto_regime = "MIXED"

    # Energy regime
    energy_class = class_bias.get("ENERGY", {})
    energy_regime = energy_class.get("consensus", "UNKNOWN")

    # Alerts: divergence between macro and crypto
    alerts = []
    if macro_regime == "RISK_ON" and crypto_regime == "BEARISH":
        alerts.append({
            "severity": "WARN",
            "type": "MACRO_CRYPTO_DIVERGENCE",
            "detail": f"Macro RISK_ON but crypto BEARISH — possible decoupling or lag",
        })
    if macro_regime == "RISK_OFF" and crypto_regime == "BULLISH":
        alerts.append({
            "severity": "WARN",
            "type": "MACRO_CRYPTO_DIVERGENCE",
            "detail": f"Macro RISK_OFF but crypto BULLISH — check if speculative",
        })

    # Alert: single-asset outliers
    for sym, t in tickets.items():
        cls = t["asset_class"]
        consensus = class_bias.get(cls, {}).get("consensus")
        if t["bias"] and consensus and t["bias"] != consensus and consensus != "NEUTRAL":
            alerts.append({
                "severity": "INFO",
                "type": "ASSET_DIVERGENCE",
                "detail": f"{t['asset']} ({cls}) is {t['bias']} but class consensus is {consensus}",
            })

    # Top actionable signals
    actionable = []
    for sym, t in sorted(tickets.items()):
        if t["bias"] and t["bias"] != "NEUTRAL" and t["supports"] and t["resistances"]:
            actionable.append({
                "asset": t["asset"],
                "class": t["asset_class"],
                "bias": t["bias"],
                "entry_zone": t["supports"][0]["value"] if t["bias"] == "BULLISH" else t["resistances"][0]["value"],
                "target": t["resistances"][0]["value"] if t["bias"] == "BULLISH" else t["supports"][0]["value"],
                "invalidation": t["invalidation"],
                "plan": t["plan"],
            })

    return {
        "pipeline_step": "ANALYZE",
        "executed_at": now,
        "regimes": {
            "macro": macro_regime,
            "crypto": crypto_regime,
            "energy": energy_regime,
        },
        "class_consensus": class_bias,
        "alerts": alerts,
        "actionable_signals": actionable,
    }


# ── Pipeline runner ──────────────────────────────────────────────────────────

def run_full_pipeline(output_path: Optional[Path] = None) -> dict:
    """Run ingest → normalize → analyze and produce full report."""
    ingest = step_ingest()
    normalized = step_normalize(vision_raw=ingest["vision_raw"])
    analysis = step_analyze(normalized=normalized)

    report = {
        "contract": "analysis_pipeline_report.v1",
        "produced_at": datetime.now(timezone.utc).isoformat(),
        **ingest,
        **normalized,
        **analysis,
    }

    path = output_path or _REPORT_OUTPUT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    return report
