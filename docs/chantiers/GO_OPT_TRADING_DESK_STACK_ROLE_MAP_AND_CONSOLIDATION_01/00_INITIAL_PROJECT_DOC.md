---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - stack
  - consolidation
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01/30_P2_HANDOFF.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - docs/product/guides/DESK_PRO.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Cartographier la stack `desk*` / `desk_pro*` pour trancher si l'ensemble releve :

- d'une stack complementaire stable ;
- d'une famille devant etre fusionnee partiellement ;
- d'un noyau `desk_pro` entoure de facades et satellites specialises.

## Perimetre cible

- `desk_analyze`
- `desk_capture_inputs`
- `desk_common`
- `desk_retention`
- `desk_snapshot_ingest`
- `desk_state`
- `desk_pro`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`

## Etat d'entree

- P1 directe est closee et mergee
- base de lecture: `sot/mainline` a jour apres merge PR #772
- baseline de travail: `CURRENT_BASELINE_2026_05_20 = 98`
- `secrets/` reste hors perimetre

## Questions a trancher

1. S'agit-il d'une famille a fusionner ou d'une stack complementaire ?
2. Quel module porte l'owner canonique ?
3. Quel module porte la facade operateur ?
4. Quel module porte l'orchestration ?
5. Quel module porte la visualisation/dashboard ?
6. Quels modules `desk_*` restent coeurs, satellites ou supports shared ?
7. Quelle action registry sera requise ensuite ?
8. Quel GO physique/runtime devra suivre ?

## Contraintes appliquees

- mode `doc-only`
- aucun runtime
- aucune suppression
- aucune mutation registry
- aucun index global ajoute
- aucun toucher a `secrets/`
- machine_owner: `admin-trading`
