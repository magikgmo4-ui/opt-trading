---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01
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
  - bitget
  - long_short_ratio
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/10_PROVIDER_COVERAGE_REPORT.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Combler le gap `long_short_ratio` sur le Bitget adapter. Bitget passe de 3 métriques prouvées à 4.

## 2_CONTEXT

Le child coverage report (#696) avait classifié Bitget comme :
- PROVEN : `open_interest`, `funding_rate`, `volume_futures`
- MISSING : `long_short_ratio`, `liquidations_long`, `liquidations_short`

Ce patch comble `long_short_ratio` via l'endpoint Bitget v2 existant mais non implémenté.

## 3_DELIVERABLES

| Fichier | Rôle |
|---|---|
| `modules/derivatives_collector/app/bitget_adapter.py` | +12 lignes — fetch LSR endpoint v2 |
| `modules/derivatives_collector/tests/test_bitget_lsr_patch.py` | 9 tests : LSR populated, dégradations, division par zéro, URL params |

## 4_IMPLEMENTATION

Endpoint : `GET /api/v2/mix/market/account-long-short-ratio?symbol=BTCUSDT&productType=USDT-FUTURES&period=1H`

Réponse : `{"data": [{"longRatio": "0.58", "shortRatio": "0.42", ...}]}`

Calcul : `long_short_ratio = round(longRatio / shortRatio, 4)` si `shortRatio > 0`

Dégradations silencieuses : None si endpoint absent, data vide, shortRatio=0, champs non-numériques.

## 5_COVERAGE UPDATE

| Provider | Avant | Après |
|---|---|---|
| bitget — open_interest | PROVEN | PROVEN |
| bitget — funding_rate | PROVEN | PROVEN |
| bitget — volume_futures | PROVEN | PROVEN |
| bitget — long_short_ratio | MISSING | PROVEN |
| bitget — liquidations_long | MISSING | MISSING |
| bitget — liquidations_short | MISSING | MISSING |

Bitget status : PARTIAL (3 métriques) → PARTIAL (4 métriques). Reste PARTIAL car liquidations manquantes.

## 6_TESTS

```bash
python3 -m unittest modules.derivatives_collector.tests.test_bitget_lsr_patch -v
```

Résultat attendu : `Ran 9 tests — OK`

## 7_NOTE PRE-EXISTING

`test_binance_adapter.py::test_fetch_timeout` et `test_fetch_429_rate_limit` échouent sur `sot/mainline` (bug pré-existant : appel `_fetch(retries=N)` non supporté). Non introduit par ce child.

## 8_NEXT

`GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01` (PATCH-B3) — combler le gap liquidations sur Binance derivatives.
