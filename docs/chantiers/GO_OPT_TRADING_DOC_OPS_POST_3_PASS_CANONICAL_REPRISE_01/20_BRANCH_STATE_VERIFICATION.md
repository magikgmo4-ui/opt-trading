# 20_BRANCH_STATE_VERIFICATION.md

## Verification BRANCH_STATE

| Branche | Statut reel | BRANCH_STATE |
|---|---|---|
| `OPEN_WORK_CONTROL_01` | Existe local+remote, non mergee | BLOCKED — conservee |
| `OPEN_WORK_CONTROL_01_ISOLATED` | Supprimee local+remote | DROP_MERGED — completement supprimee |
| `BUNDLES_REPO_STORAGE_PARENT_01` | Merge dans sot/mainline, remote encore presente | DROP_MERGED — remote a supprimer |
| `CLICKUP_PARENT_CONTINUITY_01` | Existe, non mergee | A_VERIFIER — KEEP, hors lot actif |

## Decision

- **OPEN_WORK_CONTROL_01** : conservee. Ne pas supprimer. Delta reseau_ssh trop lourd pour suppression sans merge explicite.
- **OPEN_WORK_CONTROL_01_ISOLATED** : completement supprimee. Aucune action supplementaire.
- **BUNDLES_REPO_STORAGE_PARENT_01** : mergee dans sot/mainline. La remote peut etre supprimee dans un prochain lot.
- **CLICKUP_PARENT_CONTINUITY_01** : conservee. Routage fantome. Hors lot actif.

## RISKS

- À qualifier.
