---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
doc_type: closeout
status: CLOSED
verdict: PASS_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
---

# Closeout

## Verdict

`PASS_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01`

Source Dukascopy accessible. Collecteur implémenté et validé. Pipeline end-to-end sur données réelles PASS.

## Tests

- `test_collect_dukascopy_m1.py` : 22/22 PASS
- Suite complète : 87/87 PASS (adapter + exit_outcome + pipeline_integration + collector)
- Validation registry : WARNINGS pre-existing uniquement

## Smoke test end-to-end

```
Collecte : 5 jours XAUUSD M1 → 8640 candles
Pipeline : 12 sessions → 1W / 9L / 2T, avg_r=-0.7
State/   : non commité (gitignored confirmé)
```

## Commande de collecte future

```bash
python3 tools/trading_lab/collect_dukascopy_xauusd_m1.py \
  --start YYYY-MM-DD --end YYYY-MM-DD \
  --out state/trading_lab_v1/inputs/xauusd_m1_broker_<start>_<end>.csv
```

## perf_status

Reste `UNMEASURED`. Seuil : ≥ 20 trades sur ≥ 30 jours broker réels avec timeout < 30%.
Résultat smoke (1W/9L/2T sur 5 jours) non représentatif.

## Remaining gap

- Collecter 30–90 jours pour mesure décisionnelle
- Auditer les sessions `neutral` (direction indéterminée, 4/12 sur cette semaine)
- Vérifier les timeouts (2/12) — candles post-entrée manquantes en fin de plage
