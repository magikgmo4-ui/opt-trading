---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_WORKERS
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 30_WORKERS_STATE.md

## Page: Workers State

URL: `/cockpit/automation/workers`

### Tableau

| Worker | Role | Statut | Dernière tâche | Dernier heartbeat |
|---|---|---|---|---|
| strict_worker_01 | Lecture seule | active | READ_INVENTORY (PASS) | 30s ago |
| specialist_worker | Spécialiste | active | PATCH_DRAFT (PASS) | 45s ago |
| team_ai_manager | Manager AI | idle | — | 2 min ago |
| app_bridge_airtable | Bridge | active | WRITE_GATED (BLOCKED) | 10s ago |

### Actions

- [VIEW] Voir les logs du worker
- [RESTART] Redémarrer le worker (bouton safe — confirmation requise)
- [STOP] Arrêter le worker (confirmation + raison requise)
