---
doc_id: GO_EVENT_TAXONOMY_01_CURRENT_EVENT_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_EVENT_SURFACES - Surfaces et formats existants

## Ingestion

| Surface | Preuve (chemins) | Format actuel |
| --- | --- | --- |
| Webhook | `webhook_server.py` ; `modules/webhook/` | payloads dict + `schemas/webhook_event_v1.json` |
| TradingView normalized signal | `modules/signal_router/app/schema.py` | NormalizedSignal (dataclass) |

## Workers (pipeline dry-run prouvé)

| Step | Preuve (chemins) | Format actuel |
| --- | --- | --- |
| signal_router | `modules/signal_router/app/router.py` | NormalizedSignal |
| proposition_engine | `modules/proposition_engine/app/schema.py` | Proposition / PropositionRequest |
| validation_gate | `modules/validation_gate/app/schema.py` | GateDecision / GateRequest |
| trade_executor | `modules/trade_executor/app/schema.py` | TradeResult / TradeRequest |
| result_tracker | `modules/result_tracker/app/schema.py` | TradeRecord / CloseRequest |
| datasheet_writer | `modules/datasheet_writer/` | WriteResult (dry-run) |
| learning_feeder | `modules/learning_feeder/app/schema.py` | FeedResult / FeedRequest |

Preuve d’exécution: `scripts/e2e/dry_run_pipeline.py` + `tests/e2e/test_e2e_dry_run_pipeline.py`.

## Desk Pro hub

| Surface | Preuve (chemins) | Format actuel |
| --- | --- | --- |
| signal_event (Desk Pro) | `modules/desk_pro/signal_event_adapter.py` | dict V0 → dict V1 (`signal_event` V1) |
| dry-run synthesis 3 inputs | `modules/desk_pro/dry_run.py` | dict (synthèse + warnings/errors + join_checks) |
| API/UI | `modules/desk_pro/api/routes.py` ; `modules/desk_pro/ui/page.py` | HTTP + HTML |

## Notifications / Telegram

| Surface | Preuve (chemins) | Format actuel |
| --- | --- | --- |
| outbound helper | `shared/telegram_notify.py` | fonction utilitaire (texte + token/chat) |
| dispatcher | `modules/notification_dispatcher/app/dispatcher.py` | events dict internes (non canonisés) |

## Sheets / Journal

| Surface | Preuve (chemins) | Format actuel |
| --- | --- | --- |
| sync daily session | `scripts/sheets/sync_daily_session.py` | mapping colonnes + dry-run possible |

## Conclusion

L’écosystème existe déjà mais parle plusieurs dialectes (dataclasses vs dicts). L’objectif du GO est d’introduire une enveloppe canonique minimale qui “wrap” ces objets sans casser les surfaces existantes.

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest tests\test_signal_event_adapter.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat observe :

```text
61 passed
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans changement runtime
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_TELEGRAM_EVENT_ROUTING_MAP_01`
- `Gaps encore ouverts` : canonisation complete des intents NOTIFY, articulation inbound Telegram, propagation Sheets/Perf/Registry
