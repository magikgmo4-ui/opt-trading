---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01_CONFORMITY_MATRIX
doc_type: decision_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_conformity_audit
  - conformity_matrix
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/00_cadrage.md
point_de_reprise: "Tableau de conformite"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01/02_parent_opening_matrix.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md
---

# 01_conformity_matrix

| Parent / axe | Nommage canonique | Frontmatter noyau | Rattachement parent | Rattachement machine / produit / methode | Parent decoratif ? | Propagation continuite | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | oui | oui | oui, via `PARENT_OPENING_BATCH` sous `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | oui, machine `admin-trading` / produit `Desk Pro` / role operateur | non | oui apres patch des index | PASS |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | oui | oui | oui, via `PARENT_OPENING_BATCH` sous `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | oui, machine `db-layer` / produit `Desk Pro` / flux export-consultation-ingestion | non | oui apres patch des index | PASS |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` comme fusion `localcms` | oui | heritage historique, hors lot d'ouverture machine | oui, parent deja ouvert distinct du split machine | oui, methode producer-consumer UI | non | oui, a condition de ne pas cloner `GO_OPT_TRADING_PROJECT_LOCALCMS_CONSUMER_PARENT_01` | PASS |
| `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | cible seulement, non ouverte | non applicable | non ouverte par design | articulation machine / famille encore ambiguë | le risque decoratif reste evite par le report | oui, car absence d'ouverture conservee | PASS |
| `GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01` | cible seulement, non ouverte | non applicable | non ouverte par design | rattachement support durable insuffisant | le risque decoratif reste evite par le report | oui, car absence d'ouverture conservee | PASS |

## Lecture retenue

- `admin-trading` et `db-layer` passent l'audit de conformite ;
- `localcms` passe en tant qu'axe fusionne avec le parent UI existant ;
- `student` et `fantome` passent parce qu'ils restent explicitement differes et non ouverts ;
- aucun nouvel ecart structurel n'impose une modification de `BRANCH_STATE.md`.
