---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01_PARENT_TARGET_MAP
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - parent_target_map
  - project_machine_split
  - target_parents
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/00_cadrage.md
point_de_reprise: "Tableau cible"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/09_step_08_resultats_inventaire_reel.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md
---

# 01_parent_target_map

## Carte cible candidate des 5 parents

| Parent candidat | Classe | Rattachement principal | Justification repo-first | Support Git vise | Risque decoratif |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` | `PROJECT` | produit `Desk Pro` / methode producer-consumer UI | `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` prouve deja une trajectoire `opt-trading` producer -> `localcms` consumer ; le besoin reste project-level et non machine-level | `go/GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` | moyen : ne pas dupliquer le parent `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` sans clarifier s'il s'agit d'une promotion/renormalisation ou d'une simple reutilisation |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `MACHINE` | produit `Desk Pro` / surface operateur | `admin-trading` revient comme machine distante cible dans `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` et comme machine migree PASS dans les surfaces `reseau_ssh` | `go/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | faible : machine explicitement prouvee, mais il faut eviter de melanger UI, SSH et runtime trading dans un meme parent trop large |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `MACHINE` | produit `Desk Pro` / chaines export-consultation-ingestion | `db-layer` est une machine recurrente dans les preuves `reseau_ssh`, et reste un pivot credible pour les flux producer -> consumer / ingestion | `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | faible : machine prouvee, risque principal = surcharger le parent avec des objectifs trop heterogenes |
| `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | `MACHINE` | methode / famille `DeepSeek-student` avec interfaces desk associees | `student` est prouve comme machine distincte dans les surfaces `reseau_ssh` et dans plusieurs traces `deepseek_student` ; la separation machine a du sens avant toute ouverture | `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | moyen : il faut arbitrer proprement l'articulation entre machine `student` et famille `deepseek_student` pour ne pas creer un parent fourre-tout |
| `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` | `SUPPORT` | methode / support operatoire machine | `fantome` est prouve comme machine migree PASS dans `reseau_ssh`, mais son rattachement produit reste moins fort que les autres ; `SUPPORT` est plus defendable que `PROJECT` | `go/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` | eleve : risque decoratif si aucune cible durable hors `reseau_ssh` / support operatoire n'est clarifiee avant ouverture |

## Lecture retenue

- `localcms` porte l'axe `PROJECT` le plus prouve actuellement ;
- `admin-trading`, `db-layer` et `student` sont les trois axes `MACHINE` les plus solides ;
- `fantome` reste dans la carte cible, mais avec la classification `SUPPORT` pour expliciter son statut plus fragile.

## Ce qui n'est pas encore une ouverture

Ce tableau n'ouvre aucun parent. Il fige seulement la cible future et le cadrage minimal a verifier avant `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`.

## RISKS

- À qualifier.
