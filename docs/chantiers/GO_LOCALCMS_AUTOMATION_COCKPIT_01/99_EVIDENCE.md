---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_EVIDENCE
doc_type: evidence
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: passed_with_evidence
---

# 99_EVIDENCE

## Preuve concrète de validation

### 1. Automation Overview
- `20_AUTOMATION_OVERVIEW.md` — kill switch status, last action, alerts, workers en ligne
- Sources : kill_switch.state, ledger, dead-letter, health_status.py

### 2. Workers State
- `30_WORKERS_STATE.md` — 4 workers, statut, dernière tâche, boutons VIEW/RESTART/STOP

### 3. Jobs Queue
- `40_JOBS_QUEUE.md` — file d'attente, 4 jobs (done/running/queued/failed), dead-letter queue
- Filtres : statut, worker, période

### 4. Approvals
- `50_APPROVALS.md` — propositions en attente, historique, boutons APPROVE/REJECT/VIEW

### 5. Ledger
- `60_LEDGER.md` — events paginés, filtres (status, actor, surface, période), boutons REPLAY/EXPORT
- Intégration G06 : `data/runtime_health/ledger/events.jsonl` + `ledger_replay.py`

### 6. Signals
- `70_SIGNALS.md` — derniers signaux, stats (confirmés, rejetés, bloqués), boutons VIEW ORDER/REFRESH
- Intégration G10 : `data/signals/journal/` + `signal_stats.py`

### 7. Safe buttons
- `80_SAFE_BUTTONS_AND_KILL_SWITCH.md` — 5 principes (read-only par défaut, confirmation, dual confirm, log, undo)

### 8. Kill switch
- `80_SAFE_BUTTONS_AND_KILL_SWITCH.md` — 3 niveaux, visuel, dual confirm pour FULL_STOP, reset

### 9. Cockpit HTML
- `registry/cockpit/automation/index.html` — static HTML avec navigation, dark theme GitHub, 6 pages intégrées

## Conclusion

Tous les critères de succès sont remplis (6 pages documentées, safe buttons, kill switch). Statut : PASS_WITH_EVIDENCE.
