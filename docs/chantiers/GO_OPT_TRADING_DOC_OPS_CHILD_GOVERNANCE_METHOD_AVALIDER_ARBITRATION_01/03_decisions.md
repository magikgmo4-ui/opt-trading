---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - governance
  - method
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md
---

# 03_decisions — Decisions

## Decision 1 : GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 -> THREAD_ARCHIVE_REFERENCE (ETABLI)

Ce GO sert principalement a classer, qualifier et preparer le reclassement des items obsolete/archive/legacy du repo. Les regles qu'il definit (categories, actions, anti-destruction) sont au service de cet objectif d'archivage, pas d'une methode de travail generale.

Fil retenu : THREAD_ARCHIVE_REFERENCE
Confiance : ETABLI

## Decision 2 : GO_GIT_PROGRESSIVE_MIGRATION_START_13 -> THREAD_METHOD_WORKFLOW (ETABLI)

Ce GO sert a organiser une methode progressive de migration Git dans le repo canonique. C'est un GO simple autonome qui porte une methode de travail structurante, pas un objet a archiver.

Fil retenu : THREAD_METHOD_WORKFLOW
Confiance : ETABLI

## Decision 3 : pas de changement dans la repartition par fil

Les 2 GO restent dans les fils initialement proposes. La repartition par fil ne change pas :
- THREAD_METHOD_WORKFLOW : 4 GO
- THREAD_ARCHIVE_REFERENCE : 3 GO

## Decision 4 : tous les GO gouvernance/methode sont desormais ETABLI

Apres arbitrage, il ne reste plus aucun GO A_VALIDER dans le perimetre gouvernance/methode. Les 16 GO sont tous en confiance ETABLI.

## Decision 5 : pas de modification de GO_INDEX.md

Ce lot ne modifie pas GO_INDEX.md. Les affectations de fil restent dans le dossier chantier.

## Decision 6 : suite logique

Apres ce lot :
- les GO gouvernance/methode sont tous arbitres
- la suite logique est de passer aux parents machine
- puis aux GO orphelins
