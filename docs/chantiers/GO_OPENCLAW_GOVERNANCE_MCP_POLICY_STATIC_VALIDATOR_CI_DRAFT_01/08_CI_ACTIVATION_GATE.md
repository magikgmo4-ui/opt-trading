# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 08_CI_ACTIVATION_GATE

## 1_MASTER_TARGET

Define `GATE_CI_ACTIVATION` for any future active CI workflow for the MCP Policy static validator and fixture harness.

## 2_INITIAL_PROJECT_DOC

This gate follows the Human Review Gates, static validator spec, fixture harness closeout, and this CI draft.

## 3_INITIAL_NEED

Creating a real workflow can trigger automation. It therefore requires an explicit human gate and proof that warnings, runtime boundaries, and secret boundaries are handled.

## 4_MASTER_PROJECT_PLAN

Document required evidence, approvals, allowed future files, prohibited actions, rollback, and verdicts.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Gate identifier:

```text
GATE_CI_ACTIVATION
```

Gate status in this GO:

```text
defined_doc_only
not_executed
not_approved
```

## 8_VALIDATED_PLAN

Required evidence before activation:

| Evidence | Required value |
|---|---|
| Validator tests | Passing targeted test suite. |
| Harness tests | Passing targeted test suite. |
| Corpus harness | `37/37 PASS`, `0` mismatch or updated approved fixture count. |
| Warning policy | 4 warnings corrected or explicitly accepted as non-blocking. |
| Runtime policy | `runtime_binding` remains false and no runtime call exists. |
| Secret policy | No secret read, no env dump, no token-like output. |
| Workflow scope | Read-only checkout and static local commands only. |
| Human approval | Explicit approval for active workflow creation. |
| Rollback | Workflow removal or disable path documented. |

## 9_SELECTED_SOLUTION

Future files that may be created only after the gate passes:

```text
.github/workflows/openclaw_mcp_policy_static_validator.yml
```

Alternative names require the same gate.

## 12_INVARIANTS

- No active workflow before gate approval.
- No runtime OpenClaw call.
- No MCP live call.
- No Ollama call.
- No trade.
- No sudo.
- No secret.
- No environment dump.
- No warning suppression without documentation.
- No auto-fix.
- No workflow activation without rollback.

## 13_ESTABLISHED

Allowed future activation actions after approval:

- create one scoped workflow file;
- run validator unit tests;
- run harness unit tests;
- run corpus harness;
- run `git diff --check`;
- report pass, fail, mismatch, blocked, and warning counts.

Forbidden activation actions:

- load policy into runtime;
- call MCP live;
- call Ollama;
- call broker or trade;
- use repository secrets;
- dump environment;
- run sudo;
- mutate policy files;
- create broad workflow triggers without approval.

## 14_HYPOTHESIS

The warning reconciliation GO should happen before this gate is executed, because resolving the 4 inline/index warnings makes active CI behavior cleaner and easier to audit.

## 15_REMAINING_GAP

This GO defines the gate only. It does not approve, execute, or satisfy the gate.

## 16_TODO

Future activation sequence:

1. Resolve or accept inline/index warnings.
2. Rerun local validator tests.
3. Rerun local harness tests.
4. Rerun corpus harness.
5. Confirm no active YAML/JSON policy drift.
6. Obtain human approval.
7. Create scoped workflow in a dedicated GO.
8. Document rollback.

## 17_RESUME_POINT

`GATE_CI_ACTIVATION` is the mandatory checkpoint before creating any `.github/workflows` file.

## 18_TO_DOCUMENT

Future gate closeout must include:

- approver;
- evidence commands;
- warning decision;
- workflow path;
- rollback path;
- first CI result if available.

## 19_TO_REMEMBER

Possible gate verdicts:

```text
APPROVED_CI_ACTIVATION
BLOCKED_WITH_REASON
NEED_MORE_EVIDENCE
REJECTED_CI_ACTIVATION
```

## RISKS

- À qualifier.
