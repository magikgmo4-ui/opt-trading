# 10_STASH_DISPOSITION_ANALYSIS.md

## 1_MASTER_TARGET
Evaluer objectivement le patch stashed de `webhook_server.py` et recommander une disposition finale.

## 7_CANONICAL_STATE
- Branche : `go/GO_OPT_TRADING_RUNTIME_WEBHOOK_SERVER_STASH_DISPOSITION_01`
- HEAD : `e7bbce06`
- Base : `sot/mainline`
- Stash inspecte : `stash@{0}: On sot/mainline: wip: preserve webhook_server.py before doc-only push`
- Fichier concerne : `webhook_server.py`
- Worktree status : propre avant creation de cette documentation locale

## WEBHOOK_SERVER_PATCH_SUMMARY
- Nature du changement : reecriture plein-fichier visible en brut, sans difference restante sous comparaison `-w`
- Zones touchees : tout `webhook_server.py`
- Lignes ajoutees : `963`
- Lignes supprimees : `963`
- Trailing whitespace : oui, prouve par `git diff --check stash@{0}^1 stash@{0} -- webhook_server.py`
- Comportement runtime potentiellement affecte : non prouve ; aucune difference logique isolee n'apparait dans les comparaisons sans whitespace
- Risque securite : faible si le stash reste inert ; inutilement perturbateur si applique tel quel sur un fichier runtime sensible
- Risque compatibilite : faible si le stash est supprime ; eleve pour la lisibilite et la review si ce bruit est reapplique
- Risque de conflit avec `sot/mainline` courant : inutilement eleve si le stash est applique, car il reecrit tout le fichier sans apporter de changement logique observable

## OPTION_MATRIX

| Option | Description | Avantage | Risque | Condition minimale | Recommandation |
|---|---|---|---|---|---|
| APPLY_PATCH | Appliquer le patch dans le worktree | Permet de recuperer immediatement le contenu stashe | Reintroduit un diff plein-fichier whitespace-only dans un fichier runtime | Prouver qu'un changement logique utile existe au-dela du whitespace | Non |
| DROP_STASH | Supprimer le stash | Elimine un artefact bruité sans valeur logique observable | Destructif si une information utile non detectee etait cachee | Valider explicitement qu'aucun besoin d'archivage supplementaire n'existe | Oui |
| EXPORT_PATCH | Exporter le patch en fichier `.patch` sans l'appliquer | Garde une trace hors stash avant suppression | Preserve surtout du bruit si le patch est whitespace-only | Besoin explicite d'archivage avant suppression | Non |
| NEW_BRANCH | Creer une branche dediee et appliquer le stash dessus | Isole l'experimentation hors `sot/mainline` | Cree une branche et un diff runtime sans signal logique prouve | Besoin explicite d'investigation approfondie sur l'origine du bruit | Non |

## DECISION_RECOMMENDATION
DROP_STASH

## DECISION_RATIONALE
`DROP_STASH` est l'option la plus solide car le stash ne montre aucune difference logique restante ni contre son parent (`git diff -w stash@{0}^1 stash@{0}`), ni contre le `HEAD` courant (`git diff -w HEAD stash@{0}`). Le contenu conserve uniquement une reecriture plein-fichier accompagnee de nombreux `trailing whitespace`. Dans ces conditions, reappliquer ou exporter ce patch preserve surtout du bruit technique, alors que le supprimer apres validation explicite reduit le risque futur de confusion sur un fichier runtime sensible.

## EXECUTION_PLAN_IF_VALIDATED
1. Verifier une derniere fois que `stash@{0}` est bien le stash attendu avec `git stash list`.
2. Si une archive est desiree avant suppression, utiliser `git stash show -p 'stash@{0}' > webhook_server_stash_review.patch` dans un GO dedie d'archivage.
3. Si la suppression est validee sans archive, executer `git stash drop 'stash@{0}'`.
4. Re-verifier `git stash list` pour confirmer la disparition du stash cible.
5. Ne faire aucune modification a `webhook_server.py` pendant cette sequence.

## 13_ESTABLISHED
- `stash@{0}` existe encore et touche uniquement `webhook_server.py`.
- `git stash show --stat 'stash@{0}'` affiche `963 insertions` et `963 deletions` sur un seul fichier.
- `git diff -w --stat stash@{0}^1 stash@{0} -- webhook_server.py` ne remonte aucune difference.
- `git diff --stat HEAD stash@{0} -- webhook_server.py` montre encore un diff plein-fichier brut contre le `HEAD` courant.
- `git diff -w --stat HEAD stash@{0} -- webhook_server.py` ne remonte aucune difference contre le `HEAD` courant.
- `git diff --check stash@{0}^1 stash@{0} -- webhook_server.py` remonte de nombreuses erreurs `trailing whitespace`.
- `webhook_server.py` n'a pas ete applique, modifie, poppe ou restaure pendant cette passe.

## 14_HYPOTHESIS
- Le stash provient probablement d'une conversion CRLF / espaces fin de ligne ou d'une reecriture d'editeur involontaire.
- Il est improbable qu'un correctif runtime utile soit cache dans ce diff, mais cela n'est pas prouve octet par octet.

## 15_REMAINING_GAP
- Une analyse binaire ou une exportation temporaire du patch serait necessaire si l'equipe veut exclure absolument toute variation non whitespace.
- La suppression du stash reste une action destructive et demande donc validation explicite.

## 16_TODO
- Valider ou non la recommandation `DROP_STASH`.
- Si vous voulez une ceinture de securite avant suppression, choisir explicitement `EXPORT_PATCH` avant `DROP_STASH`.
- Ne lancer aucune action sur `webhook_server.py` lui-meme tant que la disposition du stash n'est pas tranchee.

## 17_RESUME_POINT
GO ouvert ; rapport de disposition cree ; `stash@{0}` intact ; `webhook_server.py` non applique ; recommandation courante : `DROP_STASH` apres validation explicite.
