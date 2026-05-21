---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01
status: closed
run_date: 2026-05-20
---

# 20_ACCEPTANCE_REPORT

## Livrable

`tools/strategy/daily_scalping/fetch_bitget.py` — fetcher XAUUSDT M5/M15 Bitget avec spread ticker.

## Run

```bash
python tools/strategy/daily_scalping/fetch_bitget.py --out data/market --days 30
```

### Données produites

| Fichier | Barres | Période | Spread |
|---|---|---|---|
| `data/market/xauusdt_m5_bitget.csv` | 8 599 | 2026-04-21 → 2026-05-21 | 0.01 USD (ticker snapshot) |
| `data/market/xauusdt_m15_bitget.csv` | 2 867 | 2026-04-21 → 2026-05-21 | 0.01 USD |

Champs : `timestamp, open, high, low, close, volume, bid, ask, spread, source, symbol, timeframe`

Source : `bitget_xauusdt_futures_approx`

## Backtest smoke (min_score=4)

Répertoire output : `artifacts/backtests/daily_scalping_bitget/`

| Variant | Trades | Expectancy R | PF | Verdict |
|---|---:|---:|---:|---|
| ORB_ONLY | 214 | -0.1442 | 0.792 | REJECT_VARIANT |
| VWAP_PULLBACK_ONLY | 25 | +0.4106 | 1.855 | NEED_MORE_DATA |
| SMC_SWEEP_ONLY | 1 | -1.0 | 0.0 | NEED_MORE_DATA |
| COMBINED_SMC_ORB_VWAP | 0 | — | — | NO_DATA |

### Observations

1. **ORB_ONLY REJECT** — cohérent avec le run GC=F. ORB breakout pur négatif sur les deux sources.
2. **VWAP_PULLBACK_ONLY +0.41R** — signal positif mais 25 trades insuffisants pour verdict (seuil = 100). À surveiller avec plus de données.
3. **SMC_SWEEP_ONLY 1 trade** — CHOCH same-bar toujours trop strict. Confirme que le rework CHOCH multi-bar est prioritaire.
4. **COMBINED 0 setups** — idem audit précédent, dépend du fix CHOCH.

## Critères d'acceptance

| Critère | Résultat |
|---|---|
| fetch_bitget.py s'exécute sans erreur | ✅ |
| CSV canonique produit avec tous les champs requis | ✅ |
| spread réel inclus (0.01 USD vs 3.0 pips hardcodé) | ✅ |
| source explicite `bitget_xauusdt_futures_approx` | ✅ |
| run_backtest.py compatible avec les CSV produits | ✅ |
| Limites documentées clairement | ✅ |

## Limites confirmées

- **Profondeur historique : ~30 jours M5** (Bitget API limit, testé 2026-05-20)
- **XAUUSDT ≠ XAUUSD spot broker** — instrument futures Bitget
- **Spread : snapshot unique au moment du fetch** — pas de données historiques bid/ask par bar
- **Classification finale : CONTEXT_RECENT_ONLY** (meilleur que GC=F smoke, pas PRIMARY_READY 180j)

## Décision

```
fetch_bitget.py = ACCEPTED comme source CONTEXT_RECENT_ONLY
Verdict backtest sur Bitget 30j = invalide pour décision stratégique
Bloquant 180j = MT5/Dukascopy toujours obligatoire pour verdict robuste
```

## Prochaines étapes

```
1. Obtenir MT5/Dukascopy export XAUUSD M5/M15 minimum 180 jours → verdict valide
2. Rework detectors.py CHOCH multi-bar → débloquer SMC_SWEEP et COMBINED
3. Valider VWAP_PULLBACK_ONLY +0.41R sur fenêtre 180j+ → signal potentiel à confirmer
```
