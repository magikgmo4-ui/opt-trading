---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_STEP_07_NOTE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - step-07
  - arbitrage
  - enfants
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/97_step_06_verification_zones_grises.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
---

# Step 07 — arbitrage enfants eventuels

## Statut
Complete.

## Objet
Decider si la profondeur atteinte dans le parent impose l'ouverture d'un chantier enfant supplementaire.

## Analyse
- `packages/` est suffisamment qualifie comme surface top-level de code mutualisable
- `tests/` est suffisamment qualifie comme surface top-level faible et non structurante
- `student/`, `data/` et `audit/` ont maintenant des frontieres lisibles
- le seul ecart detecte est documentaire : certaines docs `student/validation` pointent vers des fichiers `audit/2026-03-20/*.md` non presents en clair

## Decision
- aucun enfant n'est ouvert a ce stade
- le parent couvre deja le besoin de cartographie repo-level
- l'ecart `audit/` releve d'une hygiene documentaire ciblee, pas d'un lot enfant de synthese

## Consequence
- ne pas ouvrir `modules/`, `scripts/` ou `student/data/audit` en enfant tant qu'un besoin de profondeur supplementaire n'est pas prouve
- si un lot est ouvert ensuite, il doit cibler un probleme concret d'hygiene ou de reference, pas une cartographie generale deja couverte

## Fichiers modifies
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md`

## Rollback
- revert doc-only de `94_plan_execution_step_by_step.md`
- suppression de cette note si le step est annule

## Point de reprise
Passer a `Step 08` pour arbitrer le closeout du parent ou son maintien ouvert jusqu'au traitement de l'hygiene documentaire restante sur `audit/`.
