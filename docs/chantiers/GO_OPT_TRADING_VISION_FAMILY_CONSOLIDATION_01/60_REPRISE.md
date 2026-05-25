---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - modules
  - vision
  - reprise
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md
---

# 60_REPRISE

## Resume executif

- famille analysee sans mutation runtime
- owner canonique retenu: `vision_bot`
- composant operatoire complementaire retenu: `bot_vision_step2`
- legacy preserve retenu: `bot_vision`
- noeud ambigu restant: `modules/bot_vision/headless_capture/`

## Fichiers crees

- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/60_REPRISE.md`

## Diff summary

- fixe la lecture de famille `vision` comme stack complementaire, pas comme simple lignee step-by-step
- explicite les callers non-documentaires et les surfaces runtime utiles
- distingue survivant documentaire, composant complementaire et legacy preserve
- prepare une suite registry separee sans modifier la registry dans ce lot

## Commandes utiles de verification

```bash
rg -n "vision_bot|bot_vision_step2|bot_vision" docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
rg -n "module_name: vision_bot" registry/modules_registry.yaml
rg -n "bot_vision_step2.service|vision_bot.service|bot-vision-headless-capture.service" modules config scripts deploy
```

## Resultats attendus

- le dossier chantier contient les 7 livrables attendus
- la decision `vision_bot owner canonique / bot_vision_step2 composant complementaire / bot_vision legacy preserve` est explicite
- aucune mutation runtime ni registry n'apparait dans le diff

## Rollback

1. supprimer le dossier `docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/`
2. verifier que le worktree ne contient plus que les changements voulus hors lot

## Next GO recommandes

1. `GO_OPT_TRADING_VISION_FAMILY_REGISTRY_REALIGNMENT_01`
2. `GO_OPT_TRADING_VISION_HEADLESS_PHYSICAL_EXTRACTION_01`

## Objet du GO physique/runtime ensuite

Le GO physique/runtime a preparer ensuite doit traiter uniquement le noeud restant :

- sortir `headless_capture` du root legacy `modules/bot_vision/`, ou
- le rattacher explicitement a une surface survivante sans casser les timers/services existants

Ce GO devra rester distinct du present lot doc-only.
