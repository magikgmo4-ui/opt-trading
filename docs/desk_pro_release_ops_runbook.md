# Desk Pro - Release Ops Runbook

## 1. Objectif
Ce runbook décrit la procédure pour **figer** une version du système Desk Pro (Release) depuis Windows, puis la **vérifier** sur les machines Linux (`admin-trading`, `student`, `db-layer`).

## 2. Pré-requis
- Accès au repository Git (Windows et Linux)
- Permissions de tag/push sur `origin`
- Scripts `release_ops` présents

## 3. Workflow de Release

### Étape 1 : Figer sur Windows (Master)
1. **Ouvrir PowerShell** dans la racine du repo.
2. **Vérifier l'état** : `git status` (doit être clean).
3. **Créer le Tag** :
   ```powershell
   .\scripts\release_ops\desk_pro_freeze_tag.ps1 -TagName "v1.2.0" -TagMessage "Release v1.2.0: Ops Pack Final"
   ```
   *Le script vérifie la propreté, crée le tag annoté, et pousse vers origin.*

### Étape 2 : Vérifier sur Linux (Target)
Sur chaque machine cible (`admin-trading`, `student`, `db-layer`) :

1. **Mettre à jour** :
   ```bash
   git pull
   git fetch --tags
   ```

2. **Vérifier le Tag** :
   ```bash
   bash scripts/release_ops/desk_pro_verify_tag_linux.sh v1.2.0
   ```
   *Doit retourner "PASS: Tag 'v1.2.0' exists locally."*

3. **Validation Finale** :
   Lancer un `sanity-desk-pro` (ou équivalent local) pour confirmer que la version taggée fonctionne.

## 4. Gestion des Erreurs

### Cas : Working Tree Dirty (Windows)
**Symptôme** : Le script refuse de tagger.
**Action** :
- Commiter les changements : `git commit -am "fix..."`
- Ou utiliser `-Force` (déconseillé pour une release propre).

### Cas : Tag Existant
**Symptôme** : "FAIL: Tag already exists".
**Action** :
- Choisir un nouveau numéro de version (ex: v1.2.1).
- Ou supprimer le tag local/remote si c'est une erreur (dangereux).

### Cas : Tag Introuvable (Linux)
**Symptôme** : "FAIL: Tag not found".
**Action** :
- Vérifier que le push Windows a réussi.
- Faire `git fetch --tags` sur Linux.

---
*Dernière mise à jour : 2026-03-06*
