---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01_CLASSIFICATION_MATRIX
doc_type: classification_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01
surface: docs/chantiers
status: closed
---

# CLASSIFICATION_MATRIX_01

## Mapping conclusion → classification

| conclusion | classification | probable_cause | next_action |
|---|---|---|---|
| `success` | PASS | Aucune | `ready_for_human_review` |
| `failure` | FAIL | Échec workflow — check run, test, ou build | `inspect_logs_and_prepare_fix` |
| `cancelled` | BLOCKED | Annulé manuellement ou par concurrence | `unblock_permissions_or_timeout` |
| `timed_out` | BLOCKED | Dépassement de timeout | `unblock_permissions_or_timeout` |
| `action_required` | NEEDS_HUMAN_REVIEW | Review manuelle requise | `manual_review_required` |
| `neutral` | NEEDS_HUMAN_REVIEW | Workflow neutral — statut indéterminé | `manual_review_required` |
| `skipped` | NEEDS_HUMAN_REVIEW | Job sauté par condition | `manual_review_required` |
| `null` + `completed` | NEEDS_HUMAN_REVIEW | Conclusion absente | `manual_review_required` |
| `null` + `in_progress` | BLOCKED | Run pas encore terminé | `unblock_permissions_or_timeout` |
| `null` + `queued` | BLOCKED | Run en file d'attente | `unblock_permissions_or_timeout` |

## Logs availability

| logs_available | Condition |
|---|---|
| `true` | conclusion non nulle et status = completed |
| `false` | conclusion nulle ou status ≠ completed |

## Cas limites

| Cas | Classification | Raison |
|---|---|---|
| conclusion manquante + status completed | NEEDS_HUMAN_REVIEW | Anomalie API — ne pas prendre de risque |
| timed_out + tests en cours | BLOCKED | Infra ou job trop long |
| success partiel (certains steps failed) | FAIL | GitHub reporte failure si un step échoue |
| cancelled par concurrence | BLOCKED | Nouveau push a annulé l'ancien run |
