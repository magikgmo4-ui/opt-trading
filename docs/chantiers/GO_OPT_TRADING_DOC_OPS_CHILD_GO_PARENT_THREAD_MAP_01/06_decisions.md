---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - decisions
  - parent_thread_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
---

# 06_decisions — Decisions

## Decision 1 : pas de GO_PARENT_THREAD_MAP.md dans ce lot

La matrice draft reste dans le dossier chantier. On ne cree pas `docs/index/GO_PARENT_THREAD_MAP.md` dans ce premier lot. La matrice sera promue dans un lot ulterieur si la matrice draft est validee.

## Decision 2 : GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 -> ASSIGN vers parent UI

Ce GO traite de l'integration forms compatible avec localcms. Il se rattache logiquement a `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`. Action : ASSIGN (a propager dans GO_INDEX si confirme).

## Decision 3 : GO_GIT_PROGRESSIVE_MIGRATION_START_13 -> KEEP (GO simple)

Ce GO est ACTIVE et traite de la migration Git progressive. C'est un GO simple autonome sans parent prouve dans le repo. Il reste en KEEP comme GO simple, rattaché a lui-même. Pas de deplacement.

## Decision 4 : parents machine inchanges

Les parents machine `admin-trading` et `db-layer` restent ouverts. `student` et `fantome` restent differes. Pas de changement dans ce lot.

## Decision 5 : BRANCH_STATE.md non modifie

`BRANCH_STATE.md` reste surface branche uniquement. Pas de modification dans ce lot sauf incoherence prouvee.

## Decision 6 : GO_INDEX.md reste verite de liste

`GO_INDEX.md` reste la verite canonique de liste. La matrice draft du chantier est subordonnee a GO_INDEX.

## Decision 7 : pas de nouveau parent machine

On n'ouvre pas de nouveau parent machine dans ce lot. Les seuls parents machine sont admin-trading, db-layer (ouverts) et student, fantome (differes).

## Decision 8 : non-deplacement sans preuve

Aucun GO n'est deplace d'un parent a un parent machine sans preuve. Les seuls deplacements proposes sont :
- GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 vers parent UI (preuve : le GO traite d'integration UI localcms)

## RISKS

- À qualifier.
