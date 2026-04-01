# module: repo_ownership_guard (v1)

Pourquoi
- Sur admin-trading, un `git merge/checkout` a échoué avec:
  `unable to unlink old ... Permission denied`
- Cause typique: des dossiers/fichiers **dans le repo** appartiennent à `root:root` (ou ne sont pas
  **writable** par l'utilisateur), souvent après un `sudo unzip`, `sudo cp`, ou un service qui écrit dans le repo.

Objectif
- **Scanner** et **corriger** (si demandé) les problèmes d'ownership/perms dans le repo `/opt/trading`
  pour éviter de briser Git.

Ce module:
- Ajoute des scripts standard `cmd/menu/sanity`.
- Ne change PAS le code applicatif.
- Les corrections (chown/chmod) sont des **métadonnées filesystem** → pas visibles dans git diff.

Commandes
- `bash scripts/repo_ownership_guard_sanity.sh` : scan read-only (recommandé avant tout)
- `bash scripts/repo_ownership_guard_cmd.sh fix` : corriger (utilise sudo)
- `bash scripts/repo_ownership_guard_cmd.sh fix --dry-run` : montrer ce qui serait fait
