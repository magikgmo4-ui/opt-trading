from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Literal

EventType = Literal[
    "signal_received",
    "proposition_generated",
    "approval_required",
    "trade_executed",
    "result_known",
    "pipeline_error",
    "pipeline_info",
]

ALL_EVENT_TYPES: set[str] = {
    "signal_received", "proposition_generated", "approval_required",
    "trade_executed", "result_known", "pipeline_error", "pipeline_info",
}


@dataclass
class PipelineEvent:
    event_type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    signal_id: str = ""
    request_id: str = ""

    def validate(self) -> None:
        if self.event_type not in ALL_EVENT_TYPES:
            raise ValueError(f"unknown event_type: {self.event_type!r}")


TEMPLATES: dict[str, str] = {
    "signal_received": (
        "📡 <b>Signal reçu</b>\n"
        "Ticker: <code>{ticker}</code>  Side: <code>{side}</code>\n"
        "Price: <code>{price}</code>  TF: <code>{tf}</code>\n"
        "Strategy: <code>{strategy_id}</code>"
    ),
    "proposition_generated": (
        "🧠 <b>Proposition générée</b>\n"
        "Ticker: <code>{ticker}</code>  Action: <code>{action}</code>\n"
        "Entry: <code>{entry}</code>  SL: <code>{sl}</code>  TP: <code>{tp}</code>\n"
        "Confidence: <code>{confidence}</code>\n"
        "Rationale: {rationale}"
    ),
    "approval_required": (
        "⏳ <b>Approbation requise</b>\n"
        "Ticker: <code>{ticker}</code>  Action: <code>{action}</code>\n"
        "Entry: <code>{entry}</code>  SL: <code>{sl}</code>  TP: <code>{tp}</code>\n"
        "Confidence: <code>{confidence}</code>\n"
        "→ Répondre APPROVE ou REJECT"
    ),
    "trade_executed": (
        "✅ <b>Trade exécuté</b>\n"
        "Ticker: <code>{ticker}</code>  Side: <code>{side}</code>\n"
        "Fill price: <code>{fill_price}</code>  Qty: <code>{fill_qty}</code>\n"
        "Trade ID: <code>{trade_id}</code>"
    ),
    "result_known": (
        "📊 <b>Résultat trade</b>\n"
        "Ticker: <code>{ticker}</code>  Side: <code>{side}</code>\n"
        "P&amp;L brut: <code>{gross_pnl}</code>  Net: <code>{net_pnl}</code>\n"
        "Durée: <code>{duration}</code>  Fees: <code>{fees}</code>"
    ),
    "pipeline_error": (
        "🚨 <b>Erreur pipeline</b>\n"
        "Étape: <code>{step}</code>\n"
        "Erreur: {error}"
    ),
    "pipeline_info": (
        "ℹ️ <b>Info pipeline</b>\n"
        "{message}"
    ),
}


def format_message(event: PipelineEvent) -> str:
    template = TEMPLATES.get(event.event_type, "⚠️ Événement: {event_type}\n{payload}")
    try:
        return template.format(event_type=event.event_type, payload=event.payload, **event.payload)
    except KeyError:
        # fallback: show raw payload
        lines = [f"📬 <b>{event.event_type}</b>"]
        for k, v in event.payload.items():
            lines.append(f"  {k}: <code>{v}</code>")
        return "\n".join(lines)
