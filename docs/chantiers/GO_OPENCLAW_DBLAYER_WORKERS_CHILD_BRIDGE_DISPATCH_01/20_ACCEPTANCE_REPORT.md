---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: PASS
closed_at: 2026-06-02
---

# 20_ACCEPTANCE_REPORT — Bridge dispatch câblé

## Verdict

```
STATUS = PASS
18/18 tests PASS (10 existants + 8 nouveaux dispatch)
```

## Faits établis

```
BridgeRequest(action="dispatch", parameters={
  "packet_id": "...",   # OU packet_path OU packet_json
  "dry_run": True,      # défaut True
  "gate_approved": False
})
→ OperatorBridge.send()
→ call_dispatcher()
→ subprocess: python3 scripts/ai/workers/openclaw_strict_worker_dispatcher.py
→ BridgeResponse(status="ok"|"error", content=dispatch_status, structured=FORMAT_3)

BridgeError si packet manquant dans parameters.
```

## Invariants respectés

```
✓ Pas de LLM dans le dispatch
✓ dry_run=True par défaut
✓ gate_approved=False par défaut
✓ Tests mock — pas de gateway requis
✓ Index globaux non modifiés
✓ Parent non fermé
```
