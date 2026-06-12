---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - root
  - archive
  - arbitration
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/REPO_ROOT_POLICY.md
point_de_reprise: "Section Decision scope"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md
---

# 00_cadrage

## Objet

Arbitrer les 2 derniers GO actifs du bloc gouvernance root/archive puis les fermer si l'etat reel, les artefacts et les index le permettent sans action physique.

## Decision scope

GO traites uniquement :

- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`

## Regles

- doc-only uniquement
- aucun runtime
- aucun `modules/`
- aucun `scripts/`
- aucun deplacement physique
- aucune suppression
- aucun archivage physique
- aucun push sans instruction explicite
- `BRANCH_STATE.md` hors patch
- hors lot : naming, `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`, `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`

## Hypothese de travail

- `OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` peut etre ferme si sa matrice et ses sous-lots documentes suffisent desormais a qualifier les reliquats
- `ROOT_POLICY_AND_RECLASS_01` peut etre ferme si la politique racine absorbe explicitement le dernier cas ouvert `bitget_bridge.py`

## RISKS

- À qualifier.
