---
doc_id: OPT_TRADING_REPO_ROOT_POLICY
doc_type: governance_policy
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - governance
  - root
  - policy
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Regles racine"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
  - docs/governance/REPO_ROLE.md
  - docs/INDEX.md
---

# REPO_ROOT_POLICY — opt-trading

## Objet
Fixer la politique canonique de la racine interne du repo.

Cette politique est subordonnée à l'état réel prouvé puis à `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
Elle fixe seulement l'application locale à la racine de `opt-trading`.

## Portée
- ce document traite ce qui reste à la racine **dans le repo**
- la frontière repo/hors-repo reste portée par `docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt`

## Règles racine
- ne laisser à la racine que les éléments ayant une valeur d’entrée, d’exécution ou de compatibilité explicite
- rattacher tout objet racine à une catégorie documentée (runtime, support, legacy, ou en attente d’arbitrage)
- éviter les dépôts opportunistes non qualifiés à la racine

## Classes d’objets racine
- **Entrée produit/runtime** : artefacts d’accès immédiat à l’exécution
- **Support opératoire** : fichiers de support temporairement conservés avec justification
- **Legacy toléré** : éléments conservés pour compatibilité, explicitement marqués
- **Arbitrage ouvert** : objets à reclasser dans un chantier dédié ultérieur

## Objets racine actuellement sous arbitrage
Les objets suivants sont considérés comme sous arbitrage de reclassement (aucun déplacement dans ce lot) :
- `Readme`
- `TOOLBOX.txt`
- `UI_URLS.md`
- `journal_add.sh`
- `smartmoney.txt`
- `bitget_bridge.py`
- `_archive/`
- `trae_pack_texts/`
- `.gitignore.bak*`

## Limites
- ce document ne déplace aucun fichier à lui seul
- ce document ne remplace pas les chantiers de reclassement physique

## REPRISE
- suivi via `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`
