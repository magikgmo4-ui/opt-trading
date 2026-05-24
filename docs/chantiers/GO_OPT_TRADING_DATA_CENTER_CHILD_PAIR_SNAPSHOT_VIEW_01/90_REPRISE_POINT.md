---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01`
- Tests : **150 PASS** (135 existants + 15 nouveaux)
- Verdict : ACCEPTED

## Fichiers créés / modifiés

```text
modules/data_center/registry/consumers.json                 ← desk_pro__spot_snapshot read_path corrigé
modules/data_center/layout.py                               ← views/pair_market_snapshot/by_symbol/ ajouté
modules/data_center/pair_snapshot_view_writer.py            ← NOUVEAU — write_pair_market_snapshot_view()
modules/data_center/tests/test_contract_tests.py            ← +6 tests pair_market_snapshot invariants
modules/data_center/tests/test_layout.py                    ← +2 tests pair_snapshot dirs
modules/data_center/tests/test_pair_snapshot_view_writer.py ← NOUVEAU — 10 tests writer
docs/chantiers/...                                          ← 5 fichiers docs
```

## État figé — consumers `pair_market_snapshot.v1`

```text
desk_pro__spot_snapshot → not_started, read_path=views/pair_market_snapshot/latest.json, aucun reader réel
```

## Règle étendue

La règle "aucun consumer ne lit un producer_id path" couvre désormais les deux contrats actifs :

| contract_class | Producer paths | Vue consumer | Statut |
|---|---|---|---|
| `market_metrics.v1` | `data/data_center/derivatives/<producer_id>/` | `views/market_metrics/` | VERROUILLÉ (#761) |
| `pair_market_snapshot.v1` | `data/data_center/spot/<producer_id>/` | `views/pair_market_snapshot/` | VERROUILLÉ (ce GO) |

## Etat global consumer coverage après ce GO

| Consumer | contract_class | access_pattern | Status |
|---|---|---|---|
| `desk_pro__market_metrics` | `market_metrics.v1` | `latest_only` | MIGRÉ — reader réel |
| `desk_pro__spot_snapshot` | `pair_market_snapshot.v1` | `latest_only` | not_started (path corrigé ✓) |
| `telegram_screener__signal_context` | `market_metrics.v1` | `latest_only` | not_started |
| `google_sheets__market_reporting` | `market_metrics.v1` | `latest_only` | not_started |
| `strategy_framework__market_context` | `market_metrics.v1` | `by_symbol` | not_started |
| `perf_engine__replay_context` | `market_metrics.v1` | `full_history` | not_started |
| `localcms__data_center_health` | null | `status_only` | not_started |

## Progression vers CLOSE_GATE_MASTER_TARGET

| Critère | Requis | Atteint |
|---|---|---|
| ≥2 producers avec contrats formalisés/testés | 2 | **2** (bitget, binance) ← `market_metrics.v1` |
| ≥2 consumers avec lecture prouvée depuis data/data_center/ | 2 | **1** (Desk Pro market_metrics) |
| Tests contractuels smoke | req. | **150/150 PASS** |

Manque toujours : 1 consumer runtime réel de plus pour atteindre le close gate du parent.

## Prochaine étape

Pour satisfaire le `CLOSE_GATE_MASTER_TARGET` (≥2 consumers avec lecture prouvée) :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01
```

ou implémenter `desk_pro__spot_snapshot` comme reader réel (requiert câblage du collector vers DC view).
