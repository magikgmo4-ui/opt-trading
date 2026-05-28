---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - automation_ops
  - architecture
  - flow_map
  - human_gates
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01/10_ARCHITECTURE_REFACTOR_SCOPE.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/10_ARCHITECTURE_SURFACES.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/20_FLOW_MAP.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/30_HUMAN_AGENT_GATES.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/40_GAPS_AND_NEXT_GO.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cartographier l'architecture réelle des flux automation/jobs/semi-auto sans modifier les jobs ni workflows.

## 6_FINAL_TARGET

Carte d'architecture complète : surfaces, flux, gates humains, gaps identifiés.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Méthode | lecture code + grep + inspection — aucune mutation |
| Surfaces auditées | GHA (7), AI workers (30 job_packets + 26 scripts), OpenClaw, FastAPI, Desk Pro, Fleet |
| Mutation code | aucune |
| Verdict | PASS_ARCHITECTURE_MAP_READY |
