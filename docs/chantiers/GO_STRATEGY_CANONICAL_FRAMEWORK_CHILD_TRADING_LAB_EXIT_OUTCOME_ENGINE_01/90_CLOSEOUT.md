---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
doc_type: closeout
status: CLOSED
---

# Closeout

## Résultat de validation

- `exit_outcome_v1.py` : 25/25 tests PASS (TestCalcTp, TestResolveExitOutcomeWin, TestResolveExitOutcomeLoss, TestResolveExitOutcomeAmbiguous, TestResolveExitOutcomeTimeout, TestGetPostEntryCandles)
- Intégration bout-en-bout : 10 sessions → 6 wins + 4 losses + 0 timeouts, avg_r=0.8
- Suite complète trading_lab_v1 : 78/81 PASS (3 failures pré-existantes dans param_sweep, non liées)

## Décision de conception

`entry_candle_ts` ajouté aux features et trades pour stocker le timestamp réel du chandelier d'entrée (vs `entry_ts` = horodatage d'exécution). `apply_outcomes` utilise `entry_candle_ts` en priorité.

## Limites connues

- Cross-contamination possible si les chandeliers post-entrée dépassent l'heure de la session suivante et que la session suivante a un TP/SL identique — non réaliste en pratique, géré par conception (chaque session se résout dans sa propre fenêtre temporelle dans le CSV de référence).
- `max_bars=60` par défaut; configurable par appel.

## Prochaine étape recommandée

Connecter `apply_outcomes` au pipeline complet et mesurer le vrai `perf_status` avec données broker réelles (`state/trading_lab_v1/inputs/`).
