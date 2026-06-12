# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01 -- 01_WARNING_INVENTORY

## 1_MASTER_TARGET

Inventory the 4 fixture harness inline/index warnings.

## 2_INITIAL_PROJECT_DOC

Canonical index:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md
```

## 3_INITIAL_NEED

CI activation review needs the warning set to be explicit and reconciled.

## 4_MASTER_PROJECT_PLAN

List each warning with fixture id, file, inline field, inline value, canonical index value, risk, and proposed decision.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01`

## 7_CANONICAL_STATE

Pre-change harness warnings:

```text
FAIL_CREDENTIAL_EXPORT_APPROVABLE_01: inline expected_verdict differs from fixture index
FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01: inline expected_error_code differs from fixture index
FAIL_SECRET_READ_APPROVABLE_01: inline expected_verdict differs from fixture index
FAIL_WORKER_NO_VERDICT_01: inline expected_verdict differs from fixture index
```

## 8_VALIDATED_PLAN

| warning_id | fixture_id | file | inline_field | inline_value | canonical_index_value | risk | proposed decision |
|---|---|---|---|---|---|---|---|
| `WARN_INLINE_INDEX_01` | `FAIL_SECRET_READ_APPROVABLE_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | `expected_verdict` | `FAIL_POLICY` | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | CI activation warning; index and actual validator agree. | Align inline to index. |
| `WARN_INLINE_INDEX_02` | `FAIL_CREDENTIAL_EXPORT_APPROVABLE_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | `expected_verdict` | `FAIL_POLICY` | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | CI activation warning; index and actual validator agree. | Align inline to index. |
| `WARN_INLINE_INDEX_03` | `FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | `expected_error_code` | `ERR_TRACE_FAMILY_UNKNOWN` | `ERR_TRACE_REQUIRED_MISSING` | CI activation warning; index and actual validator agree. | Align inline to index. |
| `WARN_INLINE_INDEX_04` | `FAIL_WORKER_NO_VERDICT_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | `expected_verdict` | `FAIL_POLICY` | `NEED_MORE_EVIDENCE` | CI activation warning; index and actual validator agree. | Align inline to index. |

## 9_SELECTED_SOLUTION

All four warnings are resolved by aligning inline metadata to the canonical index. No index change is justified because harness actual outcomes already match the index.

## 12_INVARIANTS

- Do not modify fixture snippets.
- Do not modify validator logic.
- Do not modify harness logic.
- Do not modify canonical index verdicts.
- Do not alter fixture count.

## 13_ESTABLISHED

Each warning is metadata drift only. None is a validator mismatch.

## 14_HYPOTHESIS

After inline metadata alignment, the harness warning array should be empty.

## 15_REMAINING_GAP

No remaining warning is expected after correction.

## 16_TODO

Run the corpus harness after edits to prove:

```text
warnings=[]
```

## 17_RESUME_POINT

Use this inventory to audit the applied patch.

## 18_TO_DOCUMENT

The closeout must record warnings before and after reconciliation.

## 19_TO_REMEMBER

The fixture index remains canonical.

## RISKS

- À qualifier.
