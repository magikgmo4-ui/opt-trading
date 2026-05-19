---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01_WORKFLOW_SPEC
doc_type: workflow_spec
repo: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_01
status: draft
---

# 10_WORKFLOW_SPEC — CI/CD pour Workers Stricts

## Workflow 1: strict-workers-validate.yml

**Declencheur :** PR modifiant job_packets/, tasks.index.json, run_task.sh
**Action :** Valider tous les job packets JSON contre tasks.index.json

```yaml
name: Strict Workers — Validate Job Packets

on:
  pull_request:
    paths:
      - "scripts/ai/workers/job_packets/*.json"
      - "scripts/ai/workers/tasks.index.json"
      - "scripts/ai/workers/run_task.sh"
      - "scripts/ai/workers/_validate_job.py"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    name: Validate Job Packets
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Validate all job packets
        run: |
          failed=0
          for packet in scripts/ai/workers/job_packets/*.json; do
            echo "Validating: $packet"
            if python3 scripts/ai/workers/_validate_job.py "$packet"; then
              echo "  PASS"
            else
              echo "  FAIL"
              failed=$((failed + 1))
            fi
          done
          exit $failed
```

---

## Workflow 2: strict-workers-smoke.yml

**Declencheur :** PR modifiant scripts/ai/workers/ ou declenchement manuel
**Action :** Smoke test read-only du runner avec READ_INVENTORY

```yaml
name: Strict Workers — Smoke Test

on:
  pull_request:
    paths:
      - "scripts/ai/workers/**"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  smoke:
    name: Dry-Run Smoke
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - name: Dry-run READ_INVENTORY
        run: |
          bash scripts/ai/workers/run_task.sh \
            --job-packet scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json \
            --dry-run
      - name: Verify no tracked files modified
        run: |
          if [ -n "$(git diff --name-only)" ]; then
            echo "FAIL: tracked files were modified"
            git diff --name-only
            exit 1
          fi
          echo "PASS: no tracked files modified"
```

---

## Workflow 3: strict-workers-schedule.yml (optionnel)

**Declencheur :** Cron hebdomadaire
**Action :** Inventaire automatique READ_ONLY

```yaml
name: Strict Workers — Scheduled Inventory

on:
  schedule:
    - cron: "0 8 * * 1"  # chaque lundi 8h UTC
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inventory:
    name: Weekly Inventory
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - name: Run READ_INVENTORY
        run: |
          bash scripts/ai/workers/run_task.sh \
            --job-packet scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json \
            --dry-run
```
