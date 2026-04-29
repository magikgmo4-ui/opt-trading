---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - branches
  - matrix
  - membership
  - go_index
  - branch_state
  - chantier
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "01_membership_matrix.md"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/BRANCH_STATE.md
---

# 00_cadrage — GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02

## Objet

Auditer uniquement l'appartenance documentaire des branches `GO_OPT_TRADING` encore presentes.

## Question de controle

Chaque branche `GO_OPT_TRADING` restante est-elle bien representee dans :

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/GO_INDEX.md`
- `docs/index/BRANCH_STATE.md`
- `docs/chantiers/`
- un frontmatter avec `go_id` top-level coherent

## Hors scope

- aucune suppression de branche
- aucun transport de fichier
- aucun merge
- aucune modification runtime
- aucune correction appliquee aux surfaces auditees

## Methode

- liste de travail = union des branches locales et distantes contenant `GO_OPT_TRADING`
- `in_MATRICE`, `in_GO_INDEX`, `in_BRANCH_STATE` = presence textuelle du `GO_ID` ou du nom de branche cible sur la surface canonique courante
- `chantier_dir_present` = presence d'un dossier direct `docs/chantiers/<GO_ID>/` sur la copie de travail courante
- `frontmatter_go_id` = verification d'un champ `go_id:` top-level dans le dossier chantier courant
- un `go_id` imbrique sous `module:` est traite comme non conforme pour ce controle
