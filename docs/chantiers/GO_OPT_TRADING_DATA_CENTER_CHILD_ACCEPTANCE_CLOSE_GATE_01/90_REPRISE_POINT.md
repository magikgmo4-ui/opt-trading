---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01`
- Tests : **135/135 PASS** (aucun test nouveau — doc-only GO)
- Verdict : ACCEPTED

## Fichiers créés

```text
docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/20_ACCEPTANCE_REPORT.md
docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/30_REMAINING_GAPS_AND_NEXT_GO.md
docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/90_REPRISE_POINT.md
docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01.md
```

## Bloc fermé

```text
MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01 — ACCEPTED / CLOSED
```

## Bloc ouvert — PF_DATA_CENTER

```text
PF_DATA_CENTER — OPEN
GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 — OPEN
MPP_DATA_CENTER_NORMALIZED_REGISTRY — OPEN
```

## Règle canonique figée

```text
data/data_center/<family>/<producer_id>/   → écriture producteur (source d'audit)
data/data_center/views/<contract_class>/   → lecture consumer (surface neutre)
```

## État consumer coverage — figé

| access_pattern | Consumer | Status |
|---|---|---|
| `latest_only` | `desk_pro__market_metrics` | MIGRÉ — reader réel, verrouillé |
| `latest_only` | `telegram_screener__signal_context` | not_started — read_path correct |
| `latest_only` | `google_sheets__market_reporting` | not_started — read_path correct |
| `by_symbol` | `strategy_framework__market_context` | not_started — read_path correct |
| `full_history` | `perf_engine__replay_context` | not_started — read_path corrigé (#761) |
| `status_only` | `localcms__data_center_health` | not_started — hors market_metrics.v1 |

## Prochaine étape

Choisir un NEXT_GO parmi ceux listés dans `30_REMAINING_GAPS_AND_NEXT_GO.md`.

Recommandation pour satisfaire `CLOSE_GATE_MASTER_TARGET` du parent (≥2 consumers runtime) :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01
```

ou

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01
```
