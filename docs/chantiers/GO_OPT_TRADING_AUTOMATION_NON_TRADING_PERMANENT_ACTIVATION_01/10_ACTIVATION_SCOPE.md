# 10_ACTIVATION_SCOPE

## Périmètre actif

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
| Drive canary packet | drive | WRITE_GATED | manual only | HITL required |

## Surfaces exclues

| Surface | Raison |
|---------|--------|
| Gmail | Retiré du périmètre actif (PR #691) |
| Calendar | Retiré du périmètre actif (PR #691) |
| clickup | Non validé pour activation permanente |
| airtable | Non validé pour activation permanente |
| botpress | Non validé pour activation permanente |
| telegram | Non validé pour activation permanente |
| google_sheets | Non validé pour activation permanente |
| trading | Hors scope (non-trading only) |

## Modes d'exécution

- **READ_ONLY** : activation scheduler permanente autorisée
- **WRITE_GATED** : activation manuelle seulement, approval HITL requise
- **DRAFT_ONLY** : non inclus dans l'activation permanente
