---
doc_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01_SHORTLIST
doc_type: shortlist
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
status: active
updated_at: 2026-05-23
---

# 30_SELECTED_AUTOMATION_SHORTLIST

## Sélection prioritaire (Shortlist)

Basé sur la matrice de score, les deux automatisations suivantes sont sélectionnées pour le prochain cycle :

### 1. Constraint Checking Lite (Validation de périmètre)
- **Objectif** : Empêcher les erreurs de périmètre lors des sessions `DOC_ONLY` ou `READ_ONLY`.
- **Mécanisme** : Script léger vérifiant si une session déclarée comme `DOC_ONLY` modifie des fichiers en dehors de `docs/`.
- **Valeur ajoutée** : Sécurité immédiate, réduction du risque de dérive, conformité automatique aux contraintes du GO.

### 2. GO Naming + Directory Creation (Standardisation des chantiers)
- **Objectif** : Automatiser la création de la structure canonique d'un chantier.
- **Mécanisme** : Script créant le dossier `docs/chantiers/<GO_ID>/`, validant le format du `GO_ID` et générant le fichier `00_INITIAL_PROJECT_DOC.md` à partir d'un template.
- **Valeur ajoutée** : Gain de temps massif, zéro erreur de nommage, uniformité de la structure documentaire.

## Synergie identifiée
La création de chantier pourra intégrer une vérification automatique de l'état Git (Candidat 11) pour s'assurer que l'opérateur part d'une base saine (`sot/mainline` à jour).
