# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 01_STATIC_VALIDATOR_PRINCIPLES

## 1_MASTER_TARGET

Define the principles for a future static validator of OpenClaw MCP policy.

## 2_INITIAL_PROJECT_DOC

This document binds the static validator to the governance chain already validated:

```text
MCP Boundary
Human Review Gates
Trace / Evals Profile
MCP Policy Schema
MCP Policy YAML Draft
```

## 3_INITIAL_NEED

The future validator must give a deterministic policy verdict before a policy can influence any runtime, worker, gateway, Ollama Lab action, or MCP action.

## 4_MASTER_PROJECT_PLAN

The plan is to define principles first, then derive contracts, validation rules, verdicts, and conceptual fixtures.

## 6_FINAL_TARGET

The final target is a non-executable specification for fail-closed static validation.

## 7_CANONICAL_STATE

The validator is specified as documentation only. It has no parser, no runtime loader, no active policy hook, no CLI, no test runner, and no auto-fix behavior in this GO.

## 8_VALIDATED_PLAN

Validation must happen conceptually before:

- policy promotion;
- worker use;
- MCP server use;
- Ollama Lab operational change;
- runtime action;
- any sensitive write;
- any human gate final verdict.

## 9_SELECTED_SOLUTION

The selected solution is a static validation model with these principles:

| Principle | Requirement | Failure mode |
|---|---|---|
| Spec only | Documentation is the only artifact in this GO. | `BLOCKED_WITH_REASON` if executable code is created. |
| No runtime binding | `runtime_binding` must be false. | `FAIL_RUNTIME_BINDING_ENABLED`. |
| Fail closed | Unknown, incomplete, or ambiguous state is blocked. | `FAIL_POLICY` or specific failure verdict. |
| Deny by default | Unknown capability validates as blocked. | `BLOCKED_BY_DEFAULT`. |
| Explicit allow only | No implicit allow from actor, machine, or tool name. | `FAIL_POLICY`. |
| No secret | Inputs, outputs, traces, fixtures, and examples contain no secret values. | `FAIL_SECRET_RISK`. |
| No auto-fix | Validator may report remediation, not mutate policy. | `FAIL_POLICY` if auto-fix is configured. |
| Deterministic | Same input produces same verdict and error list. | `FAIL_POLICY`. |
| Clear failure | Every failure has code, severity, message, and blocked action. | `NEED_MORE_EVIDENCE` only when evidence is absent. |
| No self approval | Worker cannot approve its own sensitive action. | `FAIL_POLICY` or `BLOCKED_BY_POLICY`. |

## 12_INVARIANTS

- Documentation only.
- No executable validator.
- No runtime binding.
- Fail closed.
- Deny by default.
- Explicit allow only.
- No secret in input or output.
- No auto-fix.
- Deterministic validation.
- Every failure must produce a clear verdict.
- Unknown capability is blocked as `BLOCKED_BY_DEFAULT`.
- `NEVER_ALLOWED` has no approval path.

## 13_ESTABLISHED

The prior policy schema establishes:

- `default_status` is explicit and never inferred;
- `secret_policy` is mandatory;
- traces are mandatory;
- evals are mandatory;
- gates are mandatory before sensitive actions;
- `NEVER_ALLOWED` cannot be softened by actor, machine, tool, or gate.

## 14_HYPOTHESIS

The validator can be implemented later as a read-only command. That implementation must not affect this spec: the rules here remain canonical even if the implementation language changes.

## 15_REMAINING_GAP

The spec does not yet define executable parsing details, file IO, package layout, or CI execution.

## 16_TODO

- Encode these principles into field rules.
- Encode these principles into capability class rules.
- Encode these principles into verdicts and fixtures.

## 17_RESUME_POINT

Resume point:

```text
Use this file before designing validator IO or failure codes.
```

## 18_TO_DOCUMENT

Future implementation notes must keep the validator read-only and must not add policy mutation, auto-remediation, or active runtime hooks.

## 19_TO_REMEMBER

The validator exists to block unsafe or incomplete policy drafts before they can become operational.

## RISKS

- À qualifier.
