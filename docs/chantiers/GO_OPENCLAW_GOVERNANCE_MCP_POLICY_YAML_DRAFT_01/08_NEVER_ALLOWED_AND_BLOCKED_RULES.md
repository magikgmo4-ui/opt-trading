---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_NEVER_ALLOWED_BLOCKED
doc_type: never_allowed_and_blocked_rules
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 08_NEVER_ALLOWED_AND_BLOCKED_RULES

## 1_MASTER_TARGET

Formaliser les refus fermes de la policy MCP OpenClaw.

## 2_INITIAL_PROJECT_DOC

Sources :

- MCP Boundary blocked and never allowed spec.
- Human Gates secret, trade, runtime and MCP write gates.
- Trace/Evals secret/trade block traces.
- MCP Policy Schema deny-by-default rules.

## 3_INITIAL_NEED

Le draft YAML/JSON doit empecher toute interpretation permissive pour les actions inconnues, dangereuses, non tracees ou sans gate.

## 4_MASTER_PROJECT_PLAN

Separer :

- `NEVER_ALLOWED` : aucun approval path dans MCP.
- `BLOCKED_BY_DEFAULT` : refus jusqu'a classification explicite par futur GO.
- `BLOCKED_BY_POLICY` : refus car la policy detecte une violation.
- `FAIL_*` : echec d'eval ou risque detecte.

## 6_FINAL_TARGET

Une liste de regles de refus reutilisable par un futur validator.

## 7_CANONICAL_STATE

Regle de base :

```text
not_explicitly_allowed = BLOCKED_BY_DEFAULT
known_forbidden = NEVER_ALLOWED
sensitive_without_gate = BLOCKED_BY_POLICY
secret_detected = FAIL_SECRET_RISK
runtime_without_gate = FAIL_RUNTIME_TOUCH
```

## 8_VALIDATED_PLAN

Regles demandees :

| rule_id | condition | decision | approval path | trace | eval |
| --- | --- | --- | --- | --- | --- |
| `RULE_UNKNOWN_ACTION` | action non classee | `BLOCKED_BY_DEFAULT` | none until reclassified by GO | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `RULE_UNKNOWN_CAPABILITY` | capability inconnue | `BLOCKED_BY_POLICY` | none until capability entry exists | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `RULE_SECRET_EXFILTRATION` | secret exfiltration | `NEVER_ALLOWED` or `FAIL_SECRET_RISK` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `RULE_CREDENTIAL_DISPLAY` | credential display | `NEVER_ALLOWED` or `FAIL_SECRET_RISK` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `RULE_TRADE_WITHOUT_LIVE_GO` | trade execution without explicit live GO | `NEVER_ALLOWED` in this policy | none | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `RULE_BYPASS_HUMAN_GATE` | sensitive action without gate | `BLOCKED_BY_POLICY` | valid gate required except never allowed | `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED` |
| `RULE_SUPPRESS_AUDIT_TRACE` | attempt to hide trace | `NEVER_ALLOWED` | none | `TRACE_VERDICT` | `EVAL_TRACE_COMPLETENESS` |
| `RULE_UNRESTRICTED_SHELL` | shell libre requested | `NEVER_ALLOWED` inside MCP | none | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `RULE_SUDO_WITHOUT_GO` | sudo request inside MCP | `NEVER_ALLOWED` inside MCP | none inside MCP | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `RULE_DESTRUCTIVE_NO_ROLLBACK` | destructive action without rollback | `BLOCKED_BY_POLICY` | gate cannot approve without rollback | `TRACE_HUMAN_GATE` | `EVAL_ROLLBACK_READY` |
| `RULE_AUTO_APPROVAL` | same worker approves own action | `BLOCKED_BY_POLICY` | none | `TRACE_WORKER` | `EVAL_WORKER_SCOPE_COMPLIANCE` |
| `RULE_RUNTIME_NO_GATE` | runtime mutation without gate | `FAIL_RUNTIME_TOUCH` | gate required before action | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` |
| `RULE_GLOBAL_INDEX_NO_GATE` | global index write without gate | `BLOCKED_BY_POLICY` | `GATE_GLOBAL_INDEX` | `TRACE_CODEX_PATCH` | `EVAL_GATE_APPROVAL_VALID` |
| `RULE_FORBIDDEN_FIELD` | forbidden policy field present | `FAIL_POLICY` | none until corrected by GO | `TRACE_VERDICT` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |

## 9_SELECTED_SOLUTION

Use fail-closed order :

1. If `capability_id` is missing, return `BLOCKED_BY_DEFAULT`.
2. If class is `NEVER_ALLOWED`, return `NEVER_ALLOWED`.
3. If any forbidden field is present, return `FAIL_POLICY`.
4. If any secret value is detected, return `FAIL_SECRET_RISK`.
5. If action is runtime and gate is missing, return `FAIL_RUNTIME_TOUCH`.
6. If action requires human gate and no gate decision exists, return `BLOCKED_BY_GATE`.
7. If trace or eval binding is missing, return `FAIL_POLICY`.
8. If all required bindings exist and scope is doc-only/read-only, allow the documented verdict.

## 12_INVARIANTS

- `NEVER_ALLOWED` cannot be converted to approved by a gate.
- Secret values are never reproduced in traces or examples.
- Shell libre is not a named MCP tool.
- Sudo is not exposed by MCP.
- Governance GO does not authorize trade execution.
- Trace suppression is itself a policy violation.

## 13_ESTABLISHED

The rules above implement deny-by-default and explicit allow only.

## 14_HYPOTHESIS

Future policy may add more `BLOCKED_BY_DEFAULT` classes for unknown providers, but not by relaxing existing `NEVER_ALLOWED` rules.

## 15_REMAINING_GAP

- No executable rule engine.
- No forbidden-field scanner.
- No no-secret detector.
- No runtime mutation detector.

## 16_TODO

- Future validator must encode these rules in fail-closed order.
- Future test cases must include negative examples.

## 17_RESUME_POINT

If an action looks ambiguous, classify it as `BLOCKED_BY_DEFAULT` until a future GO defines it.

## 18_TO_DOCUMENT

Future docs should distinguish MCP `NEVER_ALLOWED` from out-of-band ops GO procedures. This draft does not grant any out-of-band operation.

## 19_TO_REMEMBER

The absence of a rule is not permission. It is a block.
