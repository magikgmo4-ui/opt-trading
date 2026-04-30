---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01_MASTER_PLAN
doc_type: chantier_master_plan
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
status: draft
lifecycle_stage: planning
topic_keys:
  - opt-trading
  - strategy
  - indicator
  - macro
  - context_filter
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
---

# MASTER PLAN — Strategy Indicator Parent

## 1_MASTER_TARGET

Construire une couche d'indicateurs de contexte trading, utilisable comme filtre de regime pour les surfaces `desk`, `probabilities` et `OpenClaw`.

## 5_GO_PLAN

### Parent

`GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01`

### Child initial

`GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01`

## 6_FINAL_TARGET

Livrable de cette phase : structure documentaire parent + child, avec point de reprise clair et ruleset initial oil macro.

## Roadmap

1. `OPENING_DOCS` : creer le parent, le child et l'inbox.
2. `OIL_MACRO_SPEC` : definir les variables d'observation oil.
3. `OIL_MACRO_RULES` : formaliser la classification risk-on / risk-off.
4. `INTEGRATION_GAP` : lister les points d'integration futurs sans les implementer.

## 15_REMAINING_GAP

- Pas encore de schema de donnees.
- Pas encore de module runtime.
- Pas encore de logging backtest.

## 16_TODO

- Finaliser `02_RULES.md` du child oil.
- Decider si le prochain lot est `SPEC_ONLY`, `DATA_SCHEMA`, ou `PROBABILITIES_INTEGRATION`.
