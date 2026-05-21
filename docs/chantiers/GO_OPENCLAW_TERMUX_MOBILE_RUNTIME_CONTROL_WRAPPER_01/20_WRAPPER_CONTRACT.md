---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_WRAPPER_CONTRACT
doc_type: contract
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
updated_at: 2026-05-21
---

# 20_WRAPPER_CONTRACT

## Proposed executable

```text
scripts/ai/workers/openclaw_mobile_control.py
```

## Command model

Conceptual CLI:

```text
python3 scripts/ai/workers/openclaw_mobile_control.py <action> --phase <phase_id> --job <job_id> --json
```

Allowed initial actions:

- `status`
- `list-jobs`
- `preflight`
- `run-dry`
- `evidence`

## Contract output schema

```json
{
  "ok": true,
  "action": "status",
  "phase": "PHASE_01",
  "job_id": null,
  "status": "PASS",
  "evidence_path": "reports/ai/mobile_control/...json",
  "blocked_reason": null,
  "safety": {
    "non_trading_only": true,
    "external_write": false,
    "signal_trading": false,
    "secret_access": false
  }
}
```

## Runtime dependencies

The wrapper may use existing repo assets only:

- git executable for read-only status/diff checks;
- gh executable for PR listing when available;
- existing scripts under `scripts/ai/workers/` and `scripts/ai/tests/`;
- `reports/ai/mobile_control/` for output;
- ledger writer when available;
- LocalCMS status sync script when available.

## Safety behavior

If an action is not mapped, the wrapper returns `BLOCKED_WITH_REASON` and does not attempt fallback execution.

If a dependency is unavailable, the wrapper returns `PRECHECK_PASS` or `BLOCKED_WITH_REASON` depending on whether the missing dependency is required for the selected action.

## Evidence behavior

Every run must produce a JSON report under:

```text
reports/ai/mobile_control/
```

Optional markdown summaries can be derived later. The first implementation should prefer JSON to keep the wrapper deterministic and easy to parse from Termux.

## Termux compatibility requirements

- no absolute machine-specific path assumption;
- resolve repo root from script location;
- plain stdout JSON mode;
- no interactive prompt required for read-only/dry-run actions;
- all failures produce a structured result instead of raw crash.
