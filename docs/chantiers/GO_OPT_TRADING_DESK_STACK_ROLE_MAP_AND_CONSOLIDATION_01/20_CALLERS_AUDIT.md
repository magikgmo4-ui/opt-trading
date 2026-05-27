---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_CALLERS_AUDIT
doc_type: callers_audit
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
  - callers
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/10_STACK_INVENTORY.md
---

# 20_CALLERS_AUDIT

## Callers coeur `desk_pro*`

| Module | Callers constates | Lecture |
| --- | --- | --- |
| `desk_pro` | `perf/perf_app.py` via `modules.desk_pro.api.routes` et `modules.desk_pro.mount`; tests `modules.desk_pro.*` | coeur partage reellement consomme |
| `desk_pro_runner` | `cmd-desk_pro_runner`, `menu-ops_menu_hub`, docs ops, wrappers registry | facade operateur live |
| `desk_pro_orchestrator` | `desk_pro_runner` via `ORCHESTRATOR_MOD`, docs runtime state | backbone sous le runner |
| `desk_pro_dashboard` | `desk_pro_runner` via `DASHBOARD_MOD`, wrappers `cmd-desk_pro_dashboard`, ui registry | visualisation complementaire exposee |

## Callers satellites `desk_*`

| Module | Callers constates | Lecture |
| --- | --- | --- |
| `desk_snapshot_ingest` | `scripts/desk_bridge/bridge_vision_to_desk_inbox.sh`, `cmd-desk_snapshot_ingest`, ui registry | satellite amont reel |
| `desk_analyze` | `cmd-desk_analyze`, `menu-ops_menu_hub`, docs ops | satellite analyse expose |
| `desk_state` | `cmd-desk_state`, ui registry, docs ops | satellite state expose |
| `desk_retention` | service/timer, docs live, OT live report | satellite hygiene actif |
| `desk_capture_inputs` | wrappers module + docs stack | satellite extraction present |
| `desk_common` | references documentaires et support de chemins partages | module support, peu de callers explicites |

## Observations registry/modules

- `desk_pro_dashboard`, `desk_pro_runner`, `desk_capture_inputs`, `desk_analyze`, `desk_state`, `desk_snapshot_ingest`, `desk_retention` sont deja presents en `modules_registry.yaml`
- `desk_pro`, `desk_pro_orchestrator` et `desk_common` sont absents de la registry modules

## Observations wrappers

- `cmd-desk_pro_runner` et `cmd-desk_pro_dashboard` sont portes par `wrappers_registry.yaml`
- `cmd-desk_snapshot_ingest` et `desk_retention` restent documentes comme wrappers live mais la couverture wrappers n'est pas complete partout

## Lecture structurante

Les callers ne montrent pas un schema de doublon concurrent.

Ils montrent un graphe de roles:

- `desk_pro` est consomme comme librairie/service partage
- `desk_pro_runner` est consomme comme entrypoint operateur
- `desk_pro_orchestrator` et `desk_pro_dashboard` sont consommes comme sous-composants du runner
- `desk_*` servent d'amont, de support ou d'outillage lateral
