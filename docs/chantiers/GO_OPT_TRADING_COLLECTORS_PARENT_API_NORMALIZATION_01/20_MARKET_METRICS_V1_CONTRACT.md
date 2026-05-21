---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_MARKET_METRICS_V1_CONTRACT
doc_type: data_contract
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 20_MARKET_METRICS_V1_CONTRACT

## Objectif

Definir le contrat `market_metrics.v1` comme sortie normalisee des collectors API et entree read-only de Desk Pro.

## Role

`market_metrics.v1` est une couche de contexte marche. Elle ne remplace pas :

- OHLCV canonique
- screenshots / visual_context
- signal_event
- decisions Desk Pro
- journal/perf engine

Elle enrichit Desk Pro avec les metriques collectables via API.

## Payload minimal

```json
{
  "contract_version": "v1",
  "input_class": "market_metrics.v1",
  "module_id": "derivatives_collector",
  "provider_id": "bitget",
  "symbol": "BTCUSDT",
  "metrics_ts": "2026-05-20T00:00:00Z",
  "freshness_state": "fresh",
  "provider_coverage": {
    "status": "partial",
    "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
    "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"]
  },
  "metrics": {
    "open_interest": 123.0,
    "funding_rate": 0.0001,
    "volume_futures": 123456.0,
    "long_short_ratio": null,
    "liquidations_long": null,
    "liquidations_short": null
  },
  "refs": {
    "primary_output": "data/derivatives/derivatives_YYYYMMDD_HHMMSS.json",
    "meta_output": "data/derivatives/derivatives_YYYYMMDD_HHMMSS.meta.json",
    "latest": "data/derivatives/latest.json",
    "status": "data/derivatives/status.json"
  },
  "warnings": ["provider missing metrics are explicit and not synthesized"]
}
```

## Champs requis

| Champ | Type | Requis | Description |
|---|---|---|---|
| `contract_version` | string | oui | `v1` |
| `input_class` | string | oui | `market_metrics.v1` |
| `module_id` | string | oui | collector source |
| `provider_id` | string/null | oui | provider source ou null si multi-source |
| `symbol` | string | oui | symbole normalise |
| `metrics_ts` | string | oui | timestamp UTC Z |
| `freshness_state` | string | oui | `fresh`, `stale`, `unknown` |
| `provider_coverage` | object | oui | couverture collectable/missing |
| `metrics` | object | oui | valeurs normalisees, null si absent |
| `refs` | object | oui | pointeurs fichiers |
| `warnings` | list | non | warnings de couverture/jointure |

## Invariants

- Une metrique non collectee reste `null`.
- Une metrique non collectee doit etre declaree dans `missing_metrics`.
- Le contrat ne simule jamais `liquidations`, `long_short_ratio` ou funding.
- Le contrat reste compatible Desk Pro read-only.
- Le contrat peut etre consomme par Sheets/Telegram/Perf plus tard, mais ne les ecrit pas directement.

## Mapping derivatives

| DerivativesRow | market_metrics.v1 |
|---|---|
| `symbol` | `symbol` |
| `exchange` | `provider_id` |
| `timestamp` | `metrics_ts` |
| `open_interest` | `metrics.open_interest` |
| `funding_rate` | `metrics.funding_rate` |
| `long_short_ratio` | `metrics.long_short_ratio` |
| `liquidations_long` | `metrics.liquidations_long` |
| `liquidations_short` | `metrics.liquidations_short` |
| `volume_futures` | `metrics.volume_futures` |
| `error` | `warnings` ou coverage status |

## Desk Pro read-only contract

Desk Pro doit lire :

```text
data/deskpro/inputs/market_metrics/latest.json
```

et optionnellement :

```text
data/deskpro/inputs/market_metrics/by_symbol/<SYMBOL>.json
```

Desk Pro ne doit pas modifier ces fichiers.

## Consommateurs futurs

- Desk Pro : decision context
- Google Sheets global : reporting et journalisation
- Telegram outbound : resume signal/context
- Perf Engine : replay et stats enrichies
- Strategy Registry / Trading Lab : evaluation par regime et contexte

## Statut

Contrat cible documente. Implementation hors de ce fichier.
