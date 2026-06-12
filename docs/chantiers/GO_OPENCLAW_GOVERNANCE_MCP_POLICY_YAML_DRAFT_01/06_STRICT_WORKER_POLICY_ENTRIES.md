---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_STRICT_WORKERS
doc_type: strict_worker_policy_entries
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 06_STRICT_WORKER_POLICY_ENTRIES

## 1_MASTER_TARGET

Borner les strict workers par la policy MCP : preuves, scope, trace, eval et verdict, sans auto-approval.

## 2_INITIAL_PROJECT_DOC

Sources :

- MCP Boundary strict worker contract.
- Human Review Gates strict worker approval contract.
- Trace/Evals worker trace and worker scope eval.

## 3_INITIAL_NEED

Un strict worker peut contribuer a l'analyse, mais ne doit pas devenir approver, runtime owner, secret reader, trader, merge actor ou shell executor.

## 4_MASTER_PROJECT_PLAN

Chaque role est defini par :

- role ;
- scope ;
- allowed capabilities ;
- blocked capabilities ;
- output contract ;
- verdict contract ;
- no self-approval rule.

## 6_FINAL_TARGET

Une table de roles strict workers directement transposable dans une future policy.

## 7_CANONICAL_STATE

Contrat commun :

```text
role: fixed
scope: one GO or one review surface
outputs: evidence_summary + trace_ref + verdict
forbidden: self_approval, merge, push, runtime mutation, secret value, trade, unrestricted shell
```

## 8_VALIDATED_PLAN

Roles requis par le prompt :

- Repo Auditor
- DocOps Auditor
- Runtime Safety Reviewer
- MCP Security Reviewer
- Ollama Lab Inspector
- Trading Risk Gate
- PR Reviewer
- Memory Brick Extractor
- Strict Worker Supervisor

## 9_SELECTED_SOLUTION

| role | scope | allowed capabilities | blocked capabilities | required trace | required eval | output contract | verdict contract | no self-approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repo Auditor | repo state and branch evidence | `repo_state`, `branch_state`, `go_index_read`, `chantier_read` | `git_push`, `merge`, `branch_delete`, `runtime_health_summary`, `secret_read`, `trade_execution`, `unrestricted_shell`, `sudo` | `TRACE_WORKER` | `EVAL_WORKER_SCOPE_COMPLIANCE` | evidence summary, file refs, no mutation | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_WITH_REASON` | yes |
| DocOps Auditor | chantier docs and local inbox only | `go_index_read`, `chantier_read`, `create_doc_file`, `create_inbox_entry` | global index write, `git_push`, `merge`, `branch_delete`, `service_restart`, `secret_read`, `trade_execution` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | doc diff summary, source refs, no runtime | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_BY_GATE` | yes |
| Runtime Safety Reviewer | existing runtime evidence and sanitized summaries | `runtime_health_summary`, `logs_tail_sanitized` | `service_restart`, `model_pull`, `sudo`, `unrestricted_shell`, `secret_read`, `trade_execution` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | sanitized report, no live mutation unless gated | `PASS_RUNTIME_READ_ONLY`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` | yes |
| MCP Security Reviewer | MCP boundary and no-secret review | `repo_state`, `chantier_read`, `logs_tail_sanitized` | `secret_read`, `credential_export`, `unrestricted_shell`, `sudo`, `trade_execution` | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | boundary finding, forbidden field check | `PASS_DOC_ONLY`, `FAIL_SECRET_RISK`, `BLOCKED_BY_POLICY` | yes |
| Ollama Lab Inspector | local lab read/probe review only | `ollama_models_read`, `ollama_health_check`, `gateway_health_check`, `smoke_test_no_trade`, `provider_routing_read` | `model_pull`, `provider_switch`, `service_restart`, `install`, `secret_read`, `trade_execution`, `unrestricted_shell` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | sanitized lab status, no install/pull | `PASS_RUNTIME_READ_ONLY`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` | yes |
| Trading Risk Gate | trading risk refusal and preconditions | `repo_state`, `chantier_read` | `trade_execution`, broker mutation, alert-to-trade bridge, `secret_read`, `credential_export`, `unrestricted_shell` | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | risk note, blocked reason, dedicated GO requirement | `BLOCKED_BY_POLICY`, `NEVER_ALLOWED`, `NEED_MORE_EVIDENCE` | yes |
| PR Reviewer | PR/doc review evidence only | `repo_state`, `branch_state`, `chantier_read` | `git_push`, `merge`, `branch_delete`, PR approval of own work, `secret_read`, `trade_execution` | `TRACE_WORKER` | `EVAL_WORKER_SCOPE_COMPLIANCE` | review findings, tests/doc proof, no merge | `PASS_DOC_ONLY`, `FAIL_POLICY`, `NEED_MORE_EVIDENCE` | yes |
| Memory Brick Extractor | extract concise continuity, no global index write | `chantier_read`, `create_doc_file`, `create_inbox_entry` | global index write, `git_push`, `merge`, runtime probe, `secret_read`, `trade_execution` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | local memory brick, source refs, no global index mutation | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_BY_GATE` | yes |
| Strict Worker Supervisor | scope and evidence supervision | `repo_state`, `branch_state`, `chantier_read` | `git_push`, `merge`, `branch_delete`, `service_restart`, `secret_read`, `trade_execution`, self-approval | `TRACE_WORKER` | `EVAL_WORKER_SCOPE_COMPLIANCE` | scope audit, worker verdict review, escalation note | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_BY_POLICY` | yes |

## 12_INVARIANTS

- A worker cannot approve its own action.
- A worker cannot expand its role during the mission.
- A worker cannot merge, push, delete branches, restart services, install packages, pull models, read secrets or trade.
- A worker output is evidence plus verdict, not authority.
- Sensitive action requests escalate to Governor and human gate.

## 13_ESTABLISHED

Strict workers are policy subjects, not policy governors. They can produce evidence and recommend a verdict, but they do not grant gates.

## 14_HYPOTHESIS

Future worker orchestration can map these roles to agent manifests, but role manifests are not created here.

## 15_REMAINING_GAP

- No worker runtime.
- No worker manifest.
- No assignment queue.
- No identity binding.

## 16_TODO

- Future GO can define worker manifest schema.
- Future GO can define worker trace storage.
- Future GO can define conflict-of-interest checks.

## 17_RESUME_POINT

Any worker request that needs a blocked capability becomes a gate request or a `BLOCKED_BY_POLICY` verdict.

## 18_TO_DOCUMENT

Future validator should reject any role entry with overlapping `allowed_capabilities` and `blocked_capabilities`.

## 19_TO_REMEMBER

The strict worker model is evidence-first and authority-limited.

## RISKS

- À qualifier.
