---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01_PLAN
doc_type: plan
---

# Operational Orchestration Plan

## Architecture

```
OpenClaw                          GitHub Actions
─────────                         ──────────────
  │                                    │
  │  lit le registry (YAML)            │
  │  filtre orchestrable jobs          │
  │                                    │
  │──── POST /dispatches ────────────▶ │
  │◀─── 204 (run scheduled) ────────── │
  │                                    │
  │──── GET /runs/{id} ──────────────▶ │
  │◀─── status + conclusion ─────────  │
  │                                    │
  │──── GET /runs/{id}/logs ──────────▶│
  │◀─── logs (si disponibles) ───────  │
  │                                    │
  │  génère OPERATIONAL_REPORT_01.md   │
  │  classe PASS/FAIL/BLOCKED/REVIEW   │
  │  propose action suivante (no exec) │
```

## Étapes

### Étape 1 : Registry discovery
- Charger `GITHUB_ACTIONS_JOBS_REGISTRY_01.yml`
- Filtrer `orchestrable_by_openclaw=true`
- Filtrer `risk_level=low` (phase initiale)
- Afficher la liste des jobs disponibles

### Étape 2 : Trigger manuel (read-only phase)
- Sélectionner un job low-risk :
  - `github-actions-job-registry-check`
  - `repo-diff-check`
  - `strict-worker-job-packet-validate`
- Déclencher `workflow_dispatch` via API GitHub
- Vérifier le code retour 204

### Étape 3 : Polling
- Interroger `/repos/{owner}/{repo}/actions/runs/{run_id}`
- Intervalle : 20s
- Timeout : 300s
- Récupérer `status` et `conclusion`

### Étape 4 : Récupération logs
- Si disponible : GET `/repos/{owner}/{repo}/actions/runs/{run_id}/logs`
- Sinon : signaler logs non disponibles

### Étape 5 : Classification
| Conclusion | Classification |
|---|---|
| `success` | PASS |
| `failure` | FAIL |
| `cancelled` | BLOCKED |
| `timed_out` | BLOCKED |
| `action_required` | NEEDS_HUMAN_REVIEW |

### Étape 6 : Proposition action suivante
- PASS → "Ready for next operational cycle"
- FAIL → "Check run logs — possible registry or workflow issue"
- BLOCKED → "Check GitHub Actions queue or permissions"
- NEEDS_HUMAN_REVIEW → "Manual intervention required on GitHub"

### Étape 7 : Rapport
- Générer `OPERATIONAL_REPORT_01.md` dans le chantier
- Contenu : date, job ID, run ID, status, classification, logs URL, next action
