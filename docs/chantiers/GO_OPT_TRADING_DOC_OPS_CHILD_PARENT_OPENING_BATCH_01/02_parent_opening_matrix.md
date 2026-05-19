---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01_OPENING_MATRIX
doc_type: decision_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - parent_opening_batch
  - opening_matrix
  - anti_decorative
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/00_cadrage.md
point_de_reprise: "Tableau de decision"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/01_opening_plan.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/02_validation_matrix.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/14_step_04_role_map_deepseek_student.md
---

# 02_parent_opening_matrix

| Parent candidat | Statut retenu | Raison courte | Ecriture creee ? | Support Git retenu | Commentaire |
| --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` | fusionne / non ouvert | axe deja couvert par `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | non | aucun nouveau support | evite un doublon decoratif project vs UI tant qu'aucune promotion canonique distincte n'est prouvee |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | ouvert maintenant | preuve machine et role operateur suffisamment stables | oui | `go/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | parent borne a la machine et a ses interfaces, sans absorber tout `reseau_ssh` |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | ouvert maintenant | preuve machine forte et usage recurrent de pivot data | oui | `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | parent borne a la machine `db-layer` et a ses flux d'interface |
| `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | differe | articulation machine / famille `deepseek_student` encore trop ambigue | non | `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` cible seulement | ouverture differee pour ne pas geler une frontiere fausse |
| `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` | differe | cible support durable insuffisamment prouvee | non | `go/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` cible seulement | maintien hors opening batch pour eviter un parent support decoratif |

## Lecture retenue

- le lot ouvre deux parents machine et rien de plus ;
- `localcms` est traite par reutilisation du parent deja existant ;
- `student` et `fantome` restent dans la carte cible future, mais pas dans l'ouverture canonique presente.

## Impact sur les surfaces canoniques

- `GO_INDEX.md` doit lister le present GO enfant et les deux nouveaux parents ouverts ;
- `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md` et `REPRISE.md` doivent montrer que `PARENT_OPENING_BATCH` est le sous-GO actif du parent split ;
- `BRANCH_STATE.md` reste intact car aucune branche parent distincte n'est creee ni representee dans ce passage.
