---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
pf_id: PF_TELEGRAM_SCREENER
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - PF_TELEGRAM_INGESTION
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/20_REGISTRY_SCHEMA_TARGET.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01

## Objectif

Promouvoir le channel registry Telegram Screener de **doc-only** vers **runtime testable**.
Le schéma YAML défini dans `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` est materialisé
sous `modules/telegram_screener/registry/` avec loader, validation et tests.

## 1_MASTER_TARGET

```text
channel registry doc-only → runtime : fichier YAML, loader validé, tests, prêt pour ingestion
```

## 4_MASTER_PROJECT_PLAN

1. **YAML schema** : materialiser `registry/telegram_screener_channels.yaml` au format V1
2. **Registry loader** : `modules/telegram_screener/registry/loader.py` charge et valide le YAML
3. **Validation** : trust_tier A/B/C/D, catégories, parsers attendus, enabled flag
4. **Tests** : valider chargement, invalide, malformed, enabled/disabled
5. **Fixtures** : YAML fixtures représentatifs

## 12_INVARIANTS

- Aucun id/channel réel dans le repo
- enabled=false par défaut
- Pas de modification des services existants
- Aucun appel Telegram live
- Pas de modification des index globaux

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01
```
