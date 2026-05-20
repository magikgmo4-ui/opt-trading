---
doc_id: GO_EVENT_TAXONOMY_01_EVENT_FAMILY_MAPPING
doc_type: mapping
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_EVENT_FAMILY_MAPPING - Types ↔ familles ↔ routing

## Familles (V1)

| Family | Description | Surfaces concernées |
| --- | --- | --- |
| `SIGNAL` | Signal initial (TV/webhook/headless) | webhook, signal_router, Desk Pro |
| `DECISION` | Proposition + gate decision | proposition_engine, validation_gate |
| `EXECUTION` | Exécution + résultat + closeout | trade_executor, result_tracker |
| `JOURNAL` | Écritures et sync (dry-run d’abord) | datasheet_writer, sheets sync |
| `LEARNING` | Feed/bricks (dry-run d’abord) | learning_feeder |
| `DESK` | Synthèse Desk Pro (inputs/joins) | desk_pro dry_run |
| `NOTIFY` | Notifications (Telegram outbound) | dispatcher, telegram_notify |

## Types (cibles)

| Event type | Family | Payload candidat (repo) |
| --- | --- | --- |
| `signal_event.v1` | SIGNAL | dict V1 (`modules/desk_pro/signal_event_adapter.py`) |
| `normalized_signal.v1` | SIGNAL | NormalizedSignal (`modules/signal_router/app/schema.py`) |
| `proposition.v1` | DECISION | Proposition (`modules/proposition_engine/app/schema.py`) |
| `gate_decision.v1` | DECISION | GateDecision (`modules/validation_gate/app/schema.py`) |
| `trade_result.v1` | EXECUTION | TradeResult (`modules/trade_executor/app/schema.py`) |
| `trade_record.v1` | EXECUTION | TradeRecord (`modules/result_tracker/app/schema.py`) |
| `sheets_write_intent.v1` | JOURNAL | WriteResult (dry-run) |
| `learning_feed_result.v1` | LEARNING | FeedResult (`modules/learning_feeder/app/schema.py`) |
| `desk_pro_synthesis.v1` | DESK | dict synthesis (`modules/desk_pro/dry_run.py`) |
| `telegram_outbound_intent.v1` | NOTIFY | dict dispatcher intent (à canoniser) |

## Routing impact (next GO)

Le mapping ci-dessus est le pré-requis direct de:

```text
GO_TELEGRAM_EVENT_ROUTING_MAP_01
```

## Ancrage umbrella

- `MASTER_TARGET` : rendre interoperables les chaines du produit final total
- `Kanban bundle` : reste la carte de navigation principale
- `Prochain item Kanban exact` : `GO_TELEGRAM_EVENT_ROUTING_MAP_01`
- `Gaps encore ouverts` : alias/destinations Telegram, policy par famille d'evenements, jonction future avec inbound screener
