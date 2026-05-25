---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
status: open
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01`
- Tests : **180 PASS** (162 existants + 18 nouveaux)
- Runtime modifié : **OUI** — `market_metrics_writer.py`, `localcms_health_reader.py`
- Verdict : ACCEPTED

## Fichiers créés / modifiés

```text
modules/data_center/runtime_registry.py                                      ← NOUVEAU
modules/data_center/tests/test_runtime_registry.py                           ← NOUVEAU — 11 tests
modules/derivatives_collector/app/market_metrics_writer.py                   ← update_registry param
modules/derivatives_collector/tests/test_market_metrics_writer.py            ← +6 tests
modules/data_center/localcms_health_reader.py                                ← producer_runtime
modules/data_center/tests/test_localcms_health_reader.py                     ← +1 test
modules/data_center/scripts/sanity_check.sh                                  ← producers with last_write
docs/chantiers/...                                                            ← 5 fichiers docs
```

## État figé — runtime registry après ce GO

```text
data/data_center/_registry/producers.json (runtime, gitignored)
  = créé lors du premier write producer réel
  = producers: {} en dev/CI (aucun run prod)
  = producers: {bitget: {...last_write...}, binance: {...}} après runs prod
```

## Gaps restants après ce GO

| Gap | Description |
|---|---|
| GAP-P01 | bitget `last_write: null` en prod — run réel non exécuté |
| GAP-P02 | binance `last_write: null` en prod — idem |
| GAP-P03 | collector_binance_spot — câblage vers DC producer path non fait |

## Prochaine étape

```text
Axe A (PF_DATA_CENTER) :
  GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
  → câbler collector_binance_spot vers DC + runtime registry pair_market_snapshot

Axe B (PF_DESK_PRO) :
  GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
  → intégrer market_metrics dans Desk Pro dry_run/read-only
```
