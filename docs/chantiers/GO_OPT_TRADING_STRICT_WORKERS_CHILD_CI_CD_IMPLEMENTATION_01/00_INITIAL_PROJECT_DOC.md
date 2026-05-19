---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_IMPLEMENTATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_IMPLEMENTATION_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - ci_cd
  - github_actions
  - implementation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01/10_WORKFLOW_SPEC.md
point_de_reprise: "Materialiser les workflows CI/CD proposes par #599 dans .github/workflows/"
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01/10_WORKFLOW_SPEC.md
  - .github/workflows/openclaw-mcp-policy-static-validator.yml
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_IMPLEMENTATION_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Materialiser les 3 workflows CI/CD proposes par PR #599 dans `.github/workflows/` : validation des job packets, smoke test read-only du runner, inventaire hebdomadaire schedule.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| Workflow spec | PR #599: `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01/10_WORKFLOW_SPEC.md` |
| Pattern existant | `.github/workflows/openclaw-mcp-policy-static-validator.yml` |
| Runner valide | `scripts/ai/workers/run_task.sh` (Phase A, PASS) |
| Validateur | `scripts/ai/workers/_validate_job.py` |

## 3_BORNES_DU_CHILD

1. **strict-workers-validate.yml** — validation des job packets JSON sur PR
2. **strict-workers-smoke.yml** — smoke test read-only sur PR
3. **strict-workers-schedule.yml** — inventaire hebdomadaire cron
4. Chaque workflow suit le pattern YAML existant du repo
5. Aucune modification du runner ou des job packets existants

## 4_WORKFLOWS

### Workflow 1: strict-workers-validate.yml

Declencheur: PR modifiant job_packets/, tasks.index.json, run_task.sh, _validate_job.py
Action: Valider tous les job packets JSON via _validate_job.py

### Workflow 2: strict-workers-smoke.yml

Declencheur: PR modifiant scripts/ai/workers/ ou declenchement manuel
Action: Dry-run READ_INVENTORY + verification "no tracked files modified"

### Workflow 3: strict-workers-schedule.yml

Declencheur: Cron hebdomadaire (lundi 8h UTC) + workflow_dispatch
Action: Dry-run READ_INVENTORY automatique

## 5_INVARIANTS

- Aucun secret expose dans les workflows
- Aucun write reel declenche par CI/CD
- Tous les steps en dry-run / read-only
- Suit le pattern YAML existant du repo (contents: read, checkout@v4, python@v5)
