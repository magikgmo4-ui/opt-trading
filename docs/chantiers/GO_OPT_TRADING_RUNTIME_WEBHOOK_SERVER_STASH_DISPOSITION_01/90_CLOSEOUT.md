# GO_OPT_TRADING_RUNTIME_WEBHOOK_SERVER_STASH_DISPOSITION_01_CLOSEOUT

## 1_MASTER_TARGET
Clore la passe de disposition du stash contenant `webhook_server.py` avec une recommandation documentee `DROP_STASH`, sans executer la suppression dans ce GO.

## 7_CANONICAL_STATE
- GO : `GO_OPT_TRADING_RUNTIME_WEBHOOK_SERVER_STASH_DISPOSITION_01`
- Branche : `go/GO_OPT_TRADING_RUNTIME_WEBHOOK_SERVER_STASH_DISPOSITION_01`
- Fichier concerne : `webhook_server.py`
- Stash concerne : `stash@{0}`
- Decision recommandee : `DROP_STASH`
- Application du stash : `NON`
- Pop du stash : `NON`
- Drop du stash : `NON`
- Modification de `webhook_server.py` : `NON`

## 13_ESTABLISHED
- `stash@{0}` existe encore au moment de la cloture documentaire.
- `webhook_server.py` n'a pas ete restaure dans le worktree.
- Le patch n'a pas ete applique.
- La recommandation documentee est `DROP_STASH`.
- Aucun changement runtime/code n'a ete execute dans ce GO.
- Le GO produit une decision de disposition, pas l'action destructive elle-meme.

## 14_HYPOTHESIS
- Le contenu stashed est probablement obsolete ou non utile par rapport a `sot/mainline` courant.
- La suppression du stash reduirait le bruit operationnel local.
- Une derniere verification juste avant drop reste necessaire, car l'ordre des stash peut changer.

## 15_REMAINING_GAP
- La suppression effective de `stash@{0}` n'est pas encore executee.
- Avant tout `DROP_STASH`, il faut reverifier que le stash cible contient bien `webhook_server.py`.
- Si l'ordre des stash change, cibler par contenu/message, pas uniquement par index `stash@{0}`.

## 16_TODO
1. Publier cette trace documentaire via PR doc-only.
2. Apres merge, executer une passe locale separee `DROP_STASH`.
3. Avant suppression, verifier :
   - `git stash list`
   - `git stash show --name-status <stash_ref>`
   - presence de `webhook_server.py` dans le stash cible
4. Executer `DROP_STASH` seulement apres validation explicite.

## 17_RESUME_POINT
GO ferme documentairement avec decision recommandee `DROP_STASH`. Le stash reste intact jusqu'a une action separee explicitement validee.

## 12_INVARIANTS
- Ne pas utiliser `stash@{0}` aveuglement si l'ordre des stash change.
- Ne pas appliquer `webhook_server.py`.
- Ne pas pop le stash.
- Ne pas supprimer le stash avant validation finale.
- Ne pas melanger `DROP_STASH` avec une PR doc-only.
