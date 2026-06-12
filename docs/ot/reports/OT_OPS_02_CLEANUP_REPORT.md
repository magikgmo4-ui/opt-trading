# OT-OPS-02 — RAPPORT DE CLEANUP WORKFLOW (RÉVISÉ)

## 1. ACTION SÛRE : PATCH DE v2
- Contenu de `fix3/scripts/post_change.sh` copié dans `workflow_post_change_v2/scripts/`.
- Vérification : le script ne contient plus `ssh student "sudo ..."`.

## 2. ACTION SÛRE : DÉPRÉCIATION
- Fichier `DEPRECATED.md` ajouté dans `fix3`.
- Registry mis à jour pour rediriger les appels vers `v2` et marquer `fix3` comme déprécié/fusionné.

## 3. NON-ACTION : SUPPRESSION
- Les dossiers `fix1`, `fix2`, `fix3` sont conservés physiquement.
- Le backup de `v2` est conservé.
- Aucun wrapper global n'a été touché (car `v2` est un module hook, sans wrapper `cmd-` public).

## 4. PROCHAINES ÉTAPES
- Observer si `fix1` ou `fix2` sont appelés (via logs).
- Si aucun appel pendant 30 jours, supprimer `fix1` et `fix2`.
- Archiver `fix3` plus tard.

## RISKS

- À qualifier.
