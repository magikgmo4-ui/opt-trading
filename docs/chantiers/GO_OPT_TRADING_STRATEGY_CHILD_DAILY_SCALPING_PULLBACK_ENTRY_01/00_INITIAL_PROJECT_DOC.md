---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
updated_at: 2026-05-21
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01

## Contexte

Post GO_ENTRY_QUALITY_REWORK_01 (PR #683) :
- Vraie performance corrigée : SMC exp=-0.28R, COMBINED exp=-0.10R
- Cause identifiée : **entry au CHOCH bar close = entrée trop tardive**, loin de la structure
- Overlap seul : WR=37%, exp=+0.04R — signal marginal mais positif

## Changement clé

Ajouter une **phase de pullback** entre la confirmation CHOCH et l'entrée.

```
AVANT : entry_price = CHOCH_bar.close  (au-dessus de swing_h)
APRÈS : entry_price = swing_h           (pullback limit order au CHOCH level)
```

### Flow complet

```
bar[i-1] : low < swing_l              → sweep détecté
bar[i]   : close > swing_l            → récupération confirmée
bar[i..i+5] : close > swing_h         → CHOCH confirmé (bar j)
bar[j+1..j+10] : low ≤ swing_h        → pullback au CHOCH level
                  AND close > swing_l  → structure non cassée → ENTRY
```

### Géométrie résultante

```
Entry : swing_h  (limit order sur pullback)
SL    : swing_l - 0.1×ATR
Risk  : swing_h - swing_l + 0.1×ATR  ← structure range (petit et logique)
TP    : entry + risk × 1.8
```

Versus avant : risk = CHOCH_close - swing_l ≈ 2-5× le structure range.

## Critères d'acceptance

| Critère | Requis |
|---|---|
| SMC_SWEEP trades ≥ 80 (active sessions) | ✅ |
| Expectancy > 0R sur overlap session | ✅ |
| Expectancy > -0.10R global active sessions | ✅ |
| Pas de look-ahead | ✅ |
| setup_type = SWEEP_CHOCH_PULLBACK | ✅ |

## Scope

- **Modifie** : `tools/strategy/daily_scalping/detectors.py`
- **Modifie** : `tools/strategy/daily_scalping/simulator.py` (entry price = limit)
