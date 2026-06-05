---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01
machine: cursor-ai
status: active
lifecycle_stage: branch_cleanup
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - bundles/operator-export/EXPORT_MANIFEST.json
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01

## Objet

Option D : audit et nettoyage des branches cursor-ai apres merges A, B, C. Verifier que les branches mergees sont supprimees en remote, documenter les branches locales stales, et corriger l'incoherence mineure `EXPORT_MANIFEST.json` (#212 → #213).

## Etat valide

- Options A, B, C mergees (PR #210, #211, #213).
- Remote branches de PR supprimees par `gh pr merge --delete-branch`.
- Branches locales cursor-ai encore presentes (stale local).

## Livrables

| Action | Fichier |
| --- | --- |
| Audit branches | `10_BRANCH_STATE_AUDIT.md` |
| Nettoyage recommande | `20_CLEANUP_ACTIONS.md` |
| Correction manifest | `30_MANIFEST_CORRECTION.md` + `EXPORT_MANIFEST.json` |
| Verification | `40_VERIFICATION.md` |

## Invariants

- Doc-only / governance-only.
- Ne pas supprimer automatiquement de branches locales.
- Admin-trading ferme.
- Aucun runtime modifie.

## RISKS

- À qualifier.
