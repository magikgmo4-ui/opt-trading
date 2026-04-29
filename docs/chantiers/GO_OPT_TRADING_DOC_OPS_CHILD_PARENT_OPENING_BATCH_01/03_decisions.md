---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - parent_opening_batch
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/02_parent_opening_matrix.md
point_de_reprise: "Section Ce qui reste a faire"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/01_opening_plan.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/02_parent_opening_matrix.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 03_decisions

## Ce qui est etabli

- PR #181 est mergee sur `sot/mainline` au commit `7b75154` ;
- le parent actif reste `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` ;
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` devient le sous-GO canonique de l'etape courante ;
- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` et `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` sont ouverts dans ce lot ;
- `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` n'est pas cree comme doublon de `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` ;
- `BRANCH_STATE.md` reste non modifie.

## Ce qui reste hypothese

- `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` pourra etre ouvert plus tard si une frontiere machine-first est prouvee sans collision avec `deepseek_student` ;
- `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` pourra etre reconsidere si un usage support durable, distinct et non decoratif est etabli ;
- une promotion canonique de l'axe `localcms` pourra etre reouverte plus tard seulement si l'existant `UI_LOCALCMS` devient insuffisant.

## Ce qui est interdit

- rouvrir `BRANCH_CLEANUP` ;
- rouvrir `OPEN_WORK_CONTROL` ;
- rouvrir `CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL` ;
- rouvrir `PRIMARY_RESTART` ;
- rouvrir `PARENT_TARGET_MAP` ;
- lancer `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` dans ce lot ;
- creer un parent decoratif par symetrie.

## Ce qui reste a faire

- verifier le diff doc-only final ;
- valider la coherence des ouvertures admin-trading et db-layer dans les index ;
- utiliser `90_closeout.md` comme etat PASS local si le diff reste borne ;
- n'envisager `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` qu'apres validation humaine de ce lot.
