---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01_OPENING_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - doc_ops
  - parent_opening_batch
  - opening_plan
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
point_de_reprise: "Section Plan retenu"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/02_parent_opening_matrix.md
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
---

# 01_opening_plan

## Plan retenu

1. Clore implicitement la phase `PARENT_TARGET_MAP` comme phase de lecture et non d'ouverture.
2. Reutiliser `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` pour l'axe `localcms`, sans ouvrir de clone project.
3. Ouvrir `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` avec un set minimal stable.
4. Ouvrir `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` avec un set minimal stable.
5. Differer `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` tant que la frontiere machine / famille n'est pas stabilisee.
6. Differer `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` tant qu'un usage support durable n'est pas mieux prouve.
7. Propager ces decisions dans les surfaces de continuite sans toucher `BRANCH_STATE.md`.

## Ouvertures validees maintenant

### GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01

- type : `MACHINE`
- rattachement principal : `Desk Pro` / machine operateur
- support Git cible : `go/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- preuve d'ouverture : machine cible repetee dans les surfaces `reseau_ssh` et `tmux-ide`

### GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01

- type : `MACHINE`
- rattachement principal : `Desk Pro` / export-consultation-ingestion
- support Git cible : `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`
- preuve d'ouverture : machine stable recurrente dans les surfaces `reseau_ssh`

## Ouvertures non retenues maintenant

### LocalCMS

- candidat carte cible : `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01`
- decision : fusionner avec l'existant `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
- raison : pas de besoin repo-first suffisant pour cloner un parent deja ouvert sur le meme axe producer-consumer

### Student

- candidat carte cible : `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01`
- decision : differe
- raison : la lecture machine existe, mais la famille `deepseek_student` garde une verite runtime distincte qui rend l'ouverture autonome prematuree

### Fantome

- candidat carte cible : `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01`
- decision : differe
- raison : preuve machine partielle seulement sur l'axe support / `reseau_ssh`, avec risque decoratif encore trop fort

## Frontiere de ce GO

- aucune branche parent dediee n'est creee dans ce lot ;
- `BRANCH_STATE.md` ne bouge pas ;
- aucun enfant nouveau n'est ouvert sous les parents admin-trading et db-layer dans ce passage ;
- le prochain GO logique reste `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01`, mais il n'est pas lance ici.
