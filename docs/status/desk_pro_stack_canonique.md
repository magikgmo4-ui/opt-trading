---
doc_id: OPT_TRADING_STATUS_DESK_PRO_STACK_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - status
  - desk_pro
  - module_family
  - continuity
search_tags:
  - surface:module_family
  - doc_role:carte
  - product:desk_pro
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/ot/project_cards/PROJECT_CARD_DESKPRO_01.md
---

# DESK_PRO_STACK — STATUT CANONIQUE

## Role documentaire

- role_actuel: fiche courte de statut de stack pour `desk_pro*` et surfaces adjacentes
- role_cible: fiche annexe de consolidation de lignee, non souveraine
- souverainete: ne remplace ni la synthese produit Desk Pro, ni les runbooks, ni les decisions de structure
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et la synthese Desk Pro avant d'utiliser cette fiche pour lire les frontieres de stack et de transition

## Objet
Fiche courte de lignée/stack pour `desk_pro*` et `desk_*`.

## ETABLI
- `desk_pro*` est une stack à cartographier (pas un doublon simple)
- `desk_*` hors `desk_pro*` forme un sous-système adjacent à frontière encore à préciser
- `desk_pro` confirmé comme centre de gravité partagé API / UI / service
- `desk_pro_runner` confirmé comme façade opératoire module
- `desk_pro_orchestrator` confirmé comme pipeline d'exécution
- `desk_pro_dashboard` confirmé comme surface de visualisation / export
- `desk_common` confirmé comme support partagé minimal
- runtime admin réel confirmé hors `modules/` via `scripts/admin_trading/desk_pro_cmd.sh`
- `desk_snapshot_ingest`, `desk_capture_inputs`, `desk_analyze`, `desk_state`, `desk_retention` confirmés comme satellites adjacents

## Survivant / Transition / Legacy / Archive
- survivant : stack multi-composants ; pas de survivant unique
- transition : consolidation documentaire des rôles par composant
- legacy : pas de module legacy figé dans ce lot ; les wrappers legacy restent hors `modules/`
- archive : non figé dans ce lot

## Liens de preuve
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`
- `docs/desk_pro_multi_machine_map.md`
- `docs/ot/trae/OT_DESKPRO_MACHINE_PACK_WRAPPERS_REGISTRY_DECISION_01.md`

## Reprise
- reprise immédiate documentée dans `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`
- basculer ensuite en cartographie `Step 04` pour détailler les frontières P1 de la stack

## RISKS

- À qualifier.
