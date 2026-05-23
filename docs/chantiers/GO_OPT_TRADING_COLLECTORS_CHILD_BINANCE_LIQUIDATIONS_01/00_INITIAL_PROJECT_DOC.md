---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01
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
  - binance
  - liquidations
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/10_PROVIDER_COVERAGE_REPORT.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Combler le gap `liquidations_long` et `liquidations_short` sur le Binance derivatives adapter. Binance passe de 4 métriques prouvées à 6.

## 2_CONTEXT

Le child coverage report (#696) avait classifié Binance derivatives comme :
- PROVEN : `open_interest`, `funding_rate`, `volume_futures`, `long_short_ratio`
- MISSING : `liquidations_long`, `liquidations_short`

Ce patch utilise l'endpoint public `/fapi/v1/forceOrders` (pas de clé API requise).

## 3_IMPLEMENTATION

Endpoint : `GET /fapi/v1/forceOrders?symbol=BTCUSDT&limit=100` (public)

Logique d'agrégation :
- `side = "SELL"` → long position liquidée → `liquidations_long`
- `side = "BUY"` → short position liquidée → `liquidations_short`
- Valeur : `sum(executedQty * averagePrice)` en USD
- Retourne `0.0` si l'endpoint répond avec une liste vide (aucune liquidation récente)
- Retourne `None` si l'endpoint est indisponible (dégradation silencieuse)

## 4_DELIVERABLES

| Fichier | Rôle |
|---|---|
| `modules/derivatives_collector/app/binance_adapter.py` | +20 lignes — fetch forceOrders + agrégation |
| `modules/derivatives_collector/tests/test_binance_liquidations_patch.py` | 9 tests |

## 5_COVERAGE UPDATE

| Provider | Avant | Après |
|---|---|---|
| binance_derivatives — open_interest | PROVEN | PROVEN |
| binance_derivatives — funding_rate | PROVEN | PROVEN |
| binance_derivatives — volume_futures | PROVEN | PROVEN |
| binance_derivatives — long_short_ratio | PROVEN | PROVEN |
| binance_derivatives — liquidations_long | MISSING | **PROVEN** |
| binance_derivatives — liquidations_short | MISSING | **PROVEN** |

Binance derivatives status : PARTIAL (4 métriques) → **FULL** (6/6 métriques prouvées).

## 6_TESTS

```bash
python3 -m unittest modules.derivatives_collector.tests.test_binance_liquidations_patch -v
```

Résultat attendu : `Ran 9 tests — OK`

## 7_NOTE

`liquidations_long = 0.0` est une valeur valide (aucune liquidation dans la fenêtre) et distincte de `None` (endpoint indisponible). Conforme aux invariants `market_metrics.v1`.

## 8_NEXT

Seul gap restant : Coinglass adapter (PATCH-B2) — nécessite clé API. Optionnel selon disponibilité.
