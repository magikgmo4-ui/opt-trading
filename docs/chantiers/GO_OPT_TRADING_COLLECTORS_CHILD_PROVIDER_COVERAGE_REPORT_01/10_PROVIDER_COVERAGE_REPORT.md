---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_PROVIDER_COVERAGE_REPORT
doc_type: coverage_report
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_PROVIDER_COVERAGE_REPORT

## Objet

Rapport de couverture provider/metric pour les collectors API. Chaque provider est evalue sur les metriques declarees dans la dataclass `DerivativesRow` et le contrat `market_metrics.v1`.

Metriques cibles du contrat :

```text
open_interest
funding_rate
long_short_ratio
liquidations_long
liquidations_short
volume_futures
```

---

## Coverage Matrix

| Provider | Module | open_interest | funding_rate | volume_futures | long_short_ratio | liquidations_long | liquidations_short | Status |
|---|---|---|---|---|---|---|---|---|
| bitget | derivatives_collector | PROVEN | PROVEN | PROVEN | MISSING | MISSING | MISSING | PARTIAL |
| binance_derivatives | derivatives_collector | PROVEN | PROVEN | PROVEN | PROVEN | MISSING | MISSING | PARTIAL |
| coinglass | derivatives_collector | — | — | — | — | — | — | NOT_PROVEN_ADAPTER |
| coingecko | collector_coingecko | spot only | spot only | spot only | — | — | — | SPOT_ONLY |
| binance_spot | collector_binance_spot | spot only | spot only | spot only | — | — | — | SPOT_ONLY |

Legende :
- `PROVEN` : observable dans l'adapter Python lu dans le repo
- `MISSING` : champ declare dans la dataclass, non renseigne par le provider
- `NOT_PROVEN_ADAPTER` : aucun adapter runtime reel trouve dans le repo
- `SPOT_ONLY` : hors scope derivatives, couverture spot distincte

---

## Details par provider

### bitget — derivatives_collector/app/bitget_adapter.py

**Status : PARTIAL**

Metriques prouvees :
- `open_interest` — lu depuis l'endpoint Bitget futures/contract/openInterest
- `funding_rate` — lu depuis l'endpoint fundingRate
- `volume_futures` — lu depuis ticker / volume_24h

Metriques manquantes :
- `long_short_ratio` — non prouve dans l'adapter lu ; endpoint Bitget existe mais non implemente
- `liquidations_long` — non prouve ; Bitget publie des donnees de liquidation mais l'adapter ne les lit pas
- `liquidations_short` — meme raison

Notes :
- Gestion d'erreur provider-specific minimaliste
- Le champ `error` est propagé vers `DerivativesRow.error`
- Coverage report attendu en `provider_coverage.status = "partial"`

```json
{
  "provider_id": "bitget",
  "module_id": "derivatives_collector",
  "symbol": "BTCUSDT",
  "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
  "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"],
  "runtime_status": "partial",
  "adapter_file": "modules/derivatives_collector/app/bitget_adapter.py",
  "notes": ["missing metrics remain null, not synthesized"]
}
```

---

### binance_derivatives — derivatives_collector

**Status : PARTIAL**

Metriques prouvees :
- `open_interest` — endpoint /fapi/v1/openInterest
- `funding_rate` — endpoint /fapi/v1/fundingRate
- `volume_futures` — endpoint /fapi/v1/ticker/24hr quoteVolume
- `long_short_ratio` — endpoint /futures/data/globalLongShortAccountRatio observe

Metriques manquantes :
- `liquidations_long` — non prouve dans l'adapter ; endpoint /fapi/v1/forceOrders possible mais non implemente
- `liquidations_short` — meme raison

Notes :
- Couverture superieure a Bitget sur long_short_ratio
- Liquidations restent un gap pour tous les providers derivatives actuels

```json
{
  "provider_id": "binance_derivatives",
  "module_id": "derivatives_collector",
  "symbol": "BTCUSDT",
  "collectable_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio"],
  "missing_metrics": ["liquidations_long", "liquidations_short"],
  "runtime_status": "partial",
  "notes": ["long_short_ratio proven for binance_derivatives, not for bitget"]
}
```

---

### coinglass — derivatives_collector

**Status : NOT_PROVEN_RUNTIME_ADAPTER**

Aucun adapter Coinglass reel trouve dans le repo au moment de ce rapport. La dataclass peut referencer Coinglass comme source future, mais aucun code d'appel API Coinglass n'est prouve present.

Metriques potentielles si adapter implemente :
- `liquidations_long` — Coinglass est le provider canonique pour les liquidations
- `liquidations_short` — idem
- `long_short_ratio` — disponible via Coinglass

Critere de passage a PROVEN : presence d'un adapter Python avec endpoint Coinglass reel, teste smoke.

```json
{
  "provider_id": "coinglass",
  "module_id": "derivatives_collector",
  "collectable_metrics": [],
  "missing_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
  "runtime_status": "not_proven_runtime_adapter",
  "notes": ["no coinglass adapter found in repo; do not assume availability"]
}
```

---

### coingecko — collector_coingecko

**Status : SPOT_ONLY**

Hors scope derivatives. Fournit un snapshot marche spot normalise :
- market_cap, price, volume_24h, price_change_24h, circulating_supply
- raw + normalized + lifecycle family prouves

Ne contribue pas aux metriques `market_metrics.v1` derivatives.

---

### binance_spot — collector_binance_spot

**Status : SPOT_ONLY**

Hors scope derivatives. Fournit exchange info + ticker 24h spot :
- raw + normalized + lifecycle family prouves

Ne contribue pas aux metriques `market_metrics.v1` derivatives.

---

## Verdict global

| Critere | Etat |
|---|---|
| Au moins un provider derivatives partial-proven | OUI (bitget, binance_derivatives) |
| Liquidations prouvees sur un provider | NON |
| Coinglass adapter reel present | NON |
| Metriques inventees ou synthetisees | NON — interdit |
| market_metrics.v1 materialise runtime | NON — phase doc uniquement |

**Prochain gate** : voir `40_NEXT_PATCHES.md`.
