# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Inspecter le stash local contenant `webhook_server.py` et decider de son traitement futur sans appliquer le patch.

## 3_INITIAL_NEED
`webhook_server.py` est conserve dans `stash@{0}` depuis les passes doc-only precedentes. Il doit etre traite dans un GO separe avant toute restauration, suppression ou integration.

## 4_MASTER_PROJECT_PLAN
1. Verifier l'etat propre du repo.
2. Verifier que `sot/mainline` est alignee avec `origin/sot/mainline`.
3. Inspecter `stash@{0}` en read-only.
4. Resumer le diff de `webhook_server.py`.
5. Evaluer les options `APPLY_PATCH` / `KEEP_STASH` / `DROP_STASH` / `EXPORT_PATCH` / `NEW_BRANCH`.
6. Produire une recommandation sans executer la decision.

## 12_INVARIANTS
- Ne pas pop le stash.
- Ne pas appliquer le stash.
- Ne pas modifier `webhook_server.py`.
- Ne pas pousser sans validation.
- Ne pas melanger ce GO avec des docs parents ou index syncs.
