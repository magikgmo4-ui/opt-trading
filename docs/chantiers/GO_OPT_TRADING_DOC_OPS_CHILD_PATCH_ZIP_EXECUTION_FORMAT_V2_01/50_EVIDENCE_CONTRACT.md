---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_EVIDENCE_CONTRACT
doc_type: evidence_contract
repo: opt-trading
project: opt-trading
module: validation
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - evidence
  - validation
  - checklist
  - proof
---

# 50_EVIDENCE_CONTRACT

## 1_REQUIRED_EVIDENCE

| Evidence | Commande / source | Critere PASS |
| --- | --- | --- |
| Git preflight | `git status --short --branch` | branche claire, pas de pollution hors scope |
| Base synced | `git fetch --prune origin` + `git pull --ff-only` | base a jour |
| Patch check | `git apply --check GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch` | exit 0 |
| Patch apply | `git apply GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| JSON parse | `python -m json.tool scripts/ai/workers/job_packets/*.json` | exit 0 pour fichiers du GO |
| Scope | `git diff --name-only` | seulement fichiers attendus |
| Global index guard | inspection diff | aucun global index modifie |
| Secret guard | grep / scanner local | aucun secret / token / .env |
| Review | humain ou modele fort | no blocking finding |

## 2_EXPECTED_FILES

```text
docs/governance/PATCH_ZIP_EXECUTION_FORMAT_V2_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/05_LAUNCH_PROMPT.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/10_SESSION_CONTEXT_AND_DECISIONS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/20_OPENCLAW_E2E_RUNBOOK.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/30_WORKER_JOB_GRAPH.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/40_EXTERNAL_APPS_WORKERS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/50_EVIDENCE_CONTRACT.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/60_HUMAN_CLAUDE_COWORK_CHECKLIST.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/70_TARGET_STATUS_GAPS_CLOSEOUT.md
docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.md
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_READ_INVENTORY_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_FAST_TRIAGE_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_PATCH_DRAFT_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_TESTPLAN_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_DOC_DRAFT_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_ENDPOINT_AUDIT_01.json
scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_WRITE_GATED_01.json
```

## 3_FORBIDDEN_EVIDENCE

Ne jamais inclure comme preuve :

- `.env` ;
- token ;
- credential ;
- cle privee ;
- dump complet sensible ;
- capture contenant secret ;
- log contenant token.

## 4_CLOSEOUT_EVIDENCE

Closeout acceptable si :

- patch applique ;
- tous fichiers attendus presents ;
- checks PASS ;
- PR ouverte ou commit local documente ;
- aucun invariant viole.
