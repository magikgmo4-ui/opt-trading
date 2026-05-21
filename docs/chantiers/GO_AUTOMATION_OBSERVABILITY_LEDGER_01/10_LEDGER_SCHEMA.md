---
doc_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01_SCHEMA
doc_type: ledger_schema
go_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01
status: draft
---

# 10_LEDGER_SCHEMA

## Event schema

```json
{
  "event_id": "uuid",
  "event_type": "read | patch_draft | write_gated | approval | rejection | escalation | system",
  "actor_id": "humain | OpenClaw | strict_worker | team_ai_manager | specialist_worker | app_bridge | system",
  "surface_id": "repo | tmux | Telegram | TradingView | Airtable | ...",
  "action": "READ_INVENTORY | PATCH_DRAFT | WRITE_GATED | APPROVE | REJECT | ...",
  "timestamp": "ISO8601",
  "status": "PASS | FAIL | BLOCKED | WARN",
  "payload": {},
  "trace_id": "uuid (groupe d'events liés)",
  "handoff_id": "uuid | null"
}
```

## Storage

- Format : JSONL (1 event par ligne)
- Chemin : `data/runtime_health/ledger/events.jsonl`
- Rotation : 100 MB par fichier, nouveau fichier créé automatiquement
- Archive : `data/runtime_health/ledger/archive/events_<YYYY-MM-DD>.jsonl`

## Writer

Implémenté dans `scripts/ai/workers/ledger_writer.py` — usage :

```bash
python3 scripts/ai/workers/ledger_writer.py \
    --event-type read \
    --actor-id strict_worker \
    --surface-id repo \
    --action READ_INVENTORY \
    --status PASS \
    --payload '{"files_read": 5}'
```
