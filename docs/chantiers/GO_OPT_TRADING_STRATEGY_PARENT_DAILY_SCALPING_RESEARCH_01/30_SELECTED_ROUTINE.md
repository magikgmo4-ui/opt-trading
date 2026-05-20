---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_SELECTED_ROUTINE
doc_type: selected_strategy_routine
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: strategy_candidate
topic_keys: [opt-trading, strategy, daily_scalping, SMC_ORB_VWAP_SCALP_A_PLUS]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/20_STRATEGY_COMPARISON_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/40_SIGNAL_SCHEMA.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/50_BACKTEST_PROTOCOL.md
---

# 30_SELECTED_ROUTINE — SMC_ORB_VWAP_SCALP_A_PLUS

## 1_MASTER_TARGET

Routine daily scalping robuste et mesurable pour XAUUSD, indices et BTC, avec priorité test initiale sur XAUUSD M5/M15.

## 9_SELECTED_SOLUTION

```text
SMC_ORB_VWAP_SCALP_A_PLUS
```

## Logique générale

```text
HTF bias
-> active session
-> opening range or liquidity map
-> sweep or breakout
-> CHOCH/BOS confirmation
-> VWAP regime alignment
-> retest entry
-> partial TP
-> BE/trailing if valid
-> journal
-> review J+1
```

## Pré-session

- Définir le biais Daily / H4 / H1.
- Marquer high/low veille.
- Marquer Asia high/low pour XAU/FX.
- Marquer opening range pour indices/actions.
- Marquer zones de liquidité.
- Marquer VWAP session.
- Préparer scénario long, scénario short et no-trade zones.

## Setup long

Conditions minimales :

```text
- Prix proche support HTF ou low précédent.
- Sweep du low ou breakout/reclaim propre.
- Réaction impulsive.
- CHOCH M5 ou M15.
- BOS confirmé.
- Prix au-dessus ou reclaim VWAP selon contexte.
- Retest OB/FVG/VWAP/range edge.
- RR >= 1:1.8.
- Score >= 7/10.
```

Sortie :

```text
TP1 = liquidité interne / premier niveau évident
TP2 = niveau HTF ou liquidité opposée
SL = sous sweep / structure invalidante
```

## Setup short

Conditions minimales :

```text
- Prix proche résistance HTF ou high précédent.
- Sweep du high ou breakdown/reject propre.
- Réaction impulsive.
- CHOCH M5 ou M15.
- BOS confirmé.
- Prix sous ou rejet VWAP selon contexte.
- Retest OB/FVG/VWAP/range edge.
- RR >= 1:1.8.
- Score >= 7/10.
```

Sortie :

```text
TP1 = liquidité interne / premier niveau évident
TP2 = low opposé / support HTF
SL = au-dessus sweep / structure invalidante
```

## Score d'entrée /10

| Critère | Points |
| --- | ---: |
| Biais HTF clair | 2 |
| Zone de liquidité ou ORB claire | 2 |
| CHOCH/BOS confirmé | 2 |
| Retest propre | 1 |
| RR >= 1:1.8 | 1 |
| Session active | 1 |
| Spread/slippage acceptable | 1 |

Décision :

| Score | Décision |
| ---: | --- |
| 0-5 | NO_TRADE |
| 6 | WATCH_ONLY |
| 7-8 | VALID_TRADE |
| 9-10 | PREMIUM_SETUP |

## Risk engine

| Paramètre | Valeur initiale |
| --- | ---: |
| Risque par trade | 0.25% à 0.50% |
| Perte max quotidienne | 1.0% à 1.5% |
| Trades max jour | 2 à 4 |
| Pertes consécutives max | 2 |
| RR minimum | 1:1.8 |
| Score minimum | 7/10 |

## Interdictions

- Entrée avant retest sauf protocole spécifique non encore validé.
- Trade contre VWAP sans justification documentée.
- Trade après perte max jour.
- Signal Telegram exécuté brut.
- Trade sans screenshot avant/après.
- Re-entry automatique après stop.

## 13_ESTABLISHED

La routine est seulement `CANDIDATE`. Elle devient `VALIDATED` uniquement après backtest et paper forward.

## 16_TODO

Exécuter `50_BACKTEST_PROTOCOL.md` sur 100 occurrences XAUUSD M5/M15.
