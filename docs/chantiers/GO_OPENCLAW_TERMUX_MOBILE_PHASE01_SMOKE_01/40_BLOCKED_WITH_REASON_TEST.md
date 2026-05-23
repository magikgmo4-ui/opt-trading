---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_BLOCKED_WITH_REASON_TEST
doc_type: blocked_with_reason_test
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
status: active
updated_at: 2026-05-23
---

# 40_BLOCKED_WITH_REASON_TEST

## Objectif

Vérifier que le wrapper bloque correctement les demandes hors périmètre (phase invalide ou job inconnu/interdit).

## Résultats des tests de blocage

| Cas de test | Action | Job | Phase | Statut attendu | Résultat |
|---|---|---|---|---|---|
| Phase invalide | `list-jobs` | - | `PHASE_99` | `BLOCKED_WITH_REASON` | `PASS` (Bloqué avec raison: only PHASE_01 is allowed initially) |
| Job inconnu | `run-dry` | `unknown-job` | `PHASE_01` | `BLOCKED_WITH_REASON` | `PASS` (Bloqué avec raison: unknown or missing job_id) |
| Job de trading (simulé) | `preflight` | `repo-trading-start` | `PHASE_01` | `BLOCKED_WITH_REASON` | `PASS` (Bloqué avec raison: unknown or missing job_id) |

## Preuve JSON (Phase invalide)

```json
{
  "action": "list-jobs",
  "blocked_reason": "only PHASE_01 is allowed initially",
  "ok": false,
  "phase": "PHASE_99",
  "status": "BLOCKED_WITH_REASON",
  "timestamp": "2026-05-23T20:03:38.510096+00:00"
}
```

## Preuve JSON (Job inconnu)

```json
{
  "action": "run-dry",
  "blocked_reason": "unknown or missing job_id",
  "job_id": "unknown-job",
  "ok": false,
  "status": "BLOCKED_WITH_REASON",
  "timestamp": "2026-05-23T20:03:34.845768+00:00"
}
```

## Verdict Sécurité

```text
BLOCKING_LOGIC_VERIFIED_PASS
```
