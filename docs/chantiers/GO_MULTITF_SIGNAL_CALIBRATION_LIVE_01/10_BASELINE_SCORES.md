# 10_BASELINE_SCORES — Scores multi-TF avant calibration

Capturé le 2026-06-15 à 17:15 UTC depuis admin-trading.

## Baseline par actif

| Actif | Biais HTF | Biais LTF | Alignement | Setup | Grade | Score | Proba | Confiance | Fraîcheur | Complétude |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | bearish | bearish | aligned | support_watch | C | 34 | 50% | 55% | fresh | 50% |
| ETH | bearish | bearish | aligned | support_watch | C | 34 | 50% | 55% | fresh | 50% |
| SOL | bearish | bearish | aligned | support_watch | C | 34 | 50% | 55% | fresh | 50% |
| XAUUSD | bearish | bearish | aligned | support_watch | C | 34 | 50% | 55% | fresh | 50% |
| SPCX | neutral | neutral | aligned | vwap_reclaim | B+ | 62 | 57% | 72% | fresh | 0% |

## Observations

- **BTC/ETH/SOL/XAUUSD** : tous C/34 (support_watch). Biais bearish aligné mais aucun trigger CDP fort. C'est correct — on attend vwap_loss, vwap_reclaim, ou ORB pour monter.
- **SPCX** : B+/62 (vwap_reclaim). Seul actif avec un signal CDP live. La complétude est 0% parce que SPCX n'a pas de market_metrics (prix vient du command_center) — mais le CDP trigger compense.
- Missing commun : `volume_confirmation`, `orderflow` — données non disponibles pour tous les actifs.
