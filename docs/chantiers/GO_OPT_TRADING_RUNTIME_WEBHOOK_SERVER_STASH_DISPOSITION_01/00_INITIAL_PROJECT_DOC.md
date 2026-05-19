# 00_INITIAL_PROJECT_DOC.md

## 1_MASTER_TARGET
Decider du traitement final du stash contenant `webhook_server.py` sans executer d'action destructive ou runtime dans cette passe.

## 3_INITIAL_NEED
`webhook_server.py` est conserve dans `stash@{0}`. Le stash a deja ete inspecte en read-only et la decision temporaire `KEEP_STASH` a ete documentee. Il faut maintenant decider si le patch doit etre applique, supprime, exporte ou transfere dans une branche dediee.

## 4_MASTER_PROJECT_PLAN
1. Verifier que `sot/mainline` est clean et alignee.
2. Confirmer que `stash@{0}` contient toujours `webhook_server.py`.
3. Lire le diff stashed.
4. Evaluer les options `APPLY_PATCH` / `DROP_STASH` / `EXPORT_PATCH` / `NEW_BRANCH`.
5. Produire une decision recommandee avec risques et conditions d'execution.
6. Ne pas executer la decision sans validation explicite.

## 6_FINAL_TARGET
Un rapport de disposition permettant de choisir la suite operationnelle pour `webhook_server.py`.

## 12_INVARIANTS
- Ne pas pop `stash@{0}`.
- Ne pas appliquer `stash@{0}`.
- Ne pas drop `stash@{0}`.
- Ne pas modifier `webhook_server.py`.
- Ne pas commit de changement runtime/code.
- Ne pas push tant que la decision n'est pas validee.
