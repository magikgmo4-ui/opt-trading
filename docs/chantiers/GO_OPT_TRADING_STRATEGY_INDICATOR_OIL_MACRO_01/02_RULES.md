---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01_RULES
doc_type: chantier_rules
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01
status: draft
lifecycle_stage: ruleset
topic_keys:
  - oil
  - macro
  - rules
  - risk_filter
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/03_TODO.md
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
---

# RULES — Oil Macro Indicator V1

## Regle de lecture principale

Oil sert de proxy de pression inflation / logistique / geopolitique, donc de contexte de risk appetite.

## Mapping initial

| Condition | Lecture | Output |
| --- | --- | --- |
| Oil hausse rapide + DXY fort | inflation/risk-off pressure | `RISK_OFF_PRESSURE` |
| Oil hausse violente sur news | regime instable | `EVENT_SPIKE_UNSTABLE` |
| Oil range + DXY neutre | contexte propre | `NEUTRAL_RANGE` |
| Oil baisse + DXY faible | support risk-on | `RISK_ON_SUPPORTIVE` |

## Invariants

- Ne jamais convertir ce signal en ordre automatique.
- Ne jamais ignorer le contexte DXY / BTC / SPX.
- Ne pas conclure si la hausse oil vient seulement d'une news non confirmee.

## Points a quantifier plus tard

- seuil variation 1 jour ;
- seuil variation 3 jours ;
- seuil variation 5 jours ;
- confirmation par DXY ;
- fenetre de cooldown apres event spike.
