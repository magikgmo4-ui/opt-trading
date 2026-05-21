---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_SCHEDULER
doc_type: ci_scheduler
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
status: draft
---

# 20_SCHEDULER_INVENTORY.md

## Workflows CI

| Workflow | Fichier | Déclencheur | Statut |
|---|---|---|---|
| strict-workers-validate | `.github/workflows/strict-workers-validate.yml` | PR sur `go/*` | Active |
| strict-workers-smoke | `.github/workflows/strict-workers-smoke.yml` | Manual dispatch | Active |
| strict-workers-schedule | `.github/workflows/strict-workers-schedule.yml` | Cron `*/30 * * * *` | Active |

## Timers systemd

| Timer | Service | Intervalle | Statut |
|---|---|---|---|
| opt-trading-runtime-health.timer | runtime-health.service | 5 min | Active |
| opt-trading-fleet-orchestrator.timer | fleet-orchestrator.service | 15 min | Active |

## Smoke critique

```yaml
smoke_critical:
  name: "read-only smoke"
  target: scripts/ai/workers/runner_readonly.py
  job_packet: scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
  frequency: "every 30 min (CI) + every 5 min (systemd)"
  criterion: "5 reads, 0 writes"
  output: reports/ai/workers/<job_name>_RUNNER.json
```
