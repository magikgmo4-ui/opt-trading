---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
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
  - runtime
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Carte runtime observee

```text
SFTP / inbox captures
  -> desk_snapshot_ingest
  -> /opt/trading/desk/snapshots/latest.json
  -> desk_capture_inputs
  -> /opt/trading/desk/inputs/tv_inputs_latest.json
  -> desk_state
  -> /opt/trading/desk/state/latest.json

operator / cron / admin wrapper
  -> desk_pro_runner
  -> desk_pro_orchestrator
  -> data/desk_runs/*
  -> desk_pro_dashboard

host FastAPI (perf/perf_app.py)
  -> desk_pro.mount
  -> /desk/* API + UI

retention / hygiene
  -> desk_retention

snapshot-side analysis
  -> desk_analyze
```

## Role map retenu

| Role | Module | Classement |
| --- | --- | --- |
| owner canonique de stack | `desk_pro` | coeur partage |
| facade operateur canonique | `desk_pro_runner` | entrypoint CLI |
| execution backbone | `desk_pro_orchestrator` | coeur execution |
| visualization / export | `desk_pro_dashboard` | surface complementaire |
| shared support | `desk_common` | support minimal |
| ingest | `desk_snapshot_ingest` | satellite amont |
| input extraction | `desk_capture_inputs` | satellite amont |
| canonical state | `desk_state` | satellite state |
| retention | `desk_retention` | satellite hygiene |
| local analysis | `desk_analyze` | satellite analyse |

## Main stack interpretation

L'ensemble se lit en deux couches :

1. coeur Desk Pro
   - `desk_pro`
   - `desk_pro_runner`
   - `desk_pro_orchestrator`
   - `desk_pro_dashboard`

2. satellites Desk adjacents
   - `desk_common`
   - `desk_snapshot_ingest`
   - `desk_capture_inputs`
   - `desk_state`
   - `desk_retention`
   - `desk_analyze`

## Tension structurelle restante

La principale ambiguite restante n'est pas un survivant multiple.

C'est une frontiere de packaging :

- certaines surfaces historiquement separees (`desk_pro_dashboard`, possiblement `desk_snapshot_ingest`) pourraient etre absorbables dans `desk_pro`
- mais la stack actuelle est coherentement exploitable sans move physique immediate
