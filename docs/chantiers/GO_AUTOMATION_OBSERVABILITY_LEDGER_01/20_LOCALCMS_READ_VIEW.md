---
doc_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01_CMS
doc_type: cms_read_view
go_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01
status: draft
---

# 20_LOCALCMS_READ_VIEW

The ledger is exposed in LocalCMS via a read-only view.

## View location

`data/runtime_health/ledger/cms_reader.py`

## CMS integration

```python
# scripts/ai/local_cms/pages/ledger/paginated_view.py
# Exposes: /ledger?page=1&per_page=20
# Filters: status, actor_id, surface_id, event_type
# Output: JSON array of events with total count
```

## Cursor-based pagination

```bash
# Usage:
python3 scripts/ai/workers/ledger_replay.py --status PASS
python3 scripts/ai/workers/ledger_replay.py --actor strict_worker
python3 scripts/ai/workers/ledger_replay.py --surface Airtable
```

## Integration example

Used by G11 (LocalCMS cockpit) to render the "observability" panel.
Used by G10 (signal chain) to trace dry_run → write_gated → approval → write chains.
