---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: child_chantier_initial
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
strategy_version: "0.1.0"
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
constraints:
  - no_runtime_mutation
  - no_live_trade
  - no_bitget_order
  - no_automatic_sheets_write
  - no_secrets
---

# GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01

## 00_INITIAL_PROJECT_DOC

---

## 1_OBJECTIF

Appliquer le framework strategique canonique (PR #530) au premier `strategy_id`
concret : `SMC_ICT_CHOCH_BOS_RETEST`.

Ce child est doc-first.

Il produit un ensemble de documents qui permettent :

- Definition complete du spec `SMC_ICT_CHOCH_BOS_RETEST v0.1.0`;
- Regles de detection SMC/ICT : CHoCH, BOS, MSS, Sweep, Liquidity, FVG, OB, premium/discount;
- Mapping `ObservationEvent` pour l'enrichissement;
- Scoring initial de confiance;
- Protocole Telegram watch signal pour ce strategy_id;
- Metriques Perf Engine attendues;
- Protocole Trading Lab replay;
- Criteres de promotion et de retrait.

---

## 2_STRATEGY_IDENTITY

| Champ | Valeur |
| --- | --- |
| `strategy_id` | `SMC_ICT_CHOCH_BOS_RETEST` |
| `strategy_version` | `0.1.0` |
| `setup_type` | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` |
| `direction` | `WATCH_ONLY` (initial) |
| `symbol` scope | BTC/USD, ETH/USD, toute paire liquide |
| `timeframe` principal | `15m` (confirmation entry); context `1h`, `4h` |
| `signal_source` | `bot_vision`, `tradingview`, `manual` |
| `observation_status` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |

---

## 3_SCOPE_DU_CHILD

Ce child couvre :

```text
10_STRATEGY_SPEC_SMC_ICT_CHOCH_BOS_RETEST.md
20_SMC_ICT_RULES_CHOCH_BOS_MSS.md
30_SMC_ICT_RULES_SWEEP_LIQUIDITY.md
40_SMC_ICT_RULES_FVG_OB_PREMIUM_DISCOUNT.md
50_OBSERVATION_EVENT_MAPPING.md
60_SCORING_INITIAL.md
70_TELEGRAM_WATCH_SIGNAL.md
80_PERF_ENGINE_METRICS.md
90_TRADING_LAB_REPLAY.md
95_PROMOTION_RETIREMENT_CRITERIA.md
99_CLOSEOUT_CRITERIA.md
```

Ce child ne couvre pas :

```text
runtime implementation
module creation
scheduler setup
Bitget integration
Sheets automation
live trading
```

---

## 4_HERITAGE_DU_PARENT

Ce child herite directement du framework parent (`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`) :

| Section parente | Application dans ce child |
| --- | --- |
| `20_STRATEGY_CANONICAL_SPEC_SCHEMA` | Instanciation concrete pour SMC_ICT |
| `30_STRATEGY_LIFECYCLE_GATES` | Gates appliquees a SMC_ICT |
| `40_OBSERVATION_EVENT_EXTENSION` | Mapping observe pour SMC_ICT |
| `60_PERF_ENGINE_STRATEGY_EVALUATION` | Metriques SMC_ICT specifiques |
| `70_TELEGRAM_WATCH_SIGNAL_PROTOCOL` | Payload concret SMC_ICT |
| `80_TRADING_LAB_REPLAY_PROTOCOL` | Artefacts SMC_ICT |

---

## 5_CONTRAINTES

| Contrainte | Statut |
| --- | --- |
| doc-only | Oui |
| no runtime mutation | Oui |
| no live trade | Oui |
| no Bitget order | Oui |
| no automatic Sheets write | Oui |
| no secrets | Oui |
| ne pas modifier index globaux sauf necessite explicite | Oui |

---

## 6_VERDICT_ATTENDU

```text
PASS_SMC_ICT_STRATEGY_CHILD_DOC_ONLY_OPENED
```

## RISKS

- À qualifier.
