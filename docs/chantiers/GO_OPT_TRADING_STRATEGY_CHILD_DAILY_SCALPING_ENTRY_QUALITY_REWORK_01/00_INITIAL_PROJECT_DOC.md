---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
updated_at: 2026-05-21
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01

## Contexte

Post GO_CHOCH_MULTI_BAR_REWORK_01 (PR #682) :
- SMC_SWEEP_ONLY : 306 trades, exp=-0.19R, pf=0.738 → **REJECT_VARIANT**
- Breakeven winrate à 1:1.8 RR = 35.7% — manquons la cible

## Diagnostic

**Problème 1 — SL mal placé**
Le simulateur calcule `sl = entry - 1.0 * ATR`. Mais sur un setup SWEEP_CHOCH :
- Entry = CHOCH bar close (déjà au-dessus du swing_h, à +10-20 pts du swept level)
- SL = entry - 1 ATR = potentiellement dans la zone de sweep
- Un simple retest du CHOCH niveau déclenche le SL

SL SMC correct : **sous le swept level** (swing_l - buffer pour un long).

**Problème 2 — Sessions Asia / Off-hours**
23 trades sur 306 en session "off", nombre significatif en "asia". Ces sessions ont
peu de volume, spreads larges, mouvements erratiques non-directionnels.

## Changements

| Fichier | Changement |
|---|---|
| `detectors.py` | Stocker `sweep_extreme` dans `Setup.extra` |
| `simulator.py` | SL = swept_level - 0.3×ATR (SMC) ; fallback 1×ATR si pas de swept_level |
| `simulator.py` | Filtrer sessions asia + off pour SMC/COMBINED |

## Critères d'acceptance

| Critère | Requis |
|---|---|
| SMC_SWEEP trades ≥ 100 | ✅ |
| Expectancy > -0.10R (amélioration vs -0.19R) | ✅ |
| Breakeven atteint (exp > 0) si possible | Cible stretch |
| Pas de look-ahead introduit | ✅ |
