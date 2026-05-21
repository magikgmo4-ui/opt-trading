---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_RETRY
doc_type: ci_retry_policy
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
status: draft
---

# 30_RETRY_POLICY.md

## Politique de retry

| Niveau | Max tentatives | Backoff | Fenêtre | Dead-letter |
|---|---|---|---|---|
| L1 — Transient | 3 | Exponential (1s, 2s, 4s) | 30s | Non (retry suffit) |
| L2 — Service | 3 | Linear (30s, 60s, 90s) | 5 min | Oui → dead-letter queue |
| L3 — Critical | 1 | None (pas de retry) | Immédiat | Oui → alerte humaine |

## Dead-letter queue

```yaml
dead_letter:
  storage: "data/runtime_health/dead_letter/"
  format: "jsonl"
  retention: 7 days
  alert_threshold: 3 events in 1 hour
  alert_channel: "telegram"
```

## Procédure

1. Un job échoue → statut FAIL dans le ledger (G06)
2. Si retry disponible → nouvelle tentative avec backoff
3. Si max tentatives atteint → écrit dans dead-letter queue
4. Si dead-letter threshold dépassé → alerte Telegram
5. Analyse hebdomadaire des dead-letter events
