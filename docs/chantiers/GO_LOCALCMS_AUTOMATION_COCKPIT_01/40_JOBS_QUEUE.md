---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_JOBS
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 40_JOBS_QUEUE.md

## Page: Jobs Queue

URL: `/cockpit/automation/jobs`

### File d'attente

```text
┌─────┬────────────────────────┬──────────┬──────────┬──────────┐
│ ID  │ Job                    │ Statut   │ Début    │ Fin      │
├─────┼────────────────────────┼──────────┼──────────┼──────────┤
│ 001 │ smoke_readonly         │ done     │ 02:30:00 │ 02:30:05 │
│ 002 │ patch_draft_config     │ running  │ 02:45:00 │ —        │
│ 003 │ bridge_sync_airtable   │ queued   │ —        │ —        │
│ 004 │ bridge_sync_telegram   │ failed   │ 02:20:00 │ 02:20:03 │
└─────┴────────────────────────┴──────────┴──────────┴──────────┘
```

### Filtres

- Statut : all | queued | running | done | failed
- Worker : all | strict_worker | specialist | bridge
- Période : 1h | 6h | 24h | 7d

### Dead-letter queue

```text
Failed jobs (dead-letter): 1
  - bridge_sync_telegram: network_timeout (retry 3/3)
```
