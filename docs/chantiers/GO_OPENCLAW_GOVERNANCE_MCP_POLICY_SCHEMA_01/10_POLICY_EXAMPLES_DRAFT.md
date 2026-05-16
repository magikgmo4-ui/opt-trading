---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_EXAMPLES_DRAFT
doc_type: policy_examples_draft
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

# 10_POLICY_EXAMPLES_DRAFT

## 1_MASTER_TARGET

Fournir des exemples conceptuels de policy MCP.

## 2_INITIAL_PROJECT_DOC

Base : fields, classes, gates, trace/eval bindings.

## 3_INITIAL_NEED

Montrer comment le schema pourrait se traduire plus tard en YAML/JSON, sans creer de policy executable.

## 4_MASTER_PROJECT_PLAN

Exemples requis :

- `repo_state` read-only ;
- `logs_tail_sanitized` ;
- `create_doc_file` write gated ;
- `git push` human approval ;
- `model_pull` gated ;
- `secret_read` never allowed ;
- `trade_execution` never allowed ;
- `unrestricted_shell` blocked.

## 6_FINAL_TARGET

Draft examples no-runtime, no-secret, non chargeables.

## 7_CANONICAL_STATE

### repo_state read-only

```yaml
capability_policy:
  policy_id: POLICY_REPO_STATE_READ
  policy_version: draft_01
  capability_id: repo_state
  capability_class: READ_ONLY
  default_status: ALLOW_IF_BOUNDED
  allowed_actor: [Codex, OpenClawGovernor, StrictWorker:RepoAuditor]
  blocked_actor: [any_unlisted]
  machine_scope: [repo]
  tool_scope: [git_status_read]
  input_policy: {allowed_params: [short_branch], forbidden_params: [raw_secret, token]}
  output_policy: {artifact: status_summary, sanitization: bounded}
  secret_policy: NO_SECRET_VALUES
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: [TRACE_MCP_CALL, TRACE_GIT_ACTION]
  eval_required: [EVAL_TRACE_COMPLETENESS, EVAL_MCP_BOUNDARY_COMPLIANCE]
  rollback_required: false
  rollback_policy: none
  verdicts: [PASS_DOC_ONLY, BLOCKED_WITH_REASON, NEED_MORE_EVIDENCE]
  escalation_path: [OpenClawGovernor]
  forbidden_fields: [secret_value, credential, raw_env]
  evidence_required: [git_status_summary]
  risk_level: low
  promotion_status: doc_only
```

### logs_tail_sanitized

```yaml
capability_policy:
  policy_id: POLICY_LOGS_TAIL_SANITIZED
  policy_version: draft_01
  capability_id: logs_tail_sanitized
  capability_class: READ_SANITIZED
  default_status: ALLOW_IF_SANITIZED
  allowed_actor: [StrictWorker:RuntimeSafetyReviewer, StrictWorker:MCPSecurityReviewer]
  blocked_actor: [any_unlisted]
  machine_scope: [db-layer, student, admin-trading]
  tool_scope: [log_summary_reader]
  input_policy: {allowed_params: [artifact_ref, max_lines], forbidden_params: [raw_env, token]}
  output_policy: {artifact: sanitized_excerpt, sanitization: required}
  secret_policy: REDACT_REQUIRED
  gate_required: true_if_raw_or_live
  gate_id: [GATE_SECRET, GATE_RUNTIME]
  trace_required: true
  trace_family: [TRACE_MCP_CALL, TRACE_RUNTIME_READ, TRACE_SECRET_BLOCK]
  eval_required: [EVAL_NO_SECRET_LEAK, EVAL_TRACE_COMPLETENESS]
  rollback_required: false
  rollback_policy: none
  verdicts: [PASS_DOC_ONLY, PASS_RUNTIME_READ_ONLY, FAIL_SECRET_RISK, BLOCKED_BY_POLICY]
  escalation_path: [SecurityOwner, RuntimeOwner]
  forbidden_fields: [secret_value, api_key, raw_log_with_token]
  evidence_required: [sanitizer_rule, no_secret_proof]
  risk_level: high
  promotion_status: doc_only
```

### create_doc_file write gated

```yaml
capability_policy:
  policy_id: POLICY_CREATE_DOC_FILE
  policy_version: draft_01
  capability_id: create_doc_file
  capability_class: WRITE_GATED
  default_status: NEEDS_GATE
  allowed_actor: [Codex]
  blocked_actor: [MCPTool:generic_writer, any_unlisted]
  machine_scope: [repo]
  tool_scope: [apply_patch]
  input_policy: {allowed_params: [go_id, target_path, doc_content], forbidden_params: [secret_value]}
  output_policy: {artifact: created_doc, sanitization: no_secret}
  secret_policy: NO_SECRET_VALUES
  gate_required: true
  gate_id: GATE_DOC_WRITE
  trace_required: true
  trace_family: [TRACE_CODEX_PATCH, TRACE_HUMAN_GATE]
  eval_required: [EVAL_DOC_ONLY_COMPLIANCE, EVAL_GATE_REQUIRED, EVAL_ROLLBACK_READY]
  rollback_required: true
  rollback_policy: delete_created_file_or_revert_patch
  verdicts: [PASS_DOC_ONLY, BLOCKED_BY_GATE, FAIL_POLICY]
  escalation_path: [HumanGOOwner, OpenClawGovernor]
  forbidden_fields: [secret_value, raw_env, credential]
  evidence_required: [go_id, target_path, diff_summary, sources]
  risk_level: medium
  promotion_status: doc_only
```

### git push human approval

```yaml
capability_policy:
  policy_id: POLICY_GIT_PUSH
  policy_version: draft_01
  capability_id: git_push
  capability_class: HUMAN_APPROVAL_REQUIRED
  default_status: NEEDS_GATE
  allowed_actor: [HumanRepoOwner]
  blocked_actor: [StrictWorker, MCPTool, any_unlisted]
  machine_scope: [repo, GitHub]
  tool_scope: [git_push_named]
  input_policy: {allowed_params: [branch, remote, refspec], forbidden_params: [force, token]}
  output_policy: {artifact: push_result, sanitization: no_credentials}
  secret_policy: NO_SECRET_VALUES
  gate_required: true
  gate_id: GATE_GIT_PUSH
  trace_required: true
  trace_family: [TRACE_GIT_ACTION, TRACE_HUMAN_GATE]
  eval_required: [EVAL_GATE_APPROVAL_VALID, EVAL_FINAL_VERDICT_VALIDITY]
  rollback_required: true
  rollback_policy: revert_commit_or_close_pr_plan
  verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE]
  escalation_path: [HumanRepoOwner]
  forbidden_fields: [force_push, credential, remote_token]
  evidence_required: [branch, remote, diff_summary, no_force_proof]
  risk_level: high
  promotion_status: doc_only
```

### model_pull gated

```yaml
capability_policy:
  policy_id: POLICY_OLLAMA_MODEL_PULL
  policy_version: draft_01
  capability_id: model_pull
  capability_class: HUMAN_APPROVAL_REQUIRED
  default_status: NEEDS_GATE
  allowed_actor: [HumanLabOwner]
  blocked_actor: [OllamaTool, StrictWorker, any_unlisted]
  machine_scope: [student]
  tool_scope: [ollama_model_pull_named]
  input_policy: {allowed_params: [model_id, source, expected_size], forbidden_params: [token, secret]}
  output_policy: {artifact: model_pull_report, sanitization: no_secret}
  secret_policy: NO_SECRET_VALUES
  gate_required: true
  gate_id: GATE_MODEL_PULL
  trace_required: true
  trace_family: [TRACE_HUMAN_GATE, TRACE_RUNTIME_GATED_ACTION]
  eval_required: [EVAL_GATE_APPROVAL_VALID, EVAL_ROLLBACK_READY, EVAL_NO_SECRET_LEAK]
  rollback_required: true
  rollback_policy: remove_model_restore_routing
  verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE]
  escalation_path: [HumanLabOwner, OpenClawGovernor]
  forbidden_fields: [api_key, credential, raw_env]
  evidence_required: [model_id, source, size, license_risk, destination, rollback_plan]
  risk_level: high
  promotion_status: doc_only
```

### secret_read never allowed

```yaml
capability_policy:
  policy_id: POLICY_SECRET_READ_NEVER
  policy_version: draft_01
  capability_id: secret_read
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  allowed_actor: []
  blocked_actor: [any_actor]
  machine_scope: [all_repo_machines]
  tool_scope: []
  input_policy: {allowed_params: [], forbidden_params: [secret_name, secret_value, env_dump]}
  output_policy: {artifact: blocked_verdict, sanitization: value_never_printed}
  secret_policy: NEVER_READ
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: [TRACE_SECRET_BLOCK]
  eval_required: [EVAL_NO_SECRET_LEAK, EVAL_FINAL_VERDICT_VALIDITY]
  rollback_required: false
  rollback_policy: none
  verdicts: [BLOCKED_BY_POLICY, FAIL_SECRET_RISK]
  escalation_path: [SecurityOwner_for_incident_only]
  forbidden_fields: [secret_value, credential, token, raw_env]
  evidence_required: [blocked_reason, policy_ref]
  risk_level: critical
  promotion_status: never
```

### trade_execution never allowed

```yaml
capability_policy:
  policy_id: POLICY_TRADE_EXECUTION_NEVER_DEFAULT_MCP
  policy_version: draft_01
  capability_id: trade_execution
  capability_class: NEVER_ALLOWED
  default_status: NEVER_ALLOWED
  allowed_actor: []
  blocked_actor: [any_actor]
  machine_scope: [admin-trading]
  tool_scope: []
  input_policy: {allowed_params: [], forbidden_params: [symbol, order, broker_token]}
  output_policy: {artifact: trade_block_verdict, sanitization: no_account_data}
  secret_policy: NO_SECRET_VALUES
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: [TRACE_TRADE_BLOCK]
  eval_required: [EVAL_GATE_REQUIRED, EVAL_FINAL_VERDICT_VALIDITY]
  rollback_required: false
  rollback_policy: none
  verdicts: [BLOCKED_BY_POLICY]
  escalation_path: [TradingOwner_for_dedicated_live_trading_GO]
  forbidden_fields: [api_key, broker_secret, account_value]
  evidence_required: [blocked_reason, required_live_trading_go]
  risk_level: critical
  promotion_status: never
```

### unrestricted_shell blocked

```yaml
capability_policy:
  policy_id: POLICY_UNRESTRICTED_SHELL_BLOCKED
  policy_version: draft_01
  capability_id: unrestricted_shell
  capability_class: BLOCKED_BY_DEFAULT
  default_status: BLOCKED_BY_DEFAULT
  allowed_actor: []
  blocked_actor: [any_actor]
  machine_scope: [all_repo_machines]
  tool_scope: []
  input_policy: {allowed_params: [], forbidden_params: [command_string, shell_session]}
  output_policy: {artifact: blocked_verdict, sanitization: no_execution}
  secret_policy: NO_SECRET_VALUES
  gate_required: false
  gate_id: none
  trace_required: true
  trace_family: [TRACE_MCP_CALL]
  eval_required: [EVAL_MCP_BOUNDARY_COMPLIANCE, EVAL_FINAL_VERDICT_VALIDITY]
  rollback_required: false
  rollback_policy: none
  verdicts: [BLOCKED_BY_POLICY, BLOCKED_WITH_REASON]
  escalation_path: [OpsGO_for_named_tool_only]
  forbidden_fields: [freeform_command, sudo, secret_value]
  evidence_required: [blocked_reason, safe_alternative_named_tool]
  risk_level: critical
  promotion_status: blocked
```

## 8_VALIDATED_PLAN

These examples are draft, non-executable and not loadable.

## 9_SELECTED_SOLUTION

Use YAML-like examples because they are readable and future-translation friendly, but this file is not a policy source.

## 12_INVARIANTS

- No real secrets.
- No runtime execution.
- No trade.
- No shell execution.
- No policy loading.

## 13_ESTABLISHED

All requested examples are present.

## 14_HYPOTHESIS

Future YAML policy can reuse these examples after validation and normalization.

## 15_REMAINING_GAP

No machine-readable policy file produced.

## 16_TODO

Future GO can create `policy.schema.yaml` or JSON Schema from these drafts.

## 17_RESUME_POINT

Use examples as illustrative references only.

## 18_TO_DOCUMENT

When promoted, add generated ids, schema version and validation report.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
Policy examples remain documentation until a dedicated GO creates and validates YAML/JSON runtime artifacts.
```
