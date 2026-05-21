---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_LEDGER
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 60_LEDGER.md

## Page: Ledger

URL: `/cockpit/automation/ledger`

### Events (paginés)

| Timestamp | Actor | Action | Surface | Status |
|---|---|---|---|---|
| 02:40:15 | strict_worker | READ_INVENTORY | Telegram | PASS |
| 02:40:15 | specialist_worker | PATCH_DRAFT | repo | PASS |
| 02:40:16 | app_bridge | WRITE_GATED | Airtable | BLOCKED |

### Filtres

- Status : all | PASS | FAIL | BLOCKED | WARN
- Actor : all | strict_worker | specialist | app_bridge | ...
- Surface : all | repo | Telegram | Airtable | ...
- Période : 1h | 6h | 24h | 7d

### Replay

```text
[BUTTON: REPLAY]  →  lit les events dans l'ordre chronologique
[BUTTON: EXPORT]  →  export JSON des events filtrés
```

### Intégration

- Alimenté par le ledger G06 (`data/runtime_health/ledger/events.jsonl`)
- Lecture via `ledger_replay.py` avec les filtres
