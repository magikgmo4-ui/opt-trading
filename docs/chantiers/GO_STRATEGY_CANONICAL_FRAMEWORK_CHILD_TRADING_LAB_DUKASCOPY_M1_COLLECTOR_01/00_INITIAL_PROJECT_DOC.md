---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
status: CLOSED
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
---

# GO: Dukascopy XAUUSD M1 Collector

## Objectif

Créer un collecteur read-only pour obtenir des données XAUUSD M1 historiques depuis le public datafeed Dukascopy et produire un CSV local compatible avec `trading_lab_v1 run-with-outcomes`.

## Résultat

- Source Dukascopy HTTP publique : **accessible, aucune authentification requise**
- Collecteur implémenté : `tools/trading_lab/collect_dukascopy_xauusd_m1.py`
- Smoke test : 5 jours (2026-04-07 à 2026-04-11) → 8640 candles
- Pipeline intégré sur données réelles :
  12 sessions → **1W / 9L / 2T, avg_r=-0.7**
- `perf_status` : toujours `UNMEASURED` (8 jours ≪ seuil de 30+)
