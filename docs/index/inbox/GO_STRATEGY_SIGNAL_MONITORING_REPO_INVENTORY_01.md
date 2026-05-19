---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - signal_chain
  - repo_inventory
  - admin_trading
  - webhook
  - desk_pro
  - bot_vision
  - telegram
  - sheets
  - perf
links:
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/20_REUSE_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/90_REPRISE_POINT.md
---

# INBOX - GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01

## Objet

Inventorier l'état réel du repo pour la chaîne produit "Signal monitoring" (TradingView/webhook → workers → Desk Pro → Telegram/Sheets/Perf/Registry), pour éviter doublons et collisions avant toute implémentation lourde.

## Résultat

État établi :

- un pipeline E2E dry-run 7 workers existe et passe (no live trade, no writes) : `scripts/e2e/dry_run_pipeline.py` + `tests/e2e/test_e2e_dry_run_pipeline.py`
- Desk Pro a un mode dry-run de synthèse 3 inputs (signal_event, visual_context, desk_snapshot) : `modules/desk_pro/dry_run.py`
- Telegram : surface outbound existe (`shared/telegram_notify.py`) + surface botpress/adapter existe (`adapter_botpress_openclaw.py`), mais pas de parser inbound "screener trades/setups" dans cette chaîne
- Google Sheets : sync journal existe (`scripts/sheets/sync_daily_session.py`), mais le "global schema transverse" du bundle reste à définir avant toute écriture élargie

## Point de reprise

```text
docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md
docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/20_REUSE_MATRIX_AND_CONSTRAINTS.md
docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/90_REPRISE_POINT.md
```
