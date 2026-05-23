---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_LAUNCH_PROMPT
doc_type: launch_prompt
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - launch_prompt
  - ide
  - openclaw
  - patch
---

# 05_LAUNCH_PROMPT

## Prompt IDE / OpenClaw

```text
GO: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01

Objectif:
Appliquer le patch d'ouverture du chantier PATCH_ZIP_EXECUTION_FORMAT_V2_01.

Base:
- repo: opt-trading
- branche base: sot/mainline
- branche travail recommandee: go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01

Preflight obligatoire:
1. git status --short --branch
2. git fetch --prune origin
3. git switch sot/mainline
4. git pull --ff-only origin sot/mainline
5. git switch -c go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
6. verifier presence:
   - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
   - scripts/ai/workers/tasks.index.json
   - scripts/ai/workers/models.registry.json
   - docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md

Application:
1. git apply --check GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
2. git apply GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
3. git diff --check
4. git status --short
5. verifier les nouveaux fichiers docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/
6. verifier les job packets scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_*.json

Contraintes:
- doc-only
- aucun secret
- aucun .env
- aucun global index
- aucun write externe
- aucun runtime
- aucun push force sauf besoin explicite et force-with-lease

Commit propose:
docs: open patch zip execution format v2

PR:
Ouvrir une PR vers sot/mainline avec description:
- spec PATCH_ZIP_EXECUTION_FORMAT_V2_01
- patch-first
- zip optional sidecar
- OpenClaw E2E runbook
- strict workers reuse
- evidence contract
```
