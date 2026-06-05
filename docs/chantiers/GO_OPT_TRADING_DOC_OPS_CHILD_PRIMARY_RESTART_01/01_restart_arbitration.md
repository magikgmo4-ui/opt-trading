---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01_RESTART_ARBITRATION
doc_type: decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - primary_restart
  - arbitration
  - p0
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/00_cadrage.md
point_de_reprise: "Decision retenue"
updated_at: 2026-04-29
links:
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
---

# 01_restart_arbitration

## Matrice P0

| Flux P0 lu | Etat lu | Rapport au redemarrage operatoire unique | Decision |
| --- | --- | --- | --- |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` sous `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | Suite explicite de la sequence parent apres PR #179 | Flux de reprise directement rattache a la chaine `BRANCH_CLEANUP` -> `OPEN_WORK_CONTROL` -> `CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL` ; prerequisite avant `PARENT_TARGET_MAP` | retenu |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | P0 actif, mais sans nouveau GO enfant a ouvrir ici | Parent de maintenance d'index deja ouvert ; ne remplace pas la reprise ordonnee du parent project/machine split | reporte |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | P0 actif, avec GO suivant explicite | Flux machine/outillage distinct, sans priorite canonique sur la chaine doc-ops du parent de reprise | reporte |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | P0 actif, sans nouveau GO enfant a ouvrir ici | Audit documentaire ouvert mais hors sequence directe du parent project/machine split | reporte |

## Decision retenue

Le flux unique retenu maintenant est :

`GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`

## Justification repo-first

- `GO_INDEX.md` et `ACTIVE_STREAMS.md` confirment que le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` reste P0 et ouvert ;
- `02_go_map.md` fixe une sequence canonique explicite ou `PRIMARY_RESTART` vient avant `PARENT_TARGET_MAP` ;
- `90_closeout.md` et `02_next_flow_arbitration.md` du GO precedent ont deja acte que `PRIMARY_RESTART` est la suite naturelle apres PASS ;
- PR #179 a merge ce PASS sur `sot/mainline`, ce qui leve le dernier blocage de continuite specifique a cette chaine ;
- aucun autre P0 n'impose un redemarrage prioritaire de cette meme sequence parent.

## Ce qui n'est pas retenu maintenant

- aucun basculement immediat vers `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` ;
- aucune ouverture du `PARENT_OPENING_BATCH` ;
- aucune ouverture des 5 parents project/machine ;
- aucune reouverture des lots fermes en amont.

## RISKS

- À qualifier.
