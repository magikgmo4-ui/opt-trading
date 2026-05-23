---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_OPENCLAW_E2E_RUNBOOK
doc_type: runbook
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - openclaw
  - e2e
  - runbook
  - gates
  - evidence
---

# 20_OPENCLAW_E2E_RUNBOOK

## 1_ROLE

OpenClaw agit comme orchestrateur, gatekeeper et collecteur de preuves. Il ne contourne pas les gates et ne transforme pas un worker strict en agent write libre.

## 2_INPUTS_REQUIRED

- `GO_ID`: `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01`
- patch: `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch`
- sidecar zip: absent pour ce GO
- base branch: `sot/mainline`
- work branch: `go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01`
- docs sources:
  - `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
  - `scripts/ai/workers/tasks.index.json`
  - `scripts/ai/workers/models.registry.json`
  - `docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md`

## 3_PREFLIGHT_GIT

```bash
git status --short --branch
git fetch --prune origin
git switch sot/mainline
git pull --ff-only origin sot/mainline
git switch -c go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
```

## 4_PREFLIGHT_POLICY

Verifier :

- aucun secret dans le patch ;
- aucun `.env` ;
- aucun token ;
- aucun credential ;
- aucun write externe ;
- aucune modification runtime ;
- aucune modification des index globaux ;
- job packets compatibles avec tasks existantes ;
- modeles references presents ou fallback explicite.

## 5_PATCH_APPLICATION

```bash
git apply --check GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
git apply GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
git diff --check
git status --short
```

## 6_JOB_GRAPH_EXECUTION

Ordre recommande :

1. `READ_INVENTORY` — confirmer fichiers ajoutes et contexte.
2. `FAST_TRIAGE` — classer risques et gaps.
3. `PATCH_DRAFT` — verifier diff attendu et coherences.
4. `TESTPLAN` — produire plan test humain/CI.
5. `DOC_DRAFT` — proposer closeout si target atteint.
6. `ENDPOINT_AUDIT` — optionnel, verifier model registry si besoin.
7. `WRITE_GATED` — uniquement si approbation humaine explicite.

## 7_EXTERNAL_APP_WORKERS

Pour ce GO d'ouverture, les apps externes restent `READ_ONLY_OR_SKIPPED`.

- ClickUp : optionnel pour creation/suivi de tache, gate `human_approve`.
- Telegram : optionnel pour notification, pas de rollback requis.
- LocalCMS : optionnel pour affichage cockpit, gate selon contrat.
- Drive/Gmail/Figma/Sheets/Airtable/Botpress/Calendar : non requis.

## 8_EVIDENCE_REQUIRED

- `git apply --check`: PASS
- `git apply`: PASS
- `git diff --check`: PASS
- `git status --short`: liste attendue uniquement
- JSON job packets parseables
- aucun fichier interdit
- aucun global index modifie
- review humaine ou modele fort

## 9_CLOSEOUT

Closeout possible si :

- la spec gouvernance existe ;
- le dossier chantier existe ;
- les job packets existent ;
- l'entree inbox existe ;
- le patch est applique sans erreur ;
- aucun invariant n'est viole.

## 10_VERDICT_TARGET

Target attendue : `PASS_DOC_ONLY_OPENING_PATCH`.
