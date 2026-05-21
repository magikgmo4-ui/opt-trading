---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_EVIDENCE
doc_type: evidence
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
status: passed_with_evidence
---

# 99_EVIDENCE

## Preuve concrète de validation

### 1. Scheduler inventory
- `20_SCHEDULER_INVENTORY.md` — 3 workflows CI, 2 timers systemd, smoke critique défini

### 2. Retry policy + dead-letter
- `30_RETRY_POLICY.md` — 3 niveaux (transient/service/critical), backoff exponential/linear, dead-letter queue
- Dead-letter : stockage `data/runtime_health/dead_letter/`, rétention 7j, alerte à 3 events/h

### 3. Status JSON
- `scripts/ai/workers/health_status.py` — génère status avec git, kill switch, ledger count, systemd timers
- Validé : output JSON correct avec tous les champs

```bash
$ python3 scripts/ai/workers/health_status.py
{
  "generated_at": "2026-05-21T02:46:10Z",
  "git": {"branch": "go/GO_CI_SCHEDULER_AUTOMATION_STABILITY_01", "commit": "625f5c94"},
  "kill_switch": "NORMAL",
  "ledger_event_count": 0,
  "systemd_timers": {
    "opt-trading-runtime-health.timer": "active",
    "opt-trading-fleet-orchestrator.timer": "inactive"
  },
  "health": {"status": "OK"}
}
```

### 4. Failure ingestion
- `40_FAILURE_INGESTION.md` — 4 sources (CI, systemd, ledger, workers), 3 classes (transient/permanent/critical), alerting canal par classe

### 5. Alerting
- `50_ALERTING.md` — Telegram + Ledger + Health Status, 4 règles (dead-letter, kill switch, failure rate, timer inactive)

### 6. Smoke critique
- Défini dans `20_SCHEDULER_INVENTORY.md`
- Validé dans G02 (PASS_WITH_EVIDENCE) — 5 reads, 0 writes

## Conclusion

Tous les critères de succès sont remplis (scheduler, retry, dead-letter, status JSON, failure ingestion, alerting). Statut : PASS_WITH_EVIDENCE.
