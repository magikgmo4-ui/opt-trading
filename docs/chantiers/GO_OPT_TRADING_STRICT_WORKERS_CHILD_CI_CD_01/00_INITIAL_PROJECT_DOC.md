---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - strict_workers
  - ci_cd
  - pipeline
  - github_actions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Proposer pipeline CI/CD pour les workers stricts : validation job packets, smoke test, scheduling"
updated_at: 2026-05-19
links:
  - .github/workflows/openclaw-mcp-policy-static-validator.yml
  - .github/workflows/openclaw-skill-policy-warning-only.yml
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - docs/product/guides/CLICKUP_COCKPIT.md
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Proposer un pipeline CI/CD GitHub Actions pour les workers stricts : validation automatique des job packets, smoke test read-only du runner, verification des invariants doc-only, et scheduling optionnel.

## 2_CONTEXTE

Le runner strict_workers (`run_task.sh`) a ete valide en Phase A du RUNTIME_LOCK_AND_E2E_01. Les workflows GitHub Actions existants (openclaw-mcp-policy-static-validator) servent de reference pour le pattern CI/CD du repo.

## 3_BORNES_DU_CHILD

1. **Workflow CI** — validation des job packets JSON contre tasks.index.json
2. **Workflow CD** — smoke test read-only du runner sur une PR
3. **Scheduling** — optionnel, cron pour inventaire periodique
4. **Doc-only** — le workflow est propose mais pas actif (DRAFT_ONLY)

## 4_WORKFLOWS_PROJETES

### Workflow 1: strict-workers-validate.yml

```yaml
name: Strict Workers — Validate

on:
  pull_request:
    paths:
      - "scripts/ai/workers/job_packets/*.json"
      - "scripts/ai/workers/tasks.index.json"
      - "scripts/ai/workers/run_task.sh"

jobs:
  validate-job-packets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate all job packets
        run: |
          for packet in scripts/ai/workers/job_packets/*.json; do
            python3 scripts/ai/workers/_validate_job.py "$packet"
          done
```

### Workflow 2: strict-workers-smoke.yml

```yaml
name: Strict Workers — Smoke

on:
  pull_request:
    paths:
      - "scripts/ai/workers/**"
  workflow_dispatch:

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dry-run READ_INVENTORY
        run: |
          bash scripts/ai/workers/run_task.sh \
            --job-packet scripts/ai/workers/job_packets/smoke_read_inventory.json \
            --dry-run
```

## 5_INVARIANTS

- Aucun secret expose dans les workflows
- Aucun write reel declenche par CI/CD
- Tous les steps en dry-run / read-only
- Les workflows suivent le pattern existant du repo

## 6_CANONICAL_STATE

- Branche: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01
- Base: sot/mainline
- Workflows existants: openclaw-mcp-policy-static-validator.yml (pattern de reference)
- Runner valide: run_task.sh (Phase A, PASS)
