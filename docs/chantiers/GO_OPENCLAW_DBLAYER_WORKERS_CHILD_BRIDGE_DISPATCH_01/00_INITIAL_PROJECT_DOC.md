---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: open
created_at: 2026-06-02
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01

## 1_MASTER_TARGET

Câbler `openclaw_operator_bridge` → `openclaw_strict_worker_dispatcher`.
L'action `"dispatch"` dans `BridgeRequest` route vers le dispatcher déterministe
sans passer par le builder agent LLM.

## 2_CHANGEMENTS

| Fichier | Modification |
| --- | --- |
| `schema.py` | `"dispatch"` ajouté à `ALLOWED_ACTIONS` |
| `client.py` | `call_dispatcher()` ajouté — appelle le dispatcher via subprocess |
| `bridge.py` | route `action == "dispatch"` vers `call_dispatcher()` |
| `test_bridge_mock.py` | 8 nouveaux tests dispatch (mock) |

## 12_INVARIANTS

```text
- Pas de LLM dans le dispatch
- dry_run=True par défaut si non spécifié
- gate_approved=False par défaut
- packet_id / packet_path / packet_json dans parameters (mutuellement exclusifs)
- BridgeError si aucun paramètre packet fourni
```
