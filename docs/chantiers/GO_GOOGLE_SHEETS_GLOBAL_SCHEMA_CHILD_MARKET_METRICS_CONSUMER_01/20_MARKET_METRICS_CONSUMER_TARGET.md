---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_CONSUMER_TARGET
doc_type: target_design
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 20_MARKET_METRICS_CONSUMER_TARGET — Design consumer V1

## Module livré

### `modules/google_sheets_global_schema/market_metrics_consumer.py`

```python
@dataclass
class ConsumerResult:
    ok: bool
    rows_written: int
    rows_attempted: int
    source_path: str
    mode: str            # "fake" | "dry_run" | "controlled_write" | "no_source"
    error: str | None

def _load_mm_v1(source_path: Path) -> dict | None:
    """Load + validate input_class. Returns None on any failure."""

def map_mm_v1_to_rows(payload: dict, source_ref: str) -> list[dict]:
    """One row per collectable + non-None metric."""

def write_market_metrics_to_sheets(
    writer: SheetsWriter,
    source_path: Path | None = None,
    *,
    root: Path | None = None,
) -> ConsumerResult:
    """Source absent -> ok=True, mode="no_source" (silent-empty fallback)."""
```

## Logique de mapping

```
market_metrics.v1
├── symbol          -> row["symbol"]
├── metrics_ts      -> row["as_of"]
└── metrics.<name>  -> row["metric_name"] = name, row["value"] = value
    (filtre: name in collectable_metrics AND value is not None)

source_ref = chemin relatif Data Center (ex: "data/data_center/views/market_metrics/latest.json")
```

Résultat : une row par (symbol, metric_name) avec `as_of` = `metrics_ts`.

## Comportement source absente

```
source_path absent ou wrong input_class ou JSON invalide
  -> ConsumerResult(ok=True, rows_written=0, mode="no_source")
  # pas de crash, pas d'erreur remontée
  # cohérent avec desk_pro fallback="silent_empty"
```

## Flux complet

```
write_market_metrics_to_sheets(writer, source_path=path)
├── _load_mm_v1(path)      -> None si absent/invalide -> ConsumerResult(no_source)
├── map_mm_v1_to_rows()    -> [] si metrics vides -> ConsumerResult(ok=True, rows_written=0)
├── writer.write_rows("market_metrics", rows)  # R1-R10 appliqués
└── -> ConsumerResult depuis WriteResult
```
