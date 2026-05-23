---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: closed
lifecycle_stage: accepted
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict

**ACCEPTED** — Tous les child GOs sans prérequis de clé API externe sont livrés et mergés.

---

## Child GOs livrés

| Child GO | PR | Status | Livraison |
|---|---|---|---|
| CHILD_PROVIDER_COVERAGE_REPORT_01 | #696 | MERGED | Rapport coverage + fixtures + schema tests + next patches |
| CHILD_MARKET_METRICS_CONTRACT_01 | #698 | MERGED | `MarketMetricsV1` dataclass + validate() + 17 tests |
| CHILD_DESKPRO_READONLY_CONSUMER_01 | #699 | MERGED | `market_metrics_reader.py` + intégration aggregator + 22 tests |
| CHILD_BITGET_LSR_PATCH_01 | #703 | MERGED | Bitget `long_short_ratio` via endpoint v2 + 9 tests |
| CHILD_BINANCE_LIQUIDATIONS_01 | #704 | MERGED | Binance `liquidations_long/short` via forceOrders + 9 tests |
| CHILD_BITGET_LIQUIDATIONS_01 | #706 | MERGED | Bitget `liquidations_long/short` via liquidation-order + 10 tests |

---

## Coverage finale des providers

| Provider | open_interest | funding_rate | volume_futures | long_short_ratio | liquidations_long | liquidations_short | Status |
|---|---|---|---|---|---|---|---|
| binance_derivatives | PROVEN | PROVEN | PROVEN | PROVEN | PROVEN | PROVEN | **FULL** |
| bitget | PROVEN | PROVEN | PROVEN | PROVEN | PROVEN | PROVEN | **FULL** |
| coinglass | — | — | — | — | — | — | NOT_PROVEN_RUNTIME_ADAPTER |
| coingecko | spot only | — | — | — | — | — | SPOT_ONLY |
| binance_spot | spot only | — | — | — | — | — | SPOT_ONLY |

---

## Décision Coinglass

Coinglass est un service payant. Aucun adapter API runtime ne sera implémenté dans ce chantier. Les données de liquidations Coinglass seront produites par un **bot vision headless** externe. Le statut `not_proven_runtime_adapter` est maintenu de façon permanente pour Coinglass dans le contrat `market_metrics.v1`.

---

## Chaîne livrée

```text
API providers (Binance, Bitget)
  -> derivatives_collector adapters (FULL coverage 6/6)
  -> DerivativesRow → market_metrics.v1 (MarketMetricsV1 dataclass + validate)
  -> data/deskpro/inputs/market_metrics/latest.json
  -> Desk Pro read-only consumer (market_metrics_reader → Snapshot augmenté)
```

---

## Tests livrés

| Suite | Fichier | Tests | Status |
|---|---|---|---|
| market_metrics_v1 schema | `test_market_metrics_v1.py` | 17 | OK |
| Desk Pro reader | `test_desk_pro_market_metrics_reader.py` | 22 | OK |
| Bitget LSR | `test_bitget_lsr_patch.py` | 9 | OK |
| Binance liquidations | `test_binance_liquidations_patch.py` | 9 | OK |
| Bitget liquidations | `test_bitget_liquidations_patch.py` | 10 | OK |
| **Total** | | **67** | **OK** |

---

## Gaps résiduels — hors scope accepté

| Gap | Raison | Action future |
|---|---|---|
| Coinglass liquidations API | Service payant | Bot vision headless |
| Bitget liquidations runtime smoke | Nécessite clé API prod | Smoke en staging |
| cache `by_symbol` | Non prioritaire | Child futur si besoin |
| ingestion DB `market_metrics` | Non prioritaire | Child futur si besoin |
