---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01_VALIDATION_MATRIX
doc_type: decision_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_target_map
  - validation
  - anti_decorative
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/01_parent_target_map.md
point_de_reprise: "Matrice de validation"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 02_validation_matrix

| Parent candidat | Preuve suffisante aujourd'hui ? | Rattachement produit ou methode | Support Git vise coherent ? | Risque decoratif principal | Condition avant opening batch |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` | oui, mais avec chevauchement de nommage | `Desk Pro` / methode producer-consumer UI | oui | dupliquer inutilement le parent `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | decider si l'existant est renomme, promu ou simplement reutilise comme parent cible sans clone |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | oui | `Desk Pro` / surface operateur machine | oui | absorber des chantiers UI, tmux et reseau sans frontiere claire | borner le parent a la machine, a ses interfaces et a son role operateur principal |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | oui | `Desk Pro` / export-consultation-ingestion | oui | melanger preuve machine, data pipeline et modules sans sequence | expliciter un intention parent compacte avant ouverture |
| `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | oui, mais articulation a clarifier | methode / `DeepSeek-student` / interfaces associees | oui | concurrence entre logique machine et famille fonctionnelle `deepseek_student` | trancher si le parent est machine-first ou famille-first avant ouverture |
| `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` | partiellement | support operatoire machine | oui | parent cree sans cible durable hors support `reseau_ssh` | prouver une cible de support durable ou retirer `fantome` de l'opening batch |

## Conditions de passage vers GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01

1. la liste des 5 parents est acceptee comme cible canonique provisoire ;
2. chaque parent a un rattachement principal explicite ;
3. chaque parent a un support Git vise documente ;
4. les risques decoratifs sont traites ou assumés explicitement ;
5. aucune ouverture n'est executee dans le present GO ;
6. `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md` et `REPRISE.md` refletent bien que l'on est au stade `PARENT_TARGET_MAP`.
