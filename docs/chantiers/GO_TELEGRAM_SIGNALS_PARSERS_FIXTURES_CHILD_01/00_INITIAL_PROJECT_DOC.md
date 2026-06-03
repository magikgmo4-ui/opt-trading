---
doc_id: GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
pf_id: PF_TELEGRAM_SCREENER
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
source_kind: canonical
created_at: 2026-06-03
updated_at: 2026-06-03
upstream:
  - GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_TELETHON_INTEGRATION_01
  - GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01
links:
  - docs/chantiers/GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01/10_SOURCE_OUTPUTS_AUDIT.md
  - docs/chantiers/GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01/20_SIGNAL_SCHEMA_DRAFT.md
---

# GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01

## Objectif

Transformer les messages Telegram deja collectes en fixtures et parseurs initiaux
de signaux exploitables metier, sans dependre d'un run live permanent.

## 1_MASTER_TARGET

```text
collector outputs -> message fixtures -> parser draft -> structured trading signal candidates
```

## 4_MASTER_PROJECT_PLAN

1. Auditer les outputs Telegram deja produits localement.
2. Definir un schema minimal de signal parse pour la phase fixtures.
3. Extraire un premier jeu de fixtures reelles a partir de `coinglass_alerts`.
4. Implementer un parseur minimal couvrant ce format prouve.
5. Ajouter des tests cibles sans dependance reseau.

## 12_INVARIANTS

- Aucun secret Telegram ne doit etre affiche ni copie.
- Aucun acces au fichier `/etc/opt-trading/env.d/roles/telegram_collector.env`.
- Aucun `getUpdates` tant que `bot_vision_step2.service` est actif.
- Pas de modification des index globaux.
- Pas de dependance a un run live permanent pour valider le parseur.

## 17_RESUME_POINT

```text
messages Telegram collectes -> fixtures locales -> parseur minimal coinglass -> signal structure partiel
```
