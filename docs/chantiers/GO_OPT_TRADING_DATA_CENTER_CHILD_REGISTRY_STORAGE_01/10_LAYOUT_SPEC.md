# 10_LAYOUT_SPEC

## Layout

```text
data/data_center/
  <producer_id>/
    raw/
    normalized/
    latest.json
    manifest.json
    status.json
    events.jsonl
    errors.jsonl
    cache/
      by_symbol/<SYMBOL>.json
  _registry/
    producers.json
    consumers.json
    schema_versions.json
```

## Registry format

### producers.json
```json
{
  "producers": [
    {
      "id": "derivatives_collector",
      "schema": "market_metrics.v1",
      "status": "active",
      "last_write": "ISO8601"
    }
  ]
}
```

### consumers.json
```json
{
  "consumers": [
    {
      "id": "desk_pro",
      "reads": ["market_metrics.v1"],
      "status": "active",
      "last_read": "ISO8601"
    }
  ]
}
```

## Module structure

```text
modules/data_center/
  storage/
    __init__.py
    layout_manager.py
    registry_manager.py
    manifest_writer.py
  tests/
    test_layout.py
    test_registry.py
```
