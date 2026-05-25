---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01_TARGET
doc_type: target
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 20_MARKET_METRICS_READONLY_TARGET

## Décision figée

```text
market_metrics.v1 = input optionnel du dry-run Desk Pro.
Absence = WARN non bloquant.
Présence = summary.market_metrics_present = True.
Source canonique = data/data_center/views/market_metrics/latest.json
```

## Contrat `market_metrics.v1` côté Desk Pro

| Champ | Source | Chemin DC |
|---|---|---|
| `open_interest` | derivatives_collector__bitget / binance | `data/data_center/views/market_metrics/latest.json` |
| `funding_rate` | idem | idem |
| `volume_futures` | idem | idem |
| `long_short_ratio` | idem | idem |
| `liquidations_long` | idem | idem |
| `liquidations_short` | idem | idem |

Reader : `read_market_metrics()` → `List[Metric]`

## Comportement dry-run avec market_metrics

| Scénario | `summary.market_metrics_present` | status impact |
|---|---|---|
| `market_metrics=None` | `False` | WARN ajouté (non bloquant) |
| `market_metrics=[]` | `False` | WARN ajouté (non bloquant) |
| `market_metrics=[Metric(...), ...]` | `True` | aucun warning ajouté |

## Warning message canonique

```text
"market_metrics missing: market-context-free synthesis"
```

Identique au pattern `visual_context missing` et `desk_snapshot missing`.
