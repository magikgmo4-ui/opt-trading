---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - collectors
  - desk_pro
  - market_metrics
  - read_only
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_MARKET_METRICS_V1_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Desk Pro consomme `market_metrics.v1` en read-only depuis `data/deskpro/inputs/market_metrics/latest.json` et injecte les métriques futures prouvées dans le Snapshot.

## 2_PARENT_CONTEXT

Child de `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`. S'appuie sur :
- `MarketMetricsV1` dataclass validée (child `GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01`, PR #698)
- Contrat `market_metrics.v1` (parent `20_MARKET_METRICS_V1_CONTRACT.md`)
- Rapport coverage (child `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`, PR #696)

## 3_DELIVERABLES

| Fichier | Rôle |
|---|---|
| `modules/desk_pro/service/market_metrics_reader.py` | `read_market_metrics()` — lit `latest.json`, retourne `List[Metric]` |
| `modules/desk_pro/service/aggregator.py` | `_augment_market_metrics()` intégrée dans `build_snapshot()` |
| `tests/test_desk_pro_market_metrics_reader.py` | 22 tests : absent, malformé, bitget partial, freshness, not_proven, normalize_asset, intégration aggregator |

## 4_INVARIANTS

- Lecture seule : aucun write DB, Sheets, Telegram
- Dégradation silencieuse : fichier absent ou malformé → liste vide, pas d'exception
- Métriques null exclus : seules les métriques dans `collectable_metrics` avec valeur non-null sont injectées
- `not_proven_runtime_adapter` → aucune métrique injectée
- Freshness → quality : fresh=0.95, stale=0.5, unknown=0.3

## 5_INTEGRATION

`build_snapshot()` appelle `_augment_market_metrics(snap)` après construction du snapshot (fixture ou mock). Si des métriques sont chargées : `snap.meta["market_metrics"] = "loaded"`.

Aucun changement de signature — rétrocompatible.

## 6_TESTS

```bash
python3 -m pytest tests/test_desk_pro_market_metrics_reader.py -v
```

Résultat attendu : `22 passed`

```bash
python3 -m pytest tests/test_desk_pro_dry_run.py tests/test_desk_pro_health_classification.py tests/test_desk_pro_combined_input_smoke.py -v
```

Résultat attendu : `38 passed` (aucune régression)

## 7_NEXT

`GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01` (PATCH-B1) — combler le gap `long_short_ratio` sur Bitget.
