# 10_ACTIVATION_SCOPE

## Périmètre actif

### READ_ONLY schedulés

| Job | Surface | Mode | Scheduler | Approval |
|-----|---------|------|-----------|----------|
| repo-status-check | repo | READ_ONLY | timer 5min | none |
| repo-diff-check | repo | READ_ONLY | timer 15min | none |
| repo-pr-audit | repo | READ_ONLY | timer 1h | none |
| ledger-heartbeat | ledger | READ_ONLY | timer 5min | none |
| ledger-replay-check | ledger | READ_ONLY | timer 1h | none |
| automation-health-status | localcms | READ_ONLY | timer 5min | none |
| anti-leak-scan | repo | READ_ONLY | timer 6h | none |
| strict-worker-readonly-smoke | strict_worker | READ_ONLY | timer 30min | none |
| capability-matrix-validate | registry | READ_ONLY | timer 24h | none |
| bridge-contract-validation | contract | READ_ONLY | timer 24h | none |
| hitl-scenarios-smoke | localcms | READ_ONLY | manual | none |
| localcms-status-sync | localcms | READ_ONLY | timer 5min | none |
| airtable-read-health | airtable | READ_ONLY | timer 30min | none |
| clickup-read-health | clickup | READ_ONLY | timer 30min | none |
| botpress-read-health | botpress | READ_ONLY | timer 30min | none |
| sheets-read-health | google_sheets | READ_ONLY | timer 30min | none |
| telegram-automation-digest | telegram | READ_ONLY | timer 1h | none |

### WRITE_GATED (manuel seulement)

| Job | Surface | Mode | Scheduler | Approval |
|-----|---------|------|-----------|----------|
| Drive canary packet | drive | WRITE_GATED | manual | HITL required |
| airtable-write-canary | airtable | WRITE_GATED | manual | HITL required |
| clickup-write-canary | clickup | WRITE_GATED | manual | HITL required |
| botpress-write-canary | botpress | WRITE_GATED | manual | HITL required |
| sheets-write-canary | google_sheets | WRITE_GATED | manual | HITL required |

## Surfaces exclues

| Surface | Raison |
|---------|--------|
| Gmail | Retiré du périmètre actif (PR #691) |
| Calendar | Retiré du périmètre actif (PR #691) |
| trading | Hors scope (non-trading only) — écriture, signal, order |

## Modes d'exécution

- **READ_ONLY** : activation scheduler permanente autorisée
- **WRITE_GATED** : activation manuelle seulement, approval HITL requise, aucun timer permanent
- **DRAFT_ONLY** : non inclus dans l'activation permanente
