# Rollback — Template

## Option A — Git (recommandé)
- Voir le commit/tag créé avant changement
- `git log --oneline -n 10`
- Revenir: `git checkout <commit> -- <files>` ou `git revert <commit>`

## Option B — Patch
- Appliquer le patch inverse ou restaurer via backup:
  - `git apply backups/<timestamp>/diff.patch` (si patch forward)
  - ou `git apply -R ...` (reverse)

## Notes
- Toujours exécuter le sanity check après rollback.
