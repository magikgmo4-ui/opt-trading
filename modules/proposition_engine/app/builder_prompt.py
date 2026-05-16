"""Compose OpenClaw builder prompt from signal + engines context."""
from __future__ import annotations
from .schema import NormalizedSignal


def compose_prompt(signal: NormalizedSignal, engines_ctx: dict) -> str:
    decision = engines_ctx.get("decision", {})
    ranker = engines_ctx.get("ranker", {})
    probability = engines_ctx.get("probability", {})

    lines = [
        f"Signal reçu: {signal.ticker} {signal.side} @ {signal.price} (tf={signal.tf}, strategy={signal.strategy_id})",
        "",
        "Contexte engines:",
        f"  decision:    {decision.get('decision', 'N/A')} (confidence={decision.get('confidence', 'N/A')}, rationale={decision.get('rationale', 'N/A')})",
        f"  ranker:      score={ranker.get('opportunity_score', 'N/A')}, priority={ranker.get('priority', 'N/A')}, bias={ranker.get('setup_bias', 'N/A')}",
        f"  probability: long={probability.get('probability_long', 'N/A')}, short={probability.get('probability_short', 'N/A')}, confidence={probability.get('confidence', 'N/A')}",
    ]

    if signal.sl is not None:
        lines.append(f"  SL proposé:  {signal.sl}")
    if signal.tp is not None:
        lines.append(f"  TP proposé:  {signal.tp}")
    if signal.reason:
        lines.append(f"  Raison signal: {signal.reason}")

    lines += [
        "",
        "Génère une proposition de trade JSON avec exactement ces champs:",
        '{"action": "BUY|SELL|HOLD|SKIP", "size_pct": 0.0-1.0, "entry": <float>, "sl": <float|null>, "tp": <float|null>, "confidence": 0.0-1.0, "rationale": "<string>"}',
        "",
        "Réponds UNIQUEMENT avec le JSON. Aucun texte avant ou après.",
    ]

    return "\n".join(lines)
