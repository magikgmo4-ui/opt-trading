---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_CHAIN_SURFACE_PROOF_MAP
doc_type: surface_proof_map
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CHAIN_SURFACE_PROOF_MAP - Surfaces prouvées dans le repo

## Chaîne "TradingView/webhook → workers → Desk Pro → outputs"

| Segment | Surface | Preuve (chemins) | Statut |
| --- | --- | --- | --- |
| Ingestion webhook | Webhook server + parsing | `webhook_server.py` ; `modules/webhook/` | PRESENT |
| Normalisation signal | Signal router | `modules/signal_router/app/router.py` ; `modules/signal_router/app/schema.py` | PRESENT |
| Proposition | Proposition engine | `modules/proposition_engine/app/engine.py` ; `modules/proposition_engine/app/schema.py` | PRESENT |
| Validation | Gate | `modules/validation_gate/app/gate.py` ; `modules/validation_gate/app/schema.py` | PRESENT |
| Exécution | Trade executor (dry-run) | `modules/trade_executor/app/schema.py` ; `modules/trade_executor/` | PRESENT |
| Résultat | Result tracker | `modules/result_tracker/app/tracker.py` ; `modules/result_tracker/app/schema.py` | PRESENT |
| Journal (write intent) | Datasheet writer (dry-run) | `modules/datasheet_writer/` ; `scripts/sheets/sync_daily_session.py` | PRESENT (bounded) |
| Learning feed | Learning feeder (dry-run) | `modules/learning_feeder/app/feeder.py` ; `modules/learning_feeder/app/schema.py` | PRESENT |
| Consumer | Desk Pro dry-run synthesis | `modules/desk_pro/dry_run.py` | PRESENT |
| Consumer | Desk Pro API/UI | `modules/desk_pro/api/routes.py` ; `modules/desk_pro/ui/page.py` | PRESENT |
| Dispatcher | Notification dispatcher | `modules/notification_dispatcher/app/dispatcher.py` | PRESENT |
| Telegram outbound | Notification helper | `shared/telegram_notify.py` | PRESENT |
| Bot vision/headless | Capture/vision surfaces | `modules/bot_vision/` ; `modules/vision_bot/` ; `modules/bot_vision_step2/` ; `modules/desk_analyze/` | PRESENT (family, non-unifié) |
| LocalCMS | UI consumer | `modules/localcms/app/main.py` | PRESENT |

## Preuve E2E dry-run (sans side effects live)

| Artifact | Preuve | Notes |
| --- | --- | --- |
| Runner | `scripts/e2e/dry_run_pipeline.py` | JSON report, DRY_RUN=1/PAPER_MODE=1 par défaut |
| Tests | `tests/e2e/test_e2e_dry_run_pipeline.py` | Vérifie steps, invariants (no live trade, no write) |
| Desk Pro 3 inputs | `tests/test_desk_pro_combined_input_smoke.py` | Prouve jointure signal_event + visual_context + desk_snapshot |

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat observe :

```text
31 passed
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans implementation live
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_EVENT_TAXONOMY_01`
- `Gaps encore ouverts` : taxonomy transverse, routing Telegram, inbound screener, schema Sheets global
