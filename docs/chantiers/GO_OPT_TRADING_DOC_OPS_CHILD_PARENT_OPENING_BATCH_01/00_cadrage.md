---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - parent_opening_batch
  - parent_project_machine_split
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
point_de_reprise: "Section Decisions d'ouverture"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/01_parent_target_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/02_validation_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/90_closeout.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01

## Objet

Ouvrir canoniquement les seuls parents project/machine vraiment defensables apres merge de PR #181, sans runtime, sans suppression de branche, sans merge secondaire et sans lancer encore `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01`.

## Etat reel de depart

- `sot/mainline` porte maintenant PR #181 au commit `7b75154`.
- Le parent actif reste `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`.
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` est merge et clos comme etape de cartographie.
- La carte cible precedente ne prouvait pas une ouverture automatique des 5 candidats ; elle imposait encore un arbitrage repo-first contre les risques decoratifs.

## Role de ce GO

Ce GO ne cartographie plus. Il tranche l'ouverture effective, parent par parent, puis propage uniquement les ouvertures valides dans les surfaces canoniques de continuite.

## Decisions d'ouverture

- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` est ouvert maintenant.
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` est ouvert maintenant.
- `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` n'est pas ouvert comme nouveau parent ; le besoin est absorbe par l'existant `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`.
- `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` est differe.
- `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` est differe.

## Justification repo-first

- `admin-trading` et `db-layer` ont une preuve machine forte, repetee et deja raccordee a un role operatoire stable dans les surfaces `reseau_ssh`.
- `localcms` possede deja un parent canonique existant ; en ouvrir un deuxieme ici creerait un doublon decoratif.
- `student` reste a la frontiere entre lecture machine et famille `deepseek_student`, avec une verite runtime encore figee hors d'un parent machine autonome.
- `fantome` reste prouve comme machine joignable et migree, mais pas encore comme cible durable suffisante pour un parent support autonome.

## Anti-cibles

Ne pas faire :

- ouvrir les 5 parents par symetrie ;
- cloner `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` sous un nouveau nom ;
- transformer `student` en parent fourre-tout machine + famille ;
- ouvrir `fantome` sans preuve supplementaire de cible durable ;
- lancer `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` dans ce lot ;
- modifier `modules/`, `scripts/`, `registry/` ou `_archive/`.

## Conditions de passage au GO suivant

Le passage vers `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` ne devient admissible qu'apres :

1. creation du dossier chantier du present GO ;
2. creation du set d'ouverture minimal pour les parents effectivement ouverts ;
3. propagation coherente dans `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md` et `REPRISE.md` ;
4. confirmation explicite que `BRANCH_STATE.md` reste inchange ;
5. verification finale du diff doc-only.
