---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_EXISTING_SURFACE_READ
doc_type: existing_surface_read
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ — Surfaces existantes

## Source canonique Data Center

### `data/data_center/views/market_metrics/latest.json`

Format : `market_metrics.v1` — écrit par `write_market_metrics_view()` dans `modules/derivatives_collector/app/market_metrics_writer.py`.

Champs utilisés par le consumer :

| Champ v1 | Mappage Sheets |
|---|---|
| `metrics_ts` | `as_of` |
| `symbol` | `symbol` |
| `metrics.<metric_name>` | `metric_name` + `value` (une row par metric) |
| `provider_coverage.collectable_metrics` | filtre — seules les métriques collectables émises |

### Consumer pattern établi

`modules/desk_pro/service/market_metrics_reader.py` :
- Lit `latest.json` (DC canonical) avec fallback silencieux si absent.
- Filtre par `collectable_metrics`.
- Retourne `[]` sur toute erreur.

Ce GO adopte le même comportement de fallback : source absente = `ok=True, mode="no_source"`.

## Sheets tab `market_metrics` — schema

```python
"market_metrics": {
    "required": ["as_of", "symbol", "metric_name", "value"],
    "enums": {},
    "timestamps": ["as_of"],
    "pk": ["as_of", "symbol", "metric_name"],
    "ref_cols": ["source_ref"],
}
```

`source_ref` = chemin relatif vers la source Data Center (ex : `data/data_center/views/market_metrics/latest.json`).

## SheetsWriter disponible (PR #813)

```python
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient

writer = SheetsWriter(client=FakeSheetsClient())
writer.write_rows("market_metrics", rows)  # -> WriteResult
```

## Registry consumers.json

`modules/data_center/registry/consumers.json` référence `desk_pro__market_metrics` avec `read_path: data/data_center/views/market_metrics/latest.json`. Ce GO suit le même read_path ; le consumer Sheets peut être ajouté au registry dans un GO séparé.
