---
doc_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - modules
  - canonical
  - archive
  - execution
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/01_grille_decision.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/03_priorisation_familles.md
---

# Plan operationnel step-by-step

## Step 01 - qualifier les familles
- statut : complete
- objectif : fixer la grille canonique / utile / compat / legacy / archive

## Step 02 - ordonner les familles
- statut : complete
- objectif : prioriser les familles ou la duplication active est la plus coûteuse

## Step 03 - ouvrir des sous-lots d'execution
- statut : in_progress
- objectif : traiter famille par famille avec sortie obligatoire :
  - module canonique
  - compat temporaire
  - legacy fige
  - archive/backup

## Step 04 - couper les references actives
- statut : pending
- objectif : aligner wrappers, registre et docs sur le canonique retenu

## Step 05 - deplacer en archive
- statut : pending
- objectif : sortir physiquement les surfaces depassees une fois les callers coupes

## Point de reprise
Sous-lot actif :
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01`

Sous-lot enfant ouvert depuis cette classification :
- `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01`
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`

Regle maintenue :
- ne pas deplacer physiquement avant la coupe des references actives.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
