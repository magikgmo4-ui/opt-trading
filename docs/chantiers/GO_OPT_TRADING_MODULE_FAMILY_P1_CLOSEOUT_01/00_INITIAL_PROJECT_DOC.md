---
doc_id: GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01_INITIAL_PROJECT_DOC
doc_type: chantier_closeout
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01
status: draft_for_review
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - modules
  - family
  - p1
  - closeout
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/100_GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_FINAL.md
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
---

# 00_INITIAL_PROJECT_DOC

## Objet

Clore la phase P1 directe du master plan de consolidation des familles de modules fractionnees.

Perimetre de closeout:

- `reseau_ssh`
- `vision`
- `perf`
- `journal`

## Etat etabli en entree

- `reseau_ssh` : salvage documentaire merge via PR #752, puis canonisation famille `ONE_MODULE`
- `vision` : `PASS`, commit local `11e569f4`
- `perf` : `PASS`, commit local `87fc8366`
- `journal` : `PASS`, commit local `5e431c8b`
- baseline de travail : `CURRENT_BASELINE_2026_05_20 = 98`
- `secrets/` non suivi, hors perimetre

## But du lot

1. formaliser que P1 directe est terminee
2. resumer les decisions survivant/legacy/compat deja prises
3. isoler les gaps registry encore ouverts
4. transmettre vers P2 sans rouvrir l'audit global

## Invariants appliques

- mode `doc-only`
- aucune mutation runtime
- aucune mutation registry
- aucun index global ajoute
- aucun toucher a `secrets/`

## Verdict attendu

`PASS`
