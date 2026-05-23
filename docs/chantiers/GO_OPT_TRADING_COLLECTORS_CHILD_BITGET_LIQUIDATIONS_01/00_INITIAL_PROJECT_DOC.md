---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01
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
  - liquidations
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Combler `liquidations_long` et `liquidations_short` sur le Bitget adapter. Bitget passe de 4 métriques à 6 — **FULL coverage**.

## 2_IMPLEMENTATION

Endpoint : `GET /api/v2/mix/market/liquidation-order?symbol=BTCUSDT&productType=USDT-FUTURES&pageSize=100`

- `side=sell` (ou `SELL`) → long position liquidée → `liquidations_long`
- `side=buy` (ou `BUY`) → short position liquidée → `liquidations_short`
- Valeur : `sum(fillQty * fillPrice)` — fallback sur `size * price`
- `0.0` si liste vide (aucune liquidation récente)
- `None` si endpoint indisponible

## 3_DELIVERABLES

| Fichier | Rôle |
|---|---|
| `modules/derivatives_collector/app/bitget_adapter.py` | +20 lignes — fetch liquidation-order |
| `modules/derivatives_collector/tests/test_bitget_liquidations_patch.py` | 10 tests |

## 4_COVERAGE UPDATE

Bitget : PARTIAL (4/6) → **FULL (6/6)**

| Métrique | Avant | Après |
|---|---|---|
| open_interest | PROVEN | PROVEN |
| funding_rate | PROVEN | PROVEN |
| volume_futures | PROVEN | PROVEN |
| long_short_ratio | PROVEN | PROVEN |
| liquidations_long | MISSING | **PROVEN** |
| liquidations_short | MISSING | **PROVEN** |

## 5_TESTS

```bash
python3 -m unittest modules.derivatives_collector.tests.test_bitget_liquidations_patch -v
```

Résultat attendu : `Ran 10 tests — OK`

## 6_ETAT FINAL COLLECTORS

Après ce child, tous les providers non-clé sont à couverture FULL :

| Provider | Métriques | Status |
|---|---|---|
| binance_derivatives | 6/6 | FULL |
| bitget | 6/6 | FULL |
| coinglass | 0/6 | NOT_PROVEN (clé API requise) |
| coingecko | spot only | SPOT_ONLY |
| binance_spot | spot only | SPOT_ONLY |
