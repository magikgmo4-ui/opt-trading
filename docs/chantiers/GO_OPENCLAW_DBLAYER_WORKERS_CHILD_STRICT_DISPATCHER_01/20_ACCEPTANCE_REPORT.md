---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: PASS
closed_at: 2026-06-02
pr: "#1043"
---

# 20_ACCEPTANCE_REPORT — Dispatcher déterministe OpenClaw → strict_workers

## Verdict

```
STATUS = PASS
PR #1043 mergée sur sot/mainline
16/16 tests PASS
```

## Deliverables produits

| Fichier | Statut |
| --- | --- |
| `scripts/ai/workers/openclaw_strict_worker_dispatcher.py` | DONE |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_READONLY_01.json` | DONE |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_WRITEGATED_01.json` | DONE |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_REFUSED_01.json` | DONE |
| `tests/test_openclaw_strict_worker_dispatcher.py` | DONE — 16/16 PASS |
| `docs/chantiers/.../FILE_SCOPE.txt` | DONE |
| `docs/chantiers/.../00_INITIAL_PROJECT_DOC.md` | DONE |

## Faits établis

```
Routing table :
  WRITE_GATED  → runner_writegated.py  (--gate-approved requis)
  autres types → runner_readonly.py

Modes d'entrée : --packet / --packet-id / --packet-json
Bloquants permanents :
  task_type inconnu → REFUSED (exit 4)
  worker non VERIFIED → REFUSED (exit 4)
  WRITE_GATED sans gate → REFUSED (exit 4)
  git tree dirty → BLOCKED (exit 2, délégué au runner)

Output FORMAT 3 (dispatcher + status + runner_result + report_path + timestamps)
Temp files inline nettoyés via atexit
```

## Invariants respectés

```
✓ 0 LLM dans la boucle de dispatch
✓ WRITE_GATED bloqué sans --gate-approved
✓ --dry-run supporté partout
✓ Index globaux non modifiés
✓ Parent non fermé
✓ FILE_SCOPE.txt présent dès J1
✓ PR gated sur sot/mainline
```

## Gaps restants

```
GAP_2 — openclaw_operator_bridge ne connaît pas encore le dispatcher
         (schema.py action whitelist = ask|build|evaluate|review ; "dispatch" absent)
GAP_3 — intégration tmux openclaw-core.sh → dispatcher non câblée
```
