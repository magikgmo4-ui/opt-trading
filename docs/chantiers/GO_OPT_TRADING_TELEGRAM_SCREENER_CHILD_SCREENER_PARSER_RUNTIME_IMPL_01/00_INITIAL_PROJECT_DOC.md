---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_RUNTIME_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_RUNTIME_IMPL_01
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
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01/10_PARSER_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01/20_TEST_PLAN.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_RUNTIME_IMPL_01 — INITIAL_PROJECT_DOC

## Objectif

Transformer le child parser Telegram Screener de **spec/doc** vers **runtime testable**.

Le context reader (`signal_context_reader.py`) existe déjà — le présent GO implémente
le parsing des messages Telegram bruts (trade setups, news/alertes, alpha) en structures
stables, sans appel Telegram live.

## 1_MASTER_TARGET

```text
raw telegram message -> telegram_screener parser -> normalized signal -> prêt pour signal producer
```

## 4_MASTER_PROJECT_PLAN

1. **Parser runtime** : créer `modules/telegram_screener/parser/` avec les parseurs spécialisés
2. **Trade parser** : parser les trade setups (entry, SL, TP, size, pair)
3. **News parser** : parser les alertes macro/news économiques
4. **Alpha parser** : parser les signaux alpha (ticker + message)
5. **Normalisation** : produire un screener signal canonique via `signal_normalizer.py`
6. **Fixtures** : échantillons représentatifs de messages Telegram
7. **Tests** : valider le parsing sur des échantillons, sans connexion réseau

## 12_INVARIANTS

- Pas de modification des services existants (webhook, perf, etc.)
- Pas de modification des index globaux (sauf chantier du GO)
- Pas d'appel Telegram live / API externe
- Fixtures-first, tests obligatoires
- Ne pas ouvrir signal producer avant parser runtime prouvé

## 17_RESUME_POINT

```text
Chantier courant recommandé:
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_RUNTIME_IMPL_01

Pourquoi:
le context reader existe, mais les messages Telegram bruts ne sont pas encore normalisés.

Après:
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01
```
