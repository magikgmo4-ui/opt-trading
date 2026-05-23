---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_HUMAN_CLAUDE_COWORK_CHECKLIST
doc_type: human_checklist
repo: opt-trading
project: opt-trading
module: operations
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - human
  - claude_cowork
  - checklist
  - pc_control
---

# 60_HUMAN_CLAUDE_COWORK_CHECKLIST

## 1_ROLE

Cette checklist sert si un assistant coworker ou un humain prend le controle du PC pour appliquer ou verifier le patch.

## 2_NAVIGATION

- Ouvrir terminal dans la racine du repo `opt-trading`.
- Verifier la branche.
- Copier le patch a la racine.
- Executer les commandes de preflight.
- Appliquer le patch seulement apres `git apply --check` PASS.

## 3_ACTIONS_TERMINAL

```bash
git status --short --branch
git fetch --prune origin
git switch sot/mainline
git pull --ff-only origin sot/mainline
git switch -c go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
git apply --check GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
git apply GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch
git diff --check
git status --short
```

## 4_UI_CHECKS

- Verifier visuellement le dossier `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/`.
- Verifier que les fichiers `.json` sont sous `scripts/ai/workers/job_packets/`.
- Verifier qu'aucun fichier secret n'a ete cree.
- Verifier qu'aucun index global n'a ete modifie.

## 5_HUMAN_APPROVAL

Avant commit, confirmer :

- [ ] Le patch ouvre seulement le chantier V2.
- [ ] Aucun runtime n'est touche.
- [ ] Aucun secret n'est present.
- [ ] Aucun global index n'est modifie.
- [ ] Les docs sont coherentes.
- [ ] Les job packets sont DRAFT_ONLY.

## 6_COMMIT_AND_PR

```bash
git add docs/governance/PATCH_ZIP_EXECUTION_FORMAT_V2_01.md   docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01   docs/index/inbox/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.md   scripts/ai/workers/job_packets/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_*.json

git commit -m "docs: open patch zip execution format v2"
git push -u origin go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
```

Ouvrir PR vers `sot/mainline`.

## 7_STOP_CONDITIONS

Stop immediat si :

- `git apply --check` echoue ;
- des fichiers hors scope apparaissent ;
- un secret est detecte ;
- un global index est modifie ;
- un write externe est demande ;
- la branche de base n'est pas a jour.
