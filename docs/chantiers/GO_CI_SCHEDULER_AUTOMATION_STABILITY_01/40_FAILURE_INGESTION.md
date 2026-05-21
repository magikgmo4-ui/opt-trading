---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_FAILURE
doc_type: ci_failure_ingestion
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
status: draft
---

# 40_FAILURE_INGESTION.md

## Collecte des échecs

| Source | Type | Collecte | Destination |
|---|---|---|---|
| CI workflows | Workflow failure | GitHub API → webhook | `data/runtime_health/failures/ci/` |
| systemd services | Service failure | journalctl | `data/runtime_health/failures/systemd/` |
| Ledger events | BLOCKED/FAIL events | ledger_replay | `data/runtime_health/failures/ledger/` |
| Workers | Runtime exception | stderr → log | `data/runtime_health/failures/workers/` |

## Classification

```yaml
failure_classes:
  transient:
    - network_timeout
    - rate_limit
    - service_unavailable
  permanent:
    - auth_failed
    - invalid_input
    - permission_denied
  critical:
    - secret_leak
    - data_corruption
    - security_breach
```

## Alerting

| Classe | Canal | Délai |
|---|---|---|
| transient | Ledger log only | N/A |
| permanent | Telegram + Ledger | 5 min |
| critical | Telegram + Email + Ledger | Immédiat |
