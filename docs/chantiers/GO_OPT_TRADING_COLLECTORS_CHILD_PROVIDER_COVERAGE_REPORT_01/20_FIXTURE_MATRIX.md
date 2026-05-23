---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_FIXTURE_MATRIX
doc_type: fixture_matrix
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

# 20_FIXTURE_MATRIX

## Objet

Matrice des fixtures representant les reponses API attendues par provider et endpoint. Ces fixtures documentent ce que les adapters doivent recevoir et produire — elles ne sont pas executees dans ce child.

Les fixtures sont exprimees en JSON inline. Elles servent de base de test pour le child `30_MARKET_METRICS_SCHEMA_TESTS.md`.

---

## Bitget — derivatives_collector

### Endpoint : open interest

Reponse API raw attendue (simplifie) :

```json
{
  "code": "00000",
  "data": {
    "symbol": "BTCUSDT_UMCBL",
    "amount": "18234.56",
    "timestamp": "1716163200000"
  }
}
```

Champ extrait : `open_interest = float(data["amount"])` = `18234.56`

### Endpoint : funding rate

```json
{
  "code": "00000",
  "data": {
    "symbol": "BTCUSDT_UMCBL",
    "fundingRate": "0.0001",
    "settleTime": "1716163200000"
  }
}
```

Champ extrait : `funding_rate = float(data["fundingRate"])` = `0.0001`

### Endpoint : ticker / volume

```json
{
  "code": "00000",
  "data": {
    "symbol": "BTCUSDT_UMCBL",
    "baseVolume": "1234.5",
    "quoteVolume": "67890123.45",
    "last": "55000.0"
  }
}
```

Champ extrait : `volume_futures = float(data["quoteVolume"])` = `67890123.45`

### Fixture DerivativesRow — Bitget

```json
{
  "symbol": "BTCUSDT",
  "exchange": "bitget",
  "timestamp": "2026-05-23T00:00:00Z",
  "open_interest": 18234.56,
  "funding_rate": 0.0001,
  "volume_futures": 67890123.45,
  "long_short_ratio": null,
  "liquidations_long": null,
  "liquidations_short": null,
  "error": null
}
```

### Fixture market_metrics.v1 — Bitget

```json
{
  "contract_version": "v1",
  "input_class": "market_metrics.v1",
  "module_id": "derivatives_collector",
  "provider_id": "bitget",
  "symbol": "BTCUSDT",
  "metrics_ts": "2026-05-23T00:00:00Z",
  "freshness_state": "fresh",
  "provider_coverage": {
    "status": "partial",
    "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
    "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"]
  },
  "metrics": {
    "open_interest": 18234.56,
    "funding_rate": 0.0001,
    "volume_futures": 67890123.45,
    "long_short_ratio": null,
    "liquidations_long": null,
    "liquidations_short": null
  },
  "refs": {
    "primary_output": "data/derivatives/derivatives_20260523_000000.json",
    "meta_output": "data/derivatives/derivatives_20260523_000000.meta.json",
    "latest": "data/derivatives/latest.json",
    "status": "data/derivatives/status.json"
  },
  "warnings": ["provider missing metrics are explicit and not synthesized"]
}
```

---

## Binance Derivatives — derivatives_collector

### Endpoint : open interest

```json
{
  "symbol": "BTCUSDT",
  "openInterest": "72145.890",
  "time": 1716163200000
}
```

Champ extrait : `open_interest = float(openInterest)` = `72145.89`

### Endpoint : funding rate

```json
[
  {
    "symbol": "BTCUSDT",
    "fundingRate": "0.00012500",
    "fundingTime": 1716163200000
  }
]
```

Champ extrait : `funding_rate = float(fundingRate)` = `0.000125`

### Endpoint : ticker 24h

```json
{
  "symbol": "BTCUSDT",
  "volume": "89012.345",
  "quoteVolume": "4890123456.78"
}
```

Champ extrait : `volume_futures = float(quoteVolume)` = `4890123456.78`

### Endpoint : long/short ratio

```json
{
  "symbol": "BTCUSDT",
  "longShortRatio": "1.8234",
  "timestamp": 1716163200000
}
```

Champ extrait : `long_short_ratio = float(longShortRatio)` = `1.8234`

### Fixture DerivativesRow — Binance Derivatives

```json
{
  "symbol": "BTCUSDT",
  "exchange": "binance_derivatives",
  "timestamp": "2026-05-23T00:00:00Z",
  "open_interest": 72145.89,
  "funding_rate": 0.000125,
  "volume_futures": 4890123456.78,
  "long_short_ratio": 1.8234,
  "liquidations_long": null,
  "liquidations_short": null,
  "error": null
}
```

### Fixture market_metrics.v1 — Binance Derivatives

```json
{
  "contract_version": "v1",
  "input_class": "market_metrics.v1",
  "module_id": "derivatives_collector",
  "provider_id": "binance_derivatives",
  "symbol": "BTCUSDT",
  "metrics_ts": "2026-05-23T00:00:00Z",
  "freshness_state": "fresh",
  "provider_coverage": {
    "status": "partial",
    "collectable_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio"],
    "missing_metrics": ["liquidations_long", "liquidations_short"]
  },
  "metrics": {
    "open_interest": 72145.89,
    "funding_rate": 0.000125,
    "volume_futures": 4890123456.78,
    "long_short_ratio": 1.8234,
    "liquidations_long": null,
    "liquidations_short": null
  },
  "refs": {
    "primary_output": "data/derivatives/derivatives_20260523_000000.json",
    "meta_output": "data/derivatives/derivatives_20260523_000000.meta.json",
    "latest": "data/derivatives/latest.json",
    "status": "data/derivatives/status.json"
  },
  "warnings": ["liquidations not available from binance_derivatives adapter"]
}
```

---

## Coinglass — NOT_PROVEN_RUNTIME_ADAPTER

Aucune fixture possible. Aucun adapter reel present dans le repo.

Fixture hypothetique (pour test futur seulement) :

```json
{
  "provider_id": "coinglass",
  "module_id": "derivatives_collector",
  "status": "not_proven_runtime_adapter",
  "collectable_metrics": [],
  "missing_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
  "notes": ["no adapter file found; do not fabricate data"]
}
```

---

## Fixture provider_metric_coverage_latest.json

Structure du rapport de couverture consolide attendu :

```json
{
  "report_version": "v1",
  "generated_at": "2026-05-23T00:00:00Z",
  "go_id": "GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01",
  "providers": [
    {
      "provider_id": "bitget",
      "module_id": "derivatives_collector",
      "symbol": "BTCUSDT",
      "status": "partial",
      "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
      "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"],
      "notes": []
    },
    {
      "provider_id": "binance_derivatives",
      "module_id": "derivatives_collector",
      "symbol": "BTCUSDT",
      "status": "partial",
      "collectable_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio"],
      "missing_metrics": ["liquidations_long", "liquidations_short"],
      "notes": []
    },
    {
      "provider_id": "coinglass",
      "module_id": "derivatives_collector",
      "symbol": "BTCUSDT",
      "status": "not_proven_runtime_adapter",
      "collectable_metrics": [],
      "missing_metrics": ["open_interest", "funding_rate", "volume_futures", "long_short_ratio", "liquidations_long", "liquidations_short"],
      "notes": ["no adapter file found in repo"]
    },
    {
      "provider_id": "coingecko",
      "module_id": "collector_coingecko",
      "symbol": "BTC",
      "status": "spot_only",
      "collectable_metrics": ["market_cap", "price", "volume_24h", "price_change_24h", "circulating_supply"],
      "missing_metrics": [],
      "notes": ["spot metrics only, not derivatives scope"]
    },
    {
      "provider_id": "binance_spot",
      "module_id": "collector_binance_spot",
      "symbol": "BTCUSDT",
      "status": "spot_only",
      "collectable_metrics": ["price", "volume_24h", "price_change_24h"],
      "missing_metrics": [],
      "notes": ["spot metrics only, not derivatives scope"]
    }
  ],
  "summary": {
    "total_providers": 5,
    "derivatives_partial": 2,
    "derivatives_not_proven": 1,
    "spot_only": 2,
    "liquidations_gap": true,
    "coinglass_gap": true
  }
}
```
