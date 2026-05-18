---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01_SIGNAL_SCHEMA
repo: opt-trading
project: opt-trading
module: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01
doc_type: signal_schema
status: draft
lifecycle_stage: parent_spec
topic_keys: [telegram, latency, strategy, signal, schema]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-17
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/10_STRATEGY_SPEC.md
---

# 20_SIGNAL_SCHEMA — Telegram Latency Normalized Signal

## Objectif

Définir le schéma canonique minimal pour convertir un message Telegram en signal exploitable par la stratégie `Telegram Signal Latency Reaction Strategy`.

## Pipeline signal

```text
telegram_message_raw
→ parser
→ normalized_signal
→ market_snapshot_t0
→ latency_window
→ paper_decision
→ replay_event
→ perf_result
```

## Input brut

```json
{
  "source": "telegram",
  "channel_id": "string",
  "channel_name": "string",
  "message_id": "string",
  "message_text": "string",
  "message_timestamp_utc": "ISO-8601",
  "ingest_timestamp_utc": "ISO-8601",
  "collector": "telegram_listener|opencode|openclaw",
  "raw_payload_ref": "path-or-db-ref"
}
```

## Signal normalisé

```json
{
  "strategy_id": "telegram_latency_reaction_v1",
  "event_id": "string",
  "go_id": "GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01",
  "symbol": "BTCUSDT",
  "asset_class": "crypto|forex|index|commodity|unknown",
  "direction": "BUY|SELL|LONG|SHORT|UNKNOWN",
  "entry_hint": "market|limit|range|unknown",
  "targets": ["number"],
  "stop_loss": "number|null",
  "confidence_parser": 0.0,
  "confidence_signal": 0.0,
  "t0_message_utc": "ISO-8601",
  "t0_ingest_utc": "ISO-8601",
  "latency_ingest_ms": 0,
  "status": "parsed|rejected|ambiguous|watch_only"
}
```

## Snapshot marché T0

```json
{
  "event_id": "string",
  "symbol": "BTCUSDT",
  "exchange": "binance|bitget|bybit|unknown",
  "snapshot_timestamp_utc": "ISO-8601",
  "bid": 0.0,
  "ask": 0.0,
  "mid": 0.0,
  "last": 0.0,
  "spread_bps": 0.0,
  "volume_1m": 0.0,
  "volume_5m": 0.0,
  "volatility_1m_bps": 0.0,
  "volatility_5m_bps": 0.0,
  "liquidity_score": 0.0,
  "data_quality": "ok|partial|missing|stale"
}
```

## Décision V1

```json
{
  "event_id": "string",
  "mode": "watch_only|paper|replay",
  "decision": "observe|simulate_entry|reject",
  "reject_reason": "ambiguous_signal|missing_market_data|spread_too_wide|liquidity_too_low|duplicate|late_ingest|null",
  "entry_price_simulated": 0.0,
  "take_profit_bps": 0.0,
  "timeout_seconds": 0,
  "risk_note": "string"
}
```

## Résultat replay / paper

```json
{
  "event_id": "string",
  "mode": "paper|replay",
  "entry_timestamp_utc": "ISO-8601",
  "exit_timestamp_utc": "ISO-8601",
  "exit_reason": "tp|timeout|invalidated|data_gap",
  "max_favorable_excursion_bps": 0.0,
  "max_adverse_excursion_bps": 0.0,
  "net_result_bps_before_costs": 0.0,
  "estimated_cost_bps": 0.0,
  "net_result_bps_after_costs": 0.0,
  "latency_to_peak_seconds": 0,
  "verdict": "pass|fail|inconclusive"
}
```

## Rejets obligatoires

Un signal doit être rejeté si :

- direction absente ou contradictoire ;
- symbole absent ;
- données marché trop anciennes ;
- spread supérieur au seuil V1 ;
- liquidité insuffisante ;
- message déjà traité ;
- canal hors liste d’observation ;
- mode runtime réel demandé sans GO d’exécution validé.

## Invariants sécurité

- Aucun ordre réel en V1.
- Aucun secret dans les logs.
- Aucun token Telegram dans les artefacts.
- Les identifiants de canaux privés doivent rester externalisés.
- Les captures Bot Vision doivent être stockées par référence, pas inline.

## Point de reprise

Le prochain document doit définir replay/backtest, fenêtres temporelles, coûts et critères de passage watch-only → paper.