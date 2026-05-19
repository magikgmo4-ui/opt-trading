# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01 -- 02_RECONCILIATION_DECISIONS

## 1_MASTER_TARGET

Record the applied decisions for the 4 inline/index fixture warning reconciliations.

## 2_INITIAL_PROJECT_DOC

Decisions are based on the canonical fixture index and the pre-change harness reproduction.

## 3_INITIAL_NEED

The correction must be auditable and must prove that semantics and expected outcomes were not changed beyond metadata alignment.

## 4_MASTER_PROJECT_PLAN

For each warning, record the applied decision, justification, file modified, semantic impact, expected verdict impact, and residual risk.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01`

## 7_CANONICAL_STATE

Source of truth remains:

```text
09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md
```

## 8_VALIDATED_PLAN

| fixture_id | Applied decision | Justification | File modified | Semantics changed? | Expected verdict changed? | Residual risk |
|---|---|---|---|---|---|---|
| `FAIL_SECRET_READ_APPROVABLE_01` | Changed inline `expected_verdict` from `FAIL_POLICY` to `FAIL_NEVER_ALLOWED_APPROVAL_PATH`. | Index and actual validator outcome agree on the more specific never-allowed verdict. | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | no | no index change | none observed |
| `FAIL_CREDENTIAL_EXPORT_APPROVABLE_01` | Changed inline `expected_verdict` from `FAIL_POLICY` to `FAIL_NEVER_ALLOWED_APPROVAL_PATH`. | Index and actual validator outcome agree on the more specific never-allowed verdict. | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | no | no index change | none observed |
| `FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01` | Changed inline `expected_error_code` from `ERR_TRACE_FAMILY_UNKNOWN` to `ERR_TRACE_REQUIRED_MISSING`. | The harness materializer creates the missing required trace condition and actual validator outcome matches the index. | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | no | no index change | none observed |
| `FAIL_WORKER_NO_VERDICT_01` | Changed inline `expected_verdict` from `FAIL_POLICY` to `NEED_MORE_EVIDENCE`. | Index and actual validator outcome agree that missing worker verdict is an evidence gap. | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | no | no index change | none observed |

## 9_SELECTED_SOLUTION

No validator code, harness code, tests, canonical index rows, fixture snippets, gates, traces, or evals were changed.

## 12_INVARIANTS

- Metadata-only fixture correction.
- Fixture snippets unchanged.
- Canonical index unchanged.
- Validator unchanged.
- Harness unchanged.
- Test files unchanged.
- No active workflow.
- No runtime.

## 13_ESTABLISHED

The correction aligns inline metadata to the already-canonical expected outcomes.

## 14_HYPOTHESIS

Because no policy snippet changed, the validator outcomes should remain identical while harness warnings drop from 4 to 0.

## 15_REMAINING_GAP

CI activation still requires a separate gate and human approval.

## 16_TODO

Verify with:

```text
python -m pytest tests/test_openclaw_mcp_policy_validator.py -q
python -m pytest tests/test_openclaw_mcp_policy_fixture_harness.py -q
python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
git diff --check
```

## 17_RESUME_POINT

After these decisions, warnings should no longer block CI activation review.

## 18_TO_DOCUMENT

Closeout must state `warnings before=4` and `warnings after=0`.

## 19_TO_REMEMBER

The correction does not approve CI activation; it only removes the warning blocker.
