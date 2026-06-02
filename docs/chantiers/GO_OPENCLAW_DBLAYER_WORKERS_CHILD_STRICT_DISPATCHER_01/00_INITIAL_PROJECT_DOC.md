---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: open
created_at: 2026-06-01
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01

## 1_MASTER_TARGET

Implémenter un dispatcher déterministe entre OpenClaw operator bridge et les strict workers.

OpenClaw reçoit ou résout un `job_packet`, route vers le bon runner strict worker,
retourne un JSON structuré FORMAT 3. Aucun LLM dans la boucle de dispatch.

## 2_DECISION_VALIDEE

```text
dispatch      = RULE_BASED_FROM_JOB_PACKET
selector_llm  = NON
routing_llm   = NON
auditability  = MAX

WRITE_GATED task_type → runner_writegated.py (--gate-approved requis)
Tous les autres       → runner_readonly.py
task_type inconnu     → REFUSED
worker inconnu        → REFUSED
```

## 3_DELIVERABLES

| Fichier | Rôle |
| --- | --- |
| `scripts/ai/workers/openclaw_strict_worker_dispatcher.py` | Dispatcher principal |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_READONLY_01.json` | Fixture read-only |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_WRITEGATED_01.json` | Fixture write-gated |
| `scripts/ai/workers/job_packets/DISPATCHER_SMOKE_REFUSED_01.json` | Fixture task_type inconnu |
| `tests/test_openclaw_strict_worker_dispatcher.py` | Tests unitaires dry-run |

## 12_INVARIANTS

```text
- Pas de LLM dans le dispatch
- WRITE_GATED bloqué sans --gate-approved
- --dry-run toujours supporté
- task_type inconnu → REFUSED (exit 4)
- worker inconnu → REFUSED (exit 4)
- 0 modification des index globaux
- Parent non fermé
```
