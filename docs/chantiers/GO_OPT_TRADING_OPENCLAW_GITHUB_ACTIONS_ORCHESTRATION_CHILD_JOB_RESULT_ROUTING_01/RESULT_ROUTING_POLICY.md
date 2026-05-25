---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01_RESULT_ROUTING_POLICY
doc_type: policy
repo: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_RESULT_ROUTING_01
parent_go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
sphere: openclaw_github_actions_result_routing
surface: docs/chantiers
status: adopted
---

# RESULT_ROUTING_POLICY_01

## 1. Déclencheur

Un résultat de job GitHub Actions est routé quand :
- `classify_conclusion()` retourne une classification non nulle
- Le run est en statut `completed` ou a une conclusion exploitable
- Le job a été sélectionné par `route_jobs()` dans le GO précédent

## 2. Décisions

Quatre décisions possibles :

| Décision | Condition | Action proposée |
|---|---|---|
| PASS | conclusion = success, neutral | ready_for_human_review |
| FAIL | conclusion = failure | inspect_logs_and_prepare_fix |
| BLOCKED | conclusion = cancelled, timed_out, ou status = in_progress sans conclusion | unblock_permissions_or_timeout |
| NEEDS_HUMAN_REVIEW | conclusion = action_required, skipped, null, unknown | manual_review_required |

## 3. Règles

- **R1** — La décision est toujours produite par `classify_conclusion()`.
- **R2** — `next_action` est toujours une chaîne descriptive, jamais une exécution.
- **R3** — Le rapport inclut toujours run_id, html_url, job_id, workflow, classification, next_action.
- **R4** — Les logs disponibles sont notés (true/false) mais pas téléchargés.
- **R5** — Aucune mutation sur GitHub, trading, ou secrets.
- **R6** — L'humain valide toujours la next_action.

## 4. Format de sortie

```json
{
  "run_id": 123456789,
  "html_url": "https://github.com/...",
  "job_id": "example-job",
  "workflow": ".github/workflows/example.yml",
  "status": "completed",
  "conclusion": "success",
  "classification": "PASS",
  "logs_available": true,
  "probable_cause": null,
  "next_action": "ready_for_human_review"
}
```

## 5. Non-couvert

Ce GO ne couvre PAS :
- L'analyse détaillée des logs (GO suivant : FAILURE_LOGS_ANALYSIS_01)
- Le déclenchement automatique de correctifs
- La décision d'escalade vers un humain hors bande
