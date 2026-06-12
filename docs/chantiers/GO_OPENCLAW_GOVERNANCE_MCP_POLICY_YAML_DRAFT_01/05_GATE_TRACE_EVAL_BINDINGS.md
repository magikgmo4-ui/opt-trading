---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_BINDINGS
doc_type: gate_trace_eval_bindings
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 05_GATE_TRACE_EVAL_BINDINGS

## 1_MASTER_TARGET

Relier chaque capability a son gate, sa trace, son eval, son role strict worker et la decision attendue du Governor.

## 2_INITIAL_PROJECT_DOC

Sources :

- Human Review Gates : gate taxonomy et verdicts.
- Trace/Evals Profile : trace families et eval profiles.
- MCP Policy Schema : champs `gate_id`, `trace_family`, `eval_profile`, `verdicts`.

## 3_INITIAL_NEED

Une policy exploitable doit pouvoir repondre a quatre questions :

- quelle classe ?
- quel gate ?
- quelle trace ?
- quel eval ?

## 4_MASTER_PROJECT_PLAN

Table de compatibilite minimale :

| capability_id | capability_class | gate_id | trace_family | eval_profile | governor_decision | strict_worker_role |
| --- | --- | --- | --- | --- | --- | --- |
| `repo_state` | `READ_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | allow if scoped, trace verdict | Repo Auditor |
| `branch_state` | `READ_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | allow if scoped, trace verdict | Repo Auditor |
| `go_index_read` | `READ_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | allow read-only excerpt | Repo Auditor, DocOps Auditor |
| `chantier_read` | `READ_ONLY` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | allow read-only summary | Repo Auditor, DocOps Auditor |
| `logs_tail_sanitized` | `READ_SANITIZED` | conditional `GATE_RUNTIME` if live/raw | `TRACE_RUNTIME_READ` | `EVAL_NO_SECRET_LEAK` | allow sanitized artifact, block raw/live without gate | Runtime Safety Reviewer, MCP Security Reviewer |
| `runtime_health_summary` | `READ_SANITIZED` | conditional `GATE_RUNTIME` if live | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | allow existing artifact, gate live probe | Runtime Safety Reviewer, Ollama Lab Inspector |
| `create_doc_file` | `WRITE_GATED` | `GATE_DOC_WRITE` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | allow only within explicit GO scope | DocOps Auditor |
| `create_inbox_entry` | `WRITE_GATED` | `GATE_DOC_WRITE` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | allow only local inbox for current GO | DocOps Auditor |
| `git_push` | `HUMAN_APPROVAL_REQUIRED` | `GATE_GIT_PUSH` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block without human approval | PR Reviewer cannot self-approve |
| `merge` | `HUMAN_APPROVAL_REQUIRED` | `GATE_MERGE` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block for worker/proposer | PR Reviewer cannot merge |
| `branch_delete` | `HUMAN_APPROVAL_REQUIRED` | `GATE_BRANCH_DELETE` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block cleanup without explicit gate | Strict Worker Supervisor cannot delete |
| `service_restart` | `RUNTIME_GATED` | `GATE_SERVICE_RESTART` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block in doc-only GO | Runtime Safety Reviewer |
| `model_pull` | `RUNTIME_GATED` | `GATE_MODEL_PULL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block until lab owner approval | Ollama Lab Inspector |
| `ollama_health_check` | `RUNTIME_GATED` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | block in this doc-only GO | Ollama Lab Inspector |
| `smoke_test_no_trade` | `RUNTIME_GATED` | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | block in this doc-only GO, no trade always | Ollama Lab Inspector, Trading Risk Gate |
| `unrestricted_shell` | `NEVER_ALLOWED` | none | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` | `NEVER_ALLOWED` | none |
| `sudo` | `NEVER_ALLOWED` | none inside MCP | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` | `NEVER_ALLOWED` inside MCP | none |
| `secret_read` | `NEVER_ALLOWED` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` | `FAIL_SECRET_RISK` or `NEVER_ALLOWED` | MCP Security Reviewer blocks |
| `credential_export` | `NEVER_ALLOWED` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` | `FAIL_SECRET_RISK` or `NEVER_ALLOWED` | MCP Security Reviewer blocks |
| `trade_execution` | `NEVER_ALLOWED` | none in this policy | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | `NEVER_ALLOWED` without explicit live trading GO; no execution here | Trading Risk Gate blocks |

## 6_FINAL_TARGET

The final target is a compatibility matrix that binds MCP Boundary class, Human Gate, Trace family, Eval profile, Strict Worker role and Governor decision.

## 7_CANONICAL_STATE

Standard gate verdicts :

- `APPROVED`
- `REJECTED`
- `NEED_MORE_EVIDENCE`
- `BLOCKED_BY_POLICY`

Standard final verdicts include :

- `PASS_DOC_ONLY`
- `PASS_RUNTIME_READ_ONLY`
- `PASS_GATE_APPROVED`
- `FAIL_POLICY`
- `FAIL_SECRET_RISK`
- `FAIL_RUNTIME_TOUCH`
- `BLOCKED_WITH_REASON`
- `BLOCKED_BY_GATE`
- `BLOCKED_BY_POLICY`
- `NEVER_ALLOWED`
- `NEED_MORE_EVIDENCE`

## 8_VALIDATED_PLAN

Gate-to-trace pattern :

| gate_id | trace_family | eval_profile |
| --- | --- | --- |
| `GATE_DOC_WRITE` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` |
| `GATE_GLOBAL_INDEX` | `TRACE_CODEX_PATCH` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_GIT_PUSH` | `TRACE_GIT_ACTION` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_BRANCH_DELETE` | `TRACE_GIT_ACTION` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_MERGE` | `TRACE_GIT_ACTION` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_RUNTIME` | `TRACE_RUNTIME_READ` or `TRACE_RUNTIME_GATED_ACTION` | `EVAL_NO_RUNTIME_TOUCH` or `EVAL_GATE_APPROVAL_VALID` |
| `GATE_OLLAMA_INSTALL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_MODEL_PULL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_SERVICE_RESTART` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `GATE_TRADE` | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `GATE_MCP_WRITE` | `TRACE_MCP_CALL` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_REMOTE_EXEC` | `TRACE_RUNTIME_GATED_ACTION` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `GATE_DATABASE_MUTATION` | `TRACE_TOOL_CALL` + `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |

## 9_SELECTED_SOLUTION

The selected solution is table-driven binding. The future validator can fail closed if any capability references an unknown gate, trace family or eval profile.

## 12_INVARIANTS

- Gate required means action blocked until gate decision exists.
- Trace required means missing trace is `FAIL_POLICY`.
- Eval required means missing eval binding is `FAIL_POLICY`.
- A strict worker never grants its own gate.
- `NEVER_ALLOWED` ignores gate requests and remains blocked.

## 13_ESTABLISHED

Capability class, gate, trace and eval are now linked in a single table.

## 14_HYPOTHESIS

Future implementations can derive a policy middleware from this table, but no middleware is created here.

## 15_REMAINING_GAP

- No static cross-reference checker.
- No unique id registry.
- No validator output format.

## 16_TODO

- Carry this table into any future validator spec.
- Preserve fail-closed behavior for missing bindings.

## 17_RESUME_POINT

If a capability fails to resolve through this file, the Governor should treat it as `BLOCKED_BY_POLICY` or `BLOCKED_BY_DEFAULT`.

## 18_TO_DOCUMENT

Future docs should add negative examples for missing gate, missing trace and missing eval.

## 19_TO_REMEMBER

An approval without a matching trace and eval does not promote an action.

## RISKS

- À qualifier.
