---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01
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
  - PF_DATA_CENTER
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01/10_PARSER_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01/20_TEST_PLAN.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01 — INITIAL_PROJECT_DOC

## Objectif

Implémenter le parser des signaux screener Telegram. Les messages inbound
provenant de `PF_TELEGRAM_INGESTION` sont parsés en signaux normalisés
(trade setups, news, alertes) et transmis à Desk Pro.

## 1_MASTER_TARGET

```text
Telegram screener signal -> parser -> normalized signal -> Desk Pro
```

## 4_MASTER_PROJECT_PLAN

1. **Parser spec** : définir le format des signaux attendus par canal/type.
2. **Trade parser** : parser les trade setups (entry, SL, TP, size, pair).
3. **News parser** : parser les alertes macro/news économiques.
4. **Normalisation** : produire un screener signal canonique.
5. **Tests** : valider le parsing sur des échantillons réels.

## 12_INVARIANTS

- Pas de modification runtime des services existants (webhook, perf, etc.).
- Pas de modification des index globaux.
- Le parser doit être testable sans connexion Telegram live.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01
```
