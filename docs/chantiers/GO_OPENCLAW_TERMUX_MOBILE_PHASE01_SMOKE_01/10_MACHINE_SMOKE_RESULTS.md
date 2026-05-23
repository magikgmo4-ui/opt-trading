---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_MACHINE_SMOKE_RESULTS
doc_type: machine_smoke_results
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
status: active
updated_at: 2026-05-23
---

# 10_MACHINE_SMOKE_RESULTS

## Environnement de test

- **Système** : Linux x64
- **Branche** : `go/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01`
- **Date** : 2026-05-23

## Résultats des commandes

| Commande | Statut | Résultat JSON |
|---|---|---|
| `status` | PASS | `available_jobs: 12`, `ok: true` |
| `list-jobs` | PASS | Liste de 12 jobs Phase 01 récupérée. |
| `preflight` | PASS | Toutes les vérifications passent pour `repo-status-check`. |
| `run-dry` | PASS | `git status` exécuté avec succès. |

## Preuves d'exécution

### Commande `status`
```json
{
  "action": "status",
  "available_jobs": 12,
  "available_phases": [
    "PHASE_01"
  ],
  "status": "PASS",
  "timestamp": "2026-05-23T20:03:02.951363+00:00"
}
```

### Commande `run-dry` (repo-status-check)
```json
{
  "action": "run-dry",
  "job_id": "repo-status-check",
  "ok": true,
  "status": "PASS",
  "stdout": "## go/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01\n?? docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01/\n?? reports/ai/mobile_control/",
  "timestamp": "2026-05-23T20:03:03.353035+00:00"
}
```

## Verdict Machine

```text
MACHINE_SMOKE_PASS
```
