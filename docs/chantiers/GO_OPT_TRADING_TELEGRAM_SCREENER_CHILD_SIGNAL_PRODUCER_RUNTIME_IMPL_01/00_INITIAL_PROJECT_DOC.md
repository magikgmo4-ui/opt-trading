---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01
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
  - GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_RUNTIME_IMPL_01
  - PF_DESK_PRO
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01/10_SIGNAL_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01

## Objectif

Produire des screener signals normalisés depuis les signaux parsés
(ScreenerSignal), et les adapter au format telegram_claim.v1 pour Desk Pro.

## 1_MASTER_TARGET

```text
parsed signal -> signal producer -> normalized screener signal -> Desk Pro
```

## 4_MASTER_PROJECT_PLAN

1. **Signal producer** : transformer les signaux parsés en ScreenerProducedSignal
2. **Desk Pro adapter** : adapter au format telegram_claim.v1
3. **Tests** : valider production + adaptation

## 12_INVARIANTS

- Pas de modification runtime des services existants
- Pas de modification des index globaux
- Aucune dépendance réseau
- Parser déjà livré — le producer le consomme uniquement

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01
```
