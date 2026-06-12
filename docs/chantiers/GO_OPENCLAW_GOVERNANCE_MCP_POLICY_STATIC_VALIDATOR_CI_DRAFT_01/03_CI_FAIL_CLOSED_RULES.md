# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 03_CI_FAIL_CLOSED_RULES

## 1_MASTER_TARGET

Define fail-closed rules for the future MCP Policy static validator CI.

## 2_INITIAL_PROJECT_DOC

The rules inherit from the static validator spec, error catalog, fixture corpus, implementation tests, and fixture harness behavior.

## 3_INITIAL_NEED

The future CI must reject unsafe, incomplete, contradictory, or ambiguous validation evidence rather than guessing or passing partially.

## 4_MASTER_PROJECT_PLAN

Record future fail conditions as mandatory CI rules without creating an active workflow.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Canonical validator failure verdicts include:

```text
FAIL_SCHEMA_MISSING_FIELD
FAIL_UNKNOWN_CLASS
FAIL_GATE_BINDING
FAIL_TRACE_BINDING
FAIL_EVAL_BINDING
FAIL_NEVER_ALLOWED_APPROVAL_PATH
FAIL_SECRET_RISK
FAIL_RUNTIME_BINDING_ENABLED
FAIL_POLICY
BLOCKED_WITH_REASON
NEED_MORE_EVIDENCE
```

Canonical harness failure verdicts include:

```text
FAIL_FIXTURE_EXPECTATION_MISMATCH
BLOCKED_WITH_REASON
```

## 8_VALIDATED_PLAN

Future CI fail-closed rules:

| Rule | CI result | Required evidence |
|---|---|---|
| Validator unit test fails | CI fail | Failing test name and command exit code. |
| Harness unit test fails | CI fail | Failing test name and command exit code. |
| Fixture mismatch | CI fail | Fixture id, expected verdict/error, actual verdict/error. |
| Missing fixture snippet | CI fail | `BLOCKED_WITH_REASON` from harness. |
| Duplicate fixture block | CI fail | `BLOCKED_WITH_REASON` from harness. |
| Missing fixture index row | CI fail | `BLOCKED_WITH_REASON` from harness. |
| Secret risk | CI fail | `FAIL_SECRET_RISK` with suppressed value. |
| Runtime binding detected | CI fail | `FAIL_RUNTIME_BINDING_ENABLED`. |
| Active YAML/JSON policy detected outside approved scope | CI fail | Path and reason, without content dump. |
| Network call requirement in validator or harness | CI fail | Static tool no-network invariant violated. |
| Unknown capability not blocked | CI fail | `ERR_UNKNOWN_CAPABILITY` or policy inconsistency. |
| `NEVER_ALLOWED` with approval path | CI fail | `FAIL_NEVER_ALLOWED_APPROVAL_PATH`. |
| Warning policy not satisfied | CI blocked | `GATE_CI_ACTIVATION` remains closed. |

## 9_SELECTED_SOLUTION

The future CI must treat safety failures as hard failures and warning-policy gaps as activation blockers. It must not auto-fix policy files, fixture metadata, or workflow config.

## 12_INVARIANTS

- Fail closed on missing evidence.
- Fail closed on contradictory evidence.
- Fail closed on unknown capability drift.
- Fail closed on secret risk.
- Fail closed on runtime binding.
- Fail closed on active policy artifacts outside scope.
- No auto-fix.
- No runtime promotion.

## 13_ESTABLISHED

The harness already fails closed on missing snippets and duplicate fixture blocks. The validator already fails closed on schema, class, gate, trace, eval, never-allowed, secret risk, runtime binding, and unknown capability problems.

## 14_HYPOTHESIS

The future active CI can reuse current exit codes, but should also publish a concise report artifact after a separate approval GO.

## 15_REMAINING_GAP

Warning strictness is not implemented as active CI behavior. The current draft defines that activation is gated until warnings are corrected or accepted.

## 16_TODO

Future activation must define whether inline/index warnings:

- fail CI immediately; or
- remain reported and accepted by explicit governance decision.

## 17_RESUME_POINT

This fail-closed rule set is the safety contract for future CI activation.

## 18_TO_DOCUMENT

Future report schema must expose:

- command;
- verdict;
- error code;
- fixture count;
- mismatch count;
- warning count;
- blocked reasons.

## 19_TO_REMEMBER

Fail closed means no silent pass on unknown, missing, unsafe, or contradictory input.

## RISKS

- À qualifier.
