---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_TELETHON_INTEGRATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_TELETHON_INTEGRATION_01
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
  - GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_TELETHON_INTEGRATION_01

## Objectif

Implémenter le vrai client Telegram via Telethon. Connecte l'API Telegram live,
implémente InboundClient protocol, gère l'authentification (API ID, API hash, session).

Dernier gap pour CLOSE_GATE du parent PF_TELEGRAM_INGESTION.

## 1_MASTER_TARGET

```text
TelethonInboundClient : Telethon → InboundClient protocol avec authentification et mapping messages
```

## 4_MASTER_PROJECT_PLAN

1. **Telethon dependency** : ajouter telethon à requirements.txt
2. **TelethonInboundClient** : implémente InboundClient protocol via Telethon, lazy import, auth management
3. **Tests** : 100% mock Telethon, pas d'appel live, 0 secret dans le repo
4. **Smoke test pattern** : test dry-run validable localement avec credentials .env

## 12_INVARIANTS

- Aucun appel Telegram live dans les tests
- Aucun secret / API ID / API hash dans le repo
- Telethon importé lazy (try/except pour graceful degradation)
- InboundClient protocol inchangé
- Tous les tests unitaires sans réseau

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_TELETHON_INTEGRATION_01
```
