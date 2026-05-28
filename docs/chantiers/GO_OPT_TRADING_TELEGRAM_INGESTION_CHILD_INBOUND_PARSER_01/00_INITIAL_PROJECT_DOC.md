---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01
pf_id: PF_TELEGRAM_INGESTION
status: open
lifecycle_stage: implementation
surface: modules/telegram_ingestion
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - PF_TELEGRAM_INGESTION
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01 — INITIAL_PROJECT_DOC

## Objectif

Implémenter le parser inbound Telegram pour ingérer les messages depuis l'API Telegram,
les normaliser et les distribuer aux consommateurs (Screener, Desk Pro, Data Center).

## 1_MASTER_TARGET

```text
Telegram API -> inbound parser -> normalized message -> consumers
```

## 4_MASTER_PROJECT_PLAN

1. **Inbound parser** : implémenter la lecture via Telethon/API Telegram.
2. **Message normalizer** : normaliser les messages bruts en format canonique.
3. **Consumer router** : router les messages vers Screener, Desk Pro, Data Center.
4. **Tests** : valider l'ingestion et la normalisation.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01
```
