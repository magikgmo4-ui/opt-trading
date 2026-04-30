---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01
status: draft
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - oil
  - macro
  - indicator
  - crypto
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/02_RULES.md
---

# GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01 — cadrage child

## 3_INITIAL_NEED

Formaliser l'indicateur oil macro comme filtre de contexte trading pour anticiper le regime risk-on / risk-off qui peut affecter crypto, indices et sentiment global.

## 6_FINAL_TARGET

Produire une specification initiale exploitable pour :
- observer WTI / Brent ;
- qualifier le regime oil ;
- mapper oil -> inflation -> policy -> risk appetite -> crypto ;
- preparer une integration future dans desk / probabilities / OpenClaw.

## 13_ESTABLISHED

- Oil est un indicateur macro de contexte.
- Oil ne doit pas devenir un signal unique d'entree en position.
- La premiere phase reste documentaire.

## 14_HYPOTHESIS

- Une hausse rapide oil + DXY fort peut indiquer un regime risk-off crypto.
- Une baisse oil + DXY faible peut soutenir un regime risk-on.

## 17_RESUME_POINT

Reprendre par `01_SPEC.md`, puis verrouiller les regles dans `02_RULES.md`.
