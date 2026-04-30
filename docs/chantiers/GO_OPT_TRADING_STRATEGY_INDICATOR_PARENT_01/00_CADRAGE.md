---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01_CADRAGE
 doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strategy
  - indicator
  - macro
  - trading
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/01_MASTER_PLAN.md
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/00_CADRAGE.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md
---

# GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01 — cadrage parent

## 3_INITIAL_NEED

Creer un chantier parent strategie / indicateur pour centraliser les indicateurs de contexte trading et ouvrir le premier sous-chantier sur le signal macro oil.

## 4_MASTER_PROJECT_PLAN

1. Definir une famille documentaire `strategy_indicator`.
2. Stabiliser le role des indicateurs : filtre de contexte, pas signal unique d'execution.
3. Ouvrir un premier child : `GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01`.
4. Preparer l'integration future vers desk / probabilities / OpenClaw sans patch runtime dans cette phase.

## 7_CANONICAL_STATE

- Parent ouvert sur branche dediee `go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01`.
- Premier child prevu : oil macro indicator.
- Phase actuelle : documentation / cadrage.

## 11_KEY_DECISIONS

- Les indicateurs de contexte servent a qualifier le regime de marche.
- Le signal oil est traite comme indicateur macro de risk-on / risk-off.
- Aucun code runtime n'est modifie dans cette ouverture.

## 12_INVARIANTS

- Patch minimal.
- Pas de refonte globale.
- Pas d'autotrading derive de ce chantier sans GO explicite.
- Les docs chantier restent sous `docs/chantiers/<GO_ID>/`.

## 17_RESUME_POINT

Reprendre par la specification du child oil macro et ses regles de classification.
