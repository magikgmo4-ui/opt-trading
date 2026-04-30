---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01_SPEC
doc_type: chantier_spec
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01
status: draft
lifecycle_stage: specification
topic_keys:
  - oil
  - macro
  - risk_on
  - risk_off
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/00_CADRAGE.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/02_RULES.md
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/02_RULES.md
---

# SPEC — Oil Macro Indicator

## Role

Indicateur de contexte macro, non signal d'execution autonome.

## Inputs candidats

- WTI daily change
- Brent daily change
- variation 3 jours
- variation 5 jours
- DXY
- BTC / ETH reaction
- inventaires oil
- decisions OPEC+
- evenements logistiques ou geopolitique energy

## Output cible

Classification simple :

- `RISK_ON_SUPPORTIVE`
- `NEUTRAL_RANGE`
- `RISK_OFF_PRESSURE`
- `EVENT_SPIKE_UNSTABLE`

## Rattachement trading

Le signal doit alimenter un filtre de contexte :
- reduire agressivite long crypto si oil spike + DXY fort ;
- autoriser regime plus favorable si oil stable/baisse + DXY faible ;
- bloquer les conclusions fortes si evenement news-driven non stabilise.

## Hors perimetre V1

- execution automatique ;
- prediction de prix oil ;
- signal direct sur futures oil ;
- integration broker.
