# Git Ops - Runbook

## 1. Objectif
Ce runbook décrit la procédure pour **synchroniser** efficacement les modifications entre le développement (Windows) et l'exploitation (Linux) via Git.
Il fournit des outils pour automatiser les tâches répétitives (commit/push/pull) et gérer les fichiers tracked modifiés localement.

## 2. Workflow Recommandé

### Étape 1 : Développement (Windows)
1. Modifier/Créer les fichiers.
2. Vérifier le status (Optionnel) :
   ```powershell
   .\scripts\git_ops\git_commit_push_windows.ps1 -ShowStatusOnly
   ```
3. Ajouter, Commiter et Pousser :
   ```powershell
   .\scripts\git_ops\git_commit_push_windows.ps1 -Paths "scripts/student", "docs/my_doc.md" -CommitMessage "feat: update student scripts"
   ```
   *Note : Les chemins peuvent être passés sous forme de tableau, ou comme une seule chaîne séparée par des virgules.*

### Étape 2 : Mise à Jour (Linux)
Sur chaque machine cible (`admin-trading`, `student`, `db-layer`) :

1. **Vérifier l'état** :
   ```bash
   git status --short
   ```

2. **Mettre à jour (Simple)** :
   ```bash
   bash scripts/git_ops/git_pull_update_linux.sh
   ```
   *Met à jour le repo (fast-forward only).*

3. **Mettre à jour avec Restauration (Si fichiers modifiés)** :
   Si des fichiers tracked (ex: scripts modifiés localement par erreur) bloquent le pull :
   ```bash
   bash scripts/git_ops/git_pull_update_linux.sh --paths scripts/student/my_script.sh
   ```
   *Restaure la version tracked du fichier avant de pull.*

## 3. Gestion des Erreurs

### Cas : Pull Bloqué (Conflict)
**Symptôme** : "error: Your local changes to the following files would be overwritten by merge".
**Action** :
- Identifier les fichiers en conflit (`git status`).
- Si les changements locaux sont à jeter : utiliser `--paths` avec le script d'update.
- Si les changements locaux sont à garder : `git stash`, puis update, puis `git stash pop`.

### Cas : Push Rejeté (Windows)
**Symptôme** : "Updates were rejected because the remote contains work that you do not have locally".
**Action** :
- Faire un `git pull --rebase` sur Windows.
- Résoudre les conflits éventuels.
- Relancer le script de push.

---
*Dernière mise à jour : 2026-03-06*

## RISKS

- À qualifier.
