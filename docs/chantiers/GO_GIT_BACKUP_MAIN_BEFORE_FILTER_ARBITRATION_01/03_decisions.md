# GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01 - decisions

## Decision

| branche | etat reel observe | verdict | justification |
| --- | --- | --- | --- |
| `backup/main-before-filter` | remote-only, merged dans `origin/sot/mainline`, ancetre pur de `origin/main` et `origin/sot/mainline`, aucun commit propre hors canon actuel | `DROP_REMOTE_CANDIDATE` | la branche ne porte plus de valeur snapshot distincte ni d'ancrage canonique actif; elle reste un pointeur historique redondant deja conserve dans l'historique reachable |

## Preuves

- **Remote-only** : `git branch -a --list "*backup/main-before-filter*"` ne montre que `remotes/origin/backup/main-before-filter`
- **Ancetre pur de `origin/main`** : `git merge-base --is-ancestor origin/backup/main-before-filter origin/main` retourne vrai
- **Ancetre pur de `origin/sot/mainline`** : `git merge-base --is-ancestor origin/backup/main-before-filter origin/sot/mainline` retourne vrai
- **Aucun commit propre hors canon** : `git rev-list --left-right --count origin/sot/mainline...origin/backup/main-before-filter` retourne `835 0`
- **Branche deja absorbee** : `git branch -r --merged origin/sot/mainline` inclut `origin/backup/main-before-filter`
- **Absence d'ancrage canonique actif** : aucune reference repo active n'a ete trouvee dans la doc canonique; seules subsistent des traces de bundle de pilotage et une mention d'upload d'archive dans `journal.md:5678`

## Garde

- ne pas supprimer cette branche dans ce GO
- ne pas melanger sa suppression eventuelle avec `GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01`
- si suppression il y a, l'ouvrir comme passage Git separe et explicitement valide

## RISKS

- À qualifier.
