# module: repo_local_artifacts (v1)

Objectif
- Empêcher les dossiers *locaux* (worktrees, holds, inbox) d'apparaître en `git status` et d'être accidentellement commit.
- Fournir une sanity check rapide.

Ce module NE change pas ton code applicatif. Il ne fait que:
- Ajouter des patterns à `.gitignore`
- Fournir des scripts `cmd/menu/sanity` standardisés

Commandes
- `bash scripts/repo_local_artifacts_cmd.sh apply` : ajoute les patterns à `.gitignore` (idempotent)
- `bash scripts/repo_local_artifacts_sanity.sh` : sanity check
