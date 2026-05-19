# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 06_CI_WARNING_POLICY

## 1_MASTER_TARGET

Document the warning policy for inline/index expectation drift before any CI activation.

## 2_INITIAL_PROJECT_DOC

The warning policy is based on the fixture harness closeout and harness test results.

## 3_INITIAL_NEED

The harness reports 4 inline/index expectation differences. They are not mismatches against the canonical index, but they must be explicit before CI becomes active.

## 4_MASTER_PROJECT_PLAN

Record the nature, canonical source, blocking effect, promotion condition, and recommendation for each warning class.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Canonical expected verdict source:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md
```

Current warning count:

```text
4 inline/index expectation differences
```

The warnings are not validator mismatches:

```text
corpus: 37/37 PASS
mismatches: 0
```

## 8_VALIDATED_PLAN

Known warnings:

| Fixture | Inline field | Inline value | Canonical index value | Effect |
|---|---|---|---|---|
| `FAIL_SECRET_READ_APPROVABLE_01` | `expected_verdict` | `FAIL_POLICY` | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | Warning only in current harness; activation gated. |
| `FAIL_CREDENTIAL_EXPORT_APPROVABLE_01` | `expected_verdict` | `FAIL_POLICY` | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | Warning only in current harness; activation gated. |
| `FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01` | `expected_error_code` | `ERR_TRACE_FAMILY_UNKNOWN` | `ERR_TRACE_REQUIRED_MISSING` | Warning only in current harness; activation gated. |
| `FAIL_WORKER_NO_VERDICT_01` | `expected_verdict` | `FAIL_POLICY` | `NEED_MORE_EVIDENCE` | Warning only in current harness; activation gated. |

## 9_SELECTED_SOLUTION

Rule for this CI draft:

```text
The fixture index remains canonical.
The CI draft can be produced while warnings exist.
Active CI must remain gated until the warnings are either corrected or explicitly accepted as non-blocking by a future GO.
```

## 12_INVARIANTS

- Warnings must be visible.
- Warnings must not be silently ignored.
- Warnings must not override the canonical index.
- Warnings must not become active CI success criteria without approval.
- Warnings block CI activation unless corrected or accepted.

## 13_ESTABLISHED

The harness compares actual validator outcomes to the index and all 37 actual outcomes match the index. The inline differences are documentary metadata drift.

## 14_HYPOTHESIS

The cleanest path is a warning reconciliation GO that updates inline fixture expectations to match the canonical index, then reruns the harness before CI activation.

## 15_REMAINING_GAP

The 4 inline/index warnings remain unresolved in this GO by design. This GO documents them and gates activation.

## 16_TODO

Recommended next step:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01
```

Purpose:

- align inline fixture expectation fields with the canonical index; or
- formally accept index-as-canonical warnings as non-blocking before active CI.

## 17_RESUME_POINT

CI activation is blocked until warning handling is resolved or approved.

## 18_TO_DOCUMENT

Future closeout must record warning count:

- before reconciliation;
- after reconciliation;
- final CI activation policy.

## 19_TO_REMEMBER

Warnings are not current harness mismatches, but they are governance evidence. Treat them as activation blockers until resolved or accepted.
