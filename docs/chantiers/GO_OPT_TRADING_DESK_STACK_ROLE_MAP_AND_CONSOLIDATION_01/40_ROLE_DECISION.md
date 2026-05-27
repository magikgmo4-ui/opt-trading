---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_ROLE_DECISION
doc_type: role_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - roles
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md
---

# 40_ROLE_DECISION

## Verdict central

L'ensemble `desk*` / `desk_pro*` est une **stack complementaire**, pas une famille a survivant unique.

## Roles tranches

### Owner canonique

- **`desk_pro` = owner canonique documentaire de stack**

Pourquoi:

- coeur partage API/UI/service confirme par README
- consomme directement par `perf/perf_app.py`
- centralise modeles, services et montage FastAPI

### Facade operateur

- **`desk_pro_runner` = facade operateur canonique**

Pourquoi:

- wrapper live `cmd-desk_pro_runner`
- expose la routine operateur standard
- pilote orchestrateur et dashboard

### Execution backbone

- **`desk_pro_orchestrator` = backbone d'execution**

### Visualization

- **`desk_pro_dashboard` = surface dashboard / export**

### Shared support

- **`desk_common` = support shared minimal**

### Satellites adjacents

- **`desk_snapshot_ingest` = ingest amont**
- **`desk_capture_inputs` = extraction d'inputs**
- **`desk_state` = state canonique lateral**
- **`desk_retention` = retention/hygiene**
- **`desk_analyze` = analyse locale ad hoc**

## Ce qu'il ne faut pas conclure

- ne pas rabattre `desk_pro_runner` sur un simple alias de `desk_pro`
- ne pas traiter `desk_pro_dashboard` comme survivant concurrent de `desk_pro`
- ne pas fusionner d'emblee tous les `desk_*` dans `desk_pro`

## Consolidation posture

Decision retenue pour ce GO doc-only:

- conserver la stack comme complementaire
- expliciter un coeur `desk_pro*`
- classer les `desk_*` en satellites ou support
- deferer toute absorption physique a un GO separe

## Classement final

| Surface | Classement |
| --- | --- |
| `desk_pro` | owner canonique de stack |
| `desk_pro_runner` | facade operateur canonique |
| `desk_pro_orchestrator` | orchestrateur coeur |
| `desk_pro_dashboard` | surface dashboard complementaire |
| `desk_common` | support shared |
| `desk_snapshot_ingest` | satellite ingest |
| `desk_capture_inputs` | satellite extraction |
| `desk_state` | satellite state |
| `desk_retention` | satellite hygiene |
| `desk_analyze` | satellite analysis |

## Verdict

**PASS**

La stack Desk est clarifiee sans mutation runtime.
