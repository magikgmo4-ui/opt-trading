---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01
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
  - market_metrics
  - schema
  - validation
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_MARKET_METRICS_V1_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/30_MARKET_METRICS_SCHEMA_TESTS.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/20_FIXTURE_MATRIX.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Matérialiser le contrat `market_metrics.v1` en Python : dataclass validée, sérialisable JSON, testée contre les fixtures du child coverage.

## 2_PARENT_CONTEXT

Child de `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`. S'appuie sur :
- Le contrat défini dans `20_MARKET_METRICS_V1_CONTRACT.md`
- Les fixtures et tests-specs de `GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`

## 3_DELIVERABLES

| Fichier | Role |
|---|---|
| `modules/derivatives_collector/app/market_metrics_v1.py` | `MarketMetricsV1` dataclass + `validate()` + `to_json()` |
| `modules/derivatives_collector/tests/test_market_metrics_v1.py` | 17 test cases : TC-BITGET, TC-BINANCE-DERIV, TC-COINGLASS, invariants |

## 4_INVARIANTS IMPLEMENTES

1. `missing_metrics` → valeur `null`
2. `collectable_metrics` → valeur non-null
3. valeur non-null → dans `collectable_metrics`
4. `status = "partial"` → `missing_metrics` non vide
5. `status = "not_proven_runtime_adapter"` → `collectable_metrics = []` et tous les `metrics.*` null

## 5_TESTS

```bash
python3 -m unittest modules.derivatives_collector.tests.test_market_metrics_v1 -v
```

Résultat attendu : `Ran 17 tests in 0.00Xs — OK`

## 6_NEXT

`GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01` — lire `market_metrics.v1` latest depuis Desk Pro sans écriture DB.
