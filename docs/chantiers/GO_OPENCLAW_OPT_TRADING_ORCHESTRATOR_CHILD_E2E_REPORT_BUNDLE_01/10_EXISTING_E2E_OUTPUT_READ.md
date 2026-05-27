---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_READ
doc_type: existing_output_read
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
status: DONE
created_at: 2026-05-26
---

# 10_EXISTING_E2E_OUTPUT_READ

## Sortie pipeline lue

`scripts/e2e/dry_run_pipeline.py` produit un dict JSON avec les champs :

```json
{
  "pipeline_name": "E2E post-gate live/dry-run",
  "dry_run": true,
  "started_at": "...",
  "completed_at": "...",
  "duration_s": 5.0,
  "steps": [
    {"step": "1_signal_router", "result": {...}},
    {"step": "2_proposition_engine", "result": {...}},
    {"step": "3_validation_gate", "result": {...}},
    {"step": "4_trade_executor", "result": {...}},
    {"step": "5_result_tracker", "result": {...}},
    {"step": "6_datasheet_writer", "result": {...}},
    {"step": "7_learning_feeder", "result": {...}}
  ],
  "e2e_post_gate_status": {
    "status": "PASS",
    "dry_run": true,
    "live_trade": false,
    "gate_status": "APPROVED_PAPER",
    "localcms_gate": "WARN_SKIPPED",
    "sheets_mode": "fake",
    "telegram_mode": "dry_run",
    "modules": { ... }
  }
}
```

## Champs bundle-eligibles

- `e2e_post_gate_status.gate_status == "APPROVED_PAPER"` — condition d'acceptation
- `e2e_post_gate_status.live_trade == false` — invariant de sécurité
- `dry_run == true` — invariant de sécurité
- `steps[]` — source pour `payload_refs.json`
