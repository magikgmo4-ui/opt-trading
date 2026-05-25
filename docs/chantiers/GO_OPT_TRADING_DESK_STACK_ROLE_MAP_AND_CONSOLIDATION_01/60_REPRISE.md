---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - reprise
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/40_ROLE_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md
---

# 60_REPRISE

## Resume executif

- la stack `desk*` / `desk_pro*` n'est pas une famille a survivant unique
- `desk_pro` est retenu comme owner canonique de stack
- `desk_pro_runner` est retenu comme facade operateur canonique
- `desk_pro_orchestrator` et `desk_pro_dashboard` restent des sous-composants coeurs complementaires
- les `desk_*` restants sont classes comme satellites ou support

## Fichiers crees

- `docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md`
- `10_STACK_INVENTORY.md`
- `20_CALLERS_AUDIT.md`
- `30_RUNTIME_SURFACE_MAP.md`
- `40_ROLE_DECISION.md`
- `50_REGISTRY_ACTIONS.md`
- `60_REPRISE.md`

## Diff summary

- clarifie l'ensemble Desk comme stack complementaire
- fixe `desk_pro` comme owner canonique et `desk_pro_runner` comme facade operateur
- classe `desk_pro_orchestrator`, `desk_pro_dashboard`, `desk_common` et les `desk_*` satellites
- prepare un realignement registry distinct sans mutation dans ce lot

## Commandes utiles de verification

```bash
rg -n "desk_pro|desk_pro_runner|desk_pro_orchestrator|desk_pro_dashboard|desk_snapshot_ingest|desk_common" docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
rg -n "module_name: (desk_pro|desk_pro_runner|desk_pro_orchestrator|desk_pro_dashboard|desk_common|desk_snapshot_ingest|desk_state)" registry/modules_registry.yaml
git status --short --branch
```

## Resultats attendus

- le dossier chantier contient les 7 livrables attendus
- la stack est explicitement classee complementaire, pas fusionnee a l'aveugle
- `desk_pro` est explicite comme owner canonique
- aucune mutation runtime ni registry n'apparait dans le diff

## Rollback

1. supprimer `docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/`
2. verifier le worktree restant avant toute autre action

## Next GO recommandes

1. `GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01`
2. `GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01`
3. `GO_OPT_TRADING_DESK_STACK_PHYSICAL_ABSORPTION_CADRAGE_01`

## Verdict

`PASS`
