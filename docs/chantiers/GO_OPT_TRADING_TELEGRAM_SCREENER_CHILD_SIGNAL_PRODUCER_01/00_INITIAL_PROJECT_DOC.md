---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01
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
  - GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01
  - PF_DESK_PRO
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01/10_PARSER_SPEC.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01 — INITIAL_PROJECT_DOC

## Objectif

Produire des screener signals normalisés depuis les signaux parsés par le parser GO,
et les transmettre à Desk Pro pour affichage.

## 1_MASTER_TARGET

```text
parsed signal -> signal producer -> normalized screener signal -> Desk Pro
```

## 4_MASTER_PROJECT_PLAN

1. **Signal schema** : définir le format du screener signal pour Desk Pro.
2. **Signal producer** : transformer les signaux parsés en screener signals.
3. **Desk Pro adapter** : adapter le signal pour la consommation Desk Pro.
4. **Tests** : valider la production de signaux.

## 12_INVARIANTS

- Pas de modification runtime des services existants.
- Pas de modification des index globaux.
- Format du signal compatible avec Desk Pro existant.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01
```
