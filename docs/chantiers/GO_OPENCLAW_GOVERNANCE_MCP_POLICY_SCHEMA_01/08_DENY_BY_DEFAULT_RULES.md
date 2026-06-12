---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_DENY_BY_DEFAULT
doc_type: deny_by_default_rules
repo: opt-trading
project: opt-trading
module: governance_openclaw_mcp_policy_schema
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
status: draft_canonical
lifecycle_stage: doc_only_spec
surface: docs/chantiers
source_kind: canonical_local
updated_at: 2026-05-13
---

# 08_DENY_BY_DEFAULT_RULES

## 1_MASTER_TARGET

Lister les regles deny-by-default du schema MCP policy.

## 2_INITIAL_PROJECT_DOC

Source directe : MCP Boundary blocked/never allowed spec.

## 3_INITIAL_NEED

Faire du refus policy un resultat attendu et trace.

## 4_MASTER_PROJECT_PLAN

Chaque regle donne condition, verdict et trace attendue.

## 6_FINAL_TARGET

Registre conceptuel des refus.

## 7_CANONICAL_STATE

| Rule | Condition | Verdict | Trace | Notes |
| --- | --- | --- | --- | --- |
| Action non classee | action absent from policy | `BLOCKED_BY_DEFAULT` | `TRACE_MCP_CALL` | no action executed |
| Capability inconnue | `capability_id` absent/unknown | `BLOCKED_BY_POLICY` | `TRACE_MCP_CALL` | unclassified allowed would be fail |
| Class invalide | `capability_class` outside enum | `FAIL_POLICY` | `TRACE_MCP_CALL` | schema failure |
| Secret detecte | input/output/trace contains secret value or asks for value | `FAIL_SECRET_RISK` or `BLOCKED_BY_POLICY` | `TRACE_SECRET_BLOCK` | never reproduce value |
| Runtime mutation sans gate | live command, restart, install, pull, config mutation without gate | `FAIL_RUNTIME_TOUCH` if touched; `BLOCKED_BY_GATE` if stopped | `TRACE_RUNTIME_READ` or `TRACE_RUNTIME_GATED_ACTION` | exact command required |
| Trade sans GO live explicite | broker/paper/live order path without explicit trading GO | `NEVER_ALLOWED` / `BLOCKED_BY_POLICY` | `TRACE_TRADE_BLOCK` | no approval path in default MCP |
| Shell libre | generic shell requested | `BLOCKED_BY_DEFAULT` | `TRACE_MCP_CALL` | replace by named tool or dedicated GO |
| Sudo | privileged command requested | `BLOCKED_BY_DEFAULT` inside MCP | `TRACE_MCP_CALL` | ops GO outside MCP required |
| Credential export/display | value display/export requested | `NEVER_ALLOWED` | `TRACE_SECRET_BLOCK` | metadata-only alternative |
| Bypass human gate | action attempts to skip gate | `NEVER_ALLOWED` | `TRACE_HUMAN_GATE` or block trace | no approval path |
| Hide/suppress audit trace | action asks to omit trace | `NEVER_ALLOWED` | block trace | refusal trace mandatory |
| Destructive action without rollback | delete/mutate with no rollback | `NEVER_ALLOWED` | action/block trace | rollback first |
| Auto-approval | worker/tool approves own sensitive action | `NEVER_ALLOWED` | `TRACE_HUMAN_GATE` | conflict of authority |
| Global index write without gate | GO_INDEX/ACTIVE_STREAMS/REPRISE/BRANCH_STATE/MACHINE_SPLIT touched without gate | `BLOCKED_BY_GATE` or `FAIL_POLICY` | `TRACE_CODEX_PATCH` | not used in this GO |

## 8_VALIDATED_PLAN

Refusal output shape :

```text
verdict: BLOCKED_BY_POLICY
policy_ref:
requested_action:
reason:
safe_alternative:
trace_ref:
no_action_executed: true
```

## 9_SELECTED_SOLUTION

`BLOCKED_BY_DEFAULT` can be reclassified only by future GO. `NEVER_ALLOWED` cannot be reclassified inside OpenClaw MCP.

## 12_INVARIANTS

- Refusals are traced.
- Refusals do not expose secrets.
- Refusals do not execute action.
- Refusals may suggest a bounded alternative.

## 13_ESTABLISHED

The required deny-by-default cases are listed.

## 14_HYPOTHESIS

A future policy engine can map these rows to deterministic error codes.

## 15_REMAINING_GAP

No policy error code registry yet.

## 16_TODO

Future eval runner should include negative tests for every row.

## 17_RESUME_POINT

Use this file to decide whether a request is blocked before checking implementation detail.

## 18_TO_DOCUMENT

Future YAML/JSON should distinguish `BLOCKED_BY_DEFAULT` from `NEVER_ALLOWED`.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw MCP must be able to refuse safely: unknown, secret, trade, sudo, shell, runtime mutation and gate bypass are blocked or never allowed.
```

## RISKS

- À qualifier.
