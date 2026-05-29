---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01
pf_id: PF_TELEGRAM_INGESTION
status: open
lifecycle_stage: implementation
surface: modules/telegram_ingestion
source_kind: canonical
created_at: 2026-05-29
updated_at: 2026-05-29
upstream:
  - GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01/10_INBOUND_SPEC.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01

## Objectif

Implémenter la distribution des messages normalisés vers les consommateurs (Telegram Screener, Desk Pro, Data Center).

Prend InboundMessage en entrée, route vers les consumers enregistrés par canal.

## 1_MASTER_TARGET

```text
ConsumerRouter : InboundMessage → dispatch vers consumers enregistrés par canal
```

## 4_MASTER_PROJECT_PLAN

1. **Consumer protocol** : interface Consumer.handle(message)
2. **ConsumerRouter** : routing table canal → liste de consumers, dispatch
3. **ScreenerConsumer** (stub) : consomme InboundMessage pour ScreenerPipeline
4. **Tests** : routing par canal, dispatch, consumer mock

## 12_INVARIANTS

- Aucun appel réseau
- Aucune modification de l'inbound parser ou normalizer existant
- Aucune connexion live à Screener, Desk Pro, Data Center
- Tous les tests unitaires sans side-effect

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01
```
