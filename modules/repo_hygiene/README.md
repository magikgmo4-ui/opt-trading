# repo_hygiene — Module d’hygiène repo (Source-of-Truth)

Objectif : éliminer les causes de confusion **Git/machines/journal** en détectant (et corrigeant prudemment) les artefacts et pièges suivants :

- Fichiers qui commencent par une ligne `\` (erreur fréquente → scripts/templates cassés)
- Artefacts SQLite runtime (`*.db-wal`, `*.db-shm`, `*.sqlite-wal`, `*.sqlite-shm`)
- Backups de patch `*.bak_*` (non ignorés par défaut) qui polluent les merges
- Détection d’un legacy student cmd auto-référencé (boucle infinie)
- Rapport “scan” clair pour décider quoi corriger

Ce module **ne supprime rien automatiquement** sans action explicite : par défaut il est en *scan/dry-run*.

## Installation (admin-trading)
1) Dézipper à la racine du repo (/opt/trading)
2) Installer les raccourcis (sudo)
3) Lancer le sanity

Commandes :
```bash
cd /opt/trading
sudo bash modules/repo_hygiene/install_shortcuts.sh
sanity-repo_hygiene
```

## Commandes utiles
```bash
cmd-repo_hygiene scan
cmd-repo_hygiene fix-leading-backslash --apply
cmd-repo_hygiene cleanup-artifacts --apply
```

## Notes
- `.gitignore` est étendu pour ignorer WAL/SHM + `*.bak_*`.
- Si `journal.md` est tracké, le module **ne le retire pas** (car destructif). Il te donne la commande à exécuter si tu veux le dé-tracker plus tard.
