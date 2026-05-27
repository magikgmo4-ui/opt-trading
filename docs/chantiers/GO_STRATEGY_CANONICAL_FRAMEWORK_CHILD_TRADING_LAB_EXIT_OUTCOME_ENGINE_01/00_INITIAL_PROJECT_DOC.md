---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
status: CLOSED
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK
---

# GO: Trading Lab Exit Outcome Engine

## Objectif

Implémenter un moteur de résolution d'issue déterministe pour les trades virtuels dans `trading_lab_v1`. Convertir les trades `virtual_open` en résultats mesurables (win/loss/timeout) en scannant les chandeliers post-entrée pour détecter un hit TP ou SL.

## Contrat de sortie

- `result` ∈ {`win`, `loss`, `timeout`}
- `win` : high >= tp (bullish) ou low <= tp (bearish)
- `loss` : low <= sl (bullish) ou high >= sl (bearish)
- même chandelier SL+TP → `loss` conservative (`sl_tp_same_candle_conservative_loss`)
- `timeout` : max_bars atteint sans hit, ou aucun chandelier post-entrée
- `r_realized` = `rr_planned` (win), `-1.0` (loss), `None` (timeout)

## Fichiers produits

- `modules/trading_lab_v1/app/exit_outcome_v1.py` — moteur de résolution
- `modules/trading_lab_v1/tests/test_exit_outcome_v1.py` — 25 tests
- `modules/trading_lab_v1/app/trading_lab_v1.py` — commande `apply-outcomes` + batch report enrichi
- `modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv` — étendu à 92 lignes (post-entrée ciblés)
