---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_TEST_AND_EVIDENCE_PLAN
doc_type: test_plan
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
updated_at: 2026-05-21
---

# 40_TEST_AND_EVIDENCE_PLAN

## Test objective

Prove that the mobile-control wrapper can run safely in non-trading local/read-only mode and emit deterministic evidence.

## Test matrix

| Test | Expected |
|---|---|
| import / syntax | PASS |
| status action | PASS JSON |
| list-jobs Phase 01 | returns allowed jobs |
| preflight known job | PASS or PRECHECK_PASS |
| preflight unknown job | BLOCKED_WITH_REASON |
| run-dry read-only job | PASS + evidence |
| run-dry forbidden job | BLOCKED_WITH_REASON |
| evidence lookup | returns report path or blocked reason |

## Required evidence

- JSON report under `reports/ai/mobile_control/`;
- stdout JSON for Termux parsing;
- safety object in every result;
- no external writes;
- no signal/trading fields;
- no secret values.

## Acceptance criteria

```text
PASS:
- all allowed Phase 01 read-only/local-only actions execute or preflight cleanly
- all forbidden or unknown actions block cleanly
- evidence files are created only under reports/ai/mobile_control
- no runtime daemon or scheduler is installed
```

## Regression guard

Any future expansion beyond Phase 01 must add explicit tests and update the action matrix before implementation.
