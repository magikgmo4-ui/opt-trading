---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_RUNTIME_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_RUNTIME_01
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
  - PF_TELEGRAM_SCREENER
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01/10_INBOUND_SPEC.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_RUNTIME_01

## Objectif

Implémenter le runtime du parser inbound Telegram : client API mockable + receiver de messages + schéma de données.

Le child GO `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01` a défini le spec et le test plan (doc-only, PASS). Ce GO réalise l'implémentation runtime.

## 1_MASTER_TARGET

```text
InboundParserRuntime : TelegramClient abstraction + MessageReceiver + RawMessage schema
→ messages Telegram ingérés en RawMessage normalisé, mocké pour les tests, prêt pour normalizer downstream
```

## 4_MASTER_PROJECT_PLAN

1. **Message Schema** : dataclasses RawMessage / InboundMessage
2. **TelegramClient abstraction** : protocol/ABC mockable (get_messages, iter_messages, add_event_handler)
3. **MessageReceiver** : polling layer qui utilise le client pour recevoir des messages
4. **Tests** : 100% mock, 0 réseau, 0 secret, 0 dépendance Telethon en runtime test

## 12_INVARIANTS

- Aucun appel Telegram live dans les tests
- Aucun secret / token / chat_id dans le repo
- Aucune dépendance à Telethon dans les tests (mocké)
- Tous les tests sont unitaires sans réseau
- Le module peut être importé sans side-effect

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_RUNTIME_01
```
