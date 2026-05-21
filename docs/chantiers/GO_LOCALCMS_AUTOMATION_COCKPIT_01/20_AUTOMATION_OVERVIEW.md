---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_OVERVIEW
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 20_AUTOMATION_OVERVIEW.md

## Page: Automation Overview

URL: `/cockpit/automation/overview`

### Sections

| Section | Source de données | Refresh |
|---|---|---|
| Global status | Kill switch state (`data/runtime_health/kill_switch.state`) | 5s |
| Dernière exécution | Ledger last event (`ledger_replay.py --replay`) | 10s |
| Alertes actives | Dead-letter count (`data/runtime_health/dead_letter/`) | 30s |
| Workers en ligne | Health status JSON (`health_status.py`) | 30s |

### Layout

```
┌─────────────────────────────────────────┐
│ [GREEN] KILL SWITCH: NORMAL    [ACTIONS] │
├──────────────────┬──────────────────────┤
│ Dernière action  │ Alertes (0)          │
│ READ_INVENTORY   │  - Aucune alerte     │
│ 2 min ago        │                      │
├──────────────────┴──────────────────────┤
│ Workers: 2 actifs, 0 inactifs           │
│ Timers: 2/2 actifs                      │
└─────────────────────────────────────────┘
```

### Données

```json
{
  "kill_switch": "NORMAL",
  "last_event": {"action": "READ_INVENTORY", "status": "PASS", "elapsed_seconds": 120},
  "active_alerts": 0,
  "workers_online": 2,
  "timers_active": 2
}
```
