---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01_UI_STEPS
doc_type: procedure
---

# GitHub UI — Activation des Required Checks

## Méthode : Ruleset (recommandé)

GitHub recommande les rulesets (Settings > Rules > Rulesets) plutôt que l'ancienne branch protection.

### Créer un ruleset

1. Aller sur **Settings > Rules > Rulesets** dans le dépôt
2. Cliquer **New ruleset**
3. Choisir **"Branch ruleset"**

### Configuration

**Name :** `Required checks — sot/mainline`

**Target branches :**
```
sot/mainline
```

**Bypass :** laisser vide (personne ne bypass)

**Rules :**

1. **Require status checks** → cocher
2. **Require branches to be up to date** → cocher
3. Ajouter les checks un par un :

| Check |
|---|
| `gate/preflight` |
| `gate/file-scope` |
| `gate/no-lock-overlap` |
| `gate/tests` |

4. **Désactiver** "Do not require enforcement on admins" (ou laisser selon politique)
5. **Require a pull request before merging** → optionnel (recommandé)
6. S'assurer que **"Automatically request the first review from the PR author"** n'est pas coché

### Validation

1. Créer une PR de test (docs-only avec un seul GO)
2. Vérifier que les 4 checks `gate/*` s'affichent
3. Vérifier que le bouton merge est désactivé tant qu'un check n'est pas vert
4. Attendre le PASS des 4 checks
5. Vérifier que le merge est possible après PASS

## Méthode alternative : Branch Protection (legacy)

1. Aller sur **Settings > Branches**
2. Cliquer **"Add branch protection rule"**
3. **Branch name pattern :** `sot/mainline`
4. **Protect matching branches** → cocher
5. **Require status checks to pass before merging** → cocher
6. **Require branches to be up to date** → cocher
7. Chercher et sélectionner les 4 checks
8. Sauvegarder

> Note : l'ancienne branch protection est dépréciée par GitHub.  
> Les rulesets sont l'approche moderne.
