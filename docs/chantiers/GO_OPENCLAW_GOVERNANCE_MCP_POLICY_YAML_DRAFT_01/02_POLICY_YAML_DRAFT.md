---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_YAML_DRAFT
doc_type: policy_yaml_draft
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 02_POLICY_YAML_DRAFT

## 1_MASTER_TARGET

Donner une premiere forme YAML documentaire de la policy MCP OpenClaw, alignable plus tard avec un schema machine-readable.

## 2_INITIAL_PROJECT_DOC

Ce draft derive de :

- `02_POLICY_SCHEMA_FIELDS.md`
- `03_CAPABILITY_POLICY_CLASSES.md`
- `08_DENY_BY_DEFAULT_RULES.md`
- `10_POLICY_EXAMPLES_DRAFT.md`

## 3_INITIAL_NEED

Representer en un bloc lisible :

- metadata ;
- version ;
- default policy ;
- classes ;
- gates ;
- traces ;
- evals ;
- strict workers ;
- Ollama Lab ;
- governor decisions ;
- never allowed ;
- blocked by default ;
- examples.

## 4_MASTER_PROJECT_PLAN

Le YAML ci-dessous est un artefact Markdown. Il ne doit pas etre extrait, charge, parse ou execute sans futur GO explicite.

## 6_FINAL_TARGET

Draft YAML documentaire complet, non runtime.

## 7_CANONICAL_STATE

Le default global est `BLOCKED_BY_DEFAULT`. Le champ `runtime_binding` est `false`. Les capabilities `NEVER_ALLOWED` ont `approval_path: none`.

## 8_VALIDATED_PLAN

Inclure les capabilities minimales demandees :

- `repo_state`
- `branch_state`
- `go_index_read`
- `chantier_read`
- `logs_tail_sanitized`
- `runtime_health_summary`
- `create_doc_file`
- `create_inbox_entry`
- `git_push`
- `merge`
- `branch_delete`
- `service_restart`
- `model_pull`
- `ollama_health_check`
- `smoke_test_no_trade`
- `unrestricted_shell`
- `sudo`
- `secret_read`
- `credential_export`
- `trade_execution`

## 9_SELECTED_SOLUTION

Bloc YAML documentaire :

```yaml
policy:
  id: OPENCLAW_MCP_POLICY_DRAFT_01
  policy_version: 0.1-doc-only
  status: draft_doc_only
  source_go: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
  source_schema_go: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
  runtime_binding: false
  validator_created: false
  active_config_mutation: false
  default_status: BLOCKED_BY_DEFAULT
  unknown_capability: BLOCKED_BY_DEFAULT
  secret_policy: no_secret_allowed
  trade_policy: no_trade_without_explicit_live_trading_go
  unrestricted_shell_policy: never_exposed_by_mcp
  sudo_policy: never_exposed_by_mcp
  forbidden_fields:
    - secret_value
    - token_value
    - password
    - api_key_value
    - private_key
    - credential_blob
    - raw_env
    - raw_runtime_log
    - unrestricted_command
    - sudo_password
    - broker_order_payload
    - approval_self_granted

default_policy:
  deny_by_default: true
  explicit_allow_only: true
  fail_closed: true
  missing_gate_binding: BLOCKED_BY_POLICY
  missing_trace_binding: FAIL_POLICY
  missing_eval_binding: FAIL_POLICY
  secret_detected: FAIL_SECRET_RISK
  runtime_mutation_without_gate: FAIL_RUNTIME_TOUCH
  unknown_or_unclassified_action: BLOCKED_BY_DEFAULT

capability_classes:
  READ_ONLY:
    default_allowed: true
    default_status: ALLOWED_IF_SCOPE_MATCH
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    approval_path: none
  READ_SANITIZED:
    default_allowed: true
    default_status: ALLOWED_IF_SANITIZED
    gate_required: false
    conditional_gate_required: true
    gate_id: required_if_raw_or_live
    trace_required: true
    trace_family: TRACE_RUNTIME_READ
    eval_required: true
    eval_profile: EVAL_NO_SECRET_LEAK
    approval_path: conditional
  WRITE_GATED:
    default_allowed: false
    default_status: BLOCKED_UNTIL_GATE
    gate_required: true
    gate_id: GATE_DOC_WRITE
    trace_required: true
    trace_family: TRACE_CODEX_PATCH
    eval_required: true
    eval_profile: EVAL_DOC_ONLY_COMPLIANCE
    rollback_required: true
    approval_path: human_gate
  RUNTIME_GATED:
    default_allowed: false
    default_status: BLOCKED_UNTIL_GATE
    gate_required: true
    gate_id: GATE_RUNTIME
    trace_required: true
    trace_family: TRACE_RUNTIME_GATED_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    approval_path: human_gate
  HUMAN_APPROVAL_REQUIRED:
    default_allowed: false
    default_status: BLOCKED_UNTIL_HUMAN_APPROVAL
    gate_required: true
    gate_id: gate_by_action_family
    trace_required: true
    trace_family: TRACE_HUMAN_GATE
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    approval_path: human_gate
  BLOCKED_BY_DEFAULT:
    default_allowed: false
    default_status: BLOCKED_BY_DEFAULT
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    approval_path: none_until_reclassified_by_go
  NEVER_ALLOWED:
    default_allowed: false
    default_status: NEVER_ALLOWED
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_VERDICT
    eval_required: true
    eval_profile: EVAL_FINAL_VERDICT_VALIDITY
    rollback_required: not_applicable
    approval_path: none

gates:
  GATE_DOC_WRITE:
    action_family: doc_chantier_or_local_inbox_write
    human_approval_required: true
    evidence_required: [go_id, target_path, diff_summary, source_refs]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_GLOBAL_INDEX:
    action_family: global_index_update
    human_approval_required: true
    evidence_required: [index_target, diff_summary, canonical_source, reason]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_GIT_PUSH:
    action_family: git_push_or_pr_publication
    human_approval_required: true
    evidence_required: [branch, remote, diff_summary, no_force_proof]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_BRANCH_DELETE:
    action_family: local_or_remote_branch_delete
    human_approval_required: true
    evidence_required: [exact_ref, merge_or_obsolete_proof, branch_state]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_MERGE:
    action_family: merge_pr_or_branch
    human_approval_required: true
    evidence_required: [pr_or_diff, tests_or_doc_proof, reviewer_status]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_RUNTIME:
    action_family: live_command_or_runtime_probe
    human_approval_required: true
    evidence_required: [exact_command, machine, timeout, no_secret_proof, no_trade_proof]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_OLLAMA_INSTALL:
    action_family: install_or_package_operation
    human_approval_required: true
    evidence_required: [package_source, version, disk_or_network_impact, rollback_plan]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_MODEL_PULL:
    action_family: model_download_or_pull
    human_approval_required: true
    evidence_required: [model_id, source, size, license_or_risk, destination]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_SERVICE_RESTART:
    action_family: service_restart_stop_start
    human_approval_required: true
    evidence_required: [service, exact_command, impact, rollback, maintenance_window]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_SECRET:
    action_family: secret_redaction_or_presence_metadata
    human_approval_required: true
    evidence_required: [need_statement, redaction_plan, no_value_output]
    rollback_required: true
    allowed_verdicts: [REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
    value_disclosure_allowed: false
  GATE_TRADE:
    action_family: trading_path_review
    human_approval_required: true
    evidence_required: [dedicated_trading_go, mode, risk, safeguards, no_secret_proof]
    rollback_required: true
    allowed_verdicts: [REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
    execution_authorized_by_this_policy: false
  GATE_MCP_WRITE:
    action_family: mcp_write_or_remote_effect
    human_approval_required: true
    evidence_required: [tool, target, payload_summary_no_secret, rollback]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_REMOTE_EXEC:
    action_family: remote_command_execution
    human_approval_required: true
    evidence_required: [host, command, user, timeout, impact, rollback]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]
  GATE_DATABASE_MUTATION:
    action_family: database_write_update_delete_migration
    human_approval_required: true
    evidence_required: [query_or_migration, backup, affected_rows_estimate, rollback]
    rollback_required: true
    allowed_verdicts: [APPROVED, REJECTED, NEED_MORE_EVIDENCE, BLOCKED_BY_POLICY]

traces:
  required_for_all_decisions: true
  families:
    TRACE_SESSION:
      eval: EVAL_TRACE_COMPLETENESS
    TRACE_GO:
      eval: EVAL_DOC_ONLY_COMPLIANCE
    TRACE_WORKER:
      eval: EVAL_WORKER_SCOPE_COMPLIANCE
    TRACE_TOOL_CALL:
      eval: EVAL_TRACE_COMPLETENESS
    TRACE_MCP_CALL:
      eval: EVAL_MCP_BOUNDARY_COMPLIANCE
    TRACE_CODEX_PATCH:
      eval: EVAL_DOC_ONLY_COMPLIANCE
    TRACE_GIT_ACTION:
      eval: EVAL_GATE_REQUIRED
    TRACE_HUMAN_GATE:
      eval: EVAL_GATE_APPROVAL_VALID
    TRACE_RUNTIME_READ:
      eval: EVAL_NO_RUNTIME_TOUCH
    TRACE_RUNTIME_GATED_ACTION:
      eval: EVAL_GATE_APPROVAL_VALID
    TRACE_SECRET_BLOCK:
      eval: EVAL_NO_SECRET_LEAK
    TRACE_TRADE_BLOCK:
      eval: EVAL_MCP_BOUNDARY_COMPLIANCE
    TRACE_EVAL_RUN:
      eval: EVAL_TRACE_COMPLETENESS
    TRACE_VERDICT:
      eval: EVAL_FINAL_VERDICT_VALIDITY

evals:
  promotion_requires_eval: true
  profiles:
    EVAL_DOC_ONLY_COMPLIANCE:
      pass_requires: [doc_only_scope, no_runtime, no_trade, no_secret, no_global_index_touch_unless_gated]
    EVAL_NO_SECRET_LEAK:
      pass_requires: [no_secret_values, no_raw_env, redaction_if_needed]
    EVAL_NO_RUNTIME_TOUCH:
      pass_requires: [no_live_mutation, no_service_change, no_process_change]
    EVAL_GATE_REQUIRED:
      pass_requires: [sensitive_action_classified, gate_id_present, gate_decision_trace_present]
    EVAL_GATE_APPROVAL_VALID:
      pass_requires: [human_decision_present, evidence_present, rollback_present, no_self_approval]
    EVAL_WORKER_SCOPE_COMPLIANCE:
      pass_requires: [role_fixed, allowed_capabilities_only, evidence_and_verdict_only]
    EVAL_MCP_BOUNDARY_COMPLIANCE:
      pass_requires: [capability_known, class_valid, default_policy_applied, forbidden_fields_absent]
    EVAL_TRACE_COMPLETENESS:
      pass_requires: [trace_id_present, actor_present, input_summary_no_secret, output_summary_no_secret, verdict_present]
    EVAL_ROLLBACK_READY:
      pass_requires: [rollback_rule_present, destructive_action_has_restore_or_mitigation]
    EVAL_FINAL_VERDICT_VALIDITY:
      pass_requires: [verdict_allowed, evidence_refs_present, blocked_reason_if_blocked]

strict_worker_roles:
  repo_auditor:
    allowed_capabilities: [repo_state, branch_state, go_index_read, chantier_read]
    blocked_capabilities: [git_push, merge, branch_delete, runtime_health_summary, secret_read, trade_execution, unrestricted_shell, sudo]
    required_trace: TRACE_WORKER
    required_eval: EVAL_WORKER_SCOPE_COMPLIANCE
    no_self_approval: true
  docops_auditor:
    allowed_capabilities: [go_index_read, chantier_read, create_doc_file, create_inbox_entry]
    blocked_capabilities: [git_push, merge, branch_delete, service_restart, secret_read, trade_execution]
    required_trace: TRACE_CODEX_PATCH
    required_eval: EVAL_DOC_ONLY_COMPLIANCE
    no_self_approval: true
  runtime_safety_reviewer:
    allowed_capabilities: [runtime_health_summary, logs_tail_sanitized]
    blocked_capabilities: [service_restart, sudo, unrestricted_shell, secret_read, trade_execution]
    required_trace: TRACE_RUNTIME_READ
    required_eval: EVAL_NO_RUNTIME_TOUCH
    no_self_approval: true
  mcp_security_reviewer:
    allowed_capabilities: [repo_state, chantier_read, logs_tail_sanitized]
    blocked_capabilities: [secret_read, credential_export, unrestricted_shell, sudo]
    required_trace: TRACE_MCP_CALL
    required_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
    no_self_approval: true
  ollama_lab_inspector:
    allowed_capabilities: [ollama_models_read, ollama_health_check, gateway_health_check, smoke_test_no_trade, provider_routing_read]
    blocked_capabilities: [model_pull, provider_switch, service_restart, install, secret_read, trade_execution, unrestricted_shell]
    required_trace: TRACE_RUNTIME_READ
    required_eval: EVAL_NO_RUNTIME_TOUCH
    no_self_approval: true
  trading_risk_gate:
    allowed_capabilities: [repo_state, chantier_read]
    blocked_capabilities: [trade_execution, secret_read, credential_export, unrestricted_shell]
    required_trace: TRACE_TRADE_BLOCK
    required_eval: EVAL_MCP_BOUNDARY_COMPLIANCE
    no_self_approval: true
  pr_reviewer:
    allowed_capabilities: [repo_state, branch_state, chantier_read]
    blocked_capabilities: [git_push, merge, branch_delete, secret_read, trade_execution]
    required_trace: TRACE_WORKER
    required_eval: EVAL_WORKER_SCOPE_COMPLIANCE
    no_self_approval: true
  memory_brick_extractor:
    allowed_capabilities: [chantier_read, create_doc_file, create_inbox_entry]
    blocked_capabilities: [global_index_update, git_push, merge, runtime_health_summary, secret_read]
    required_trace: TRACE_CODEX_PATCH
    required_eval: EVAL_DOC_ONLY_COMPLIANCE
    no_self_approval: true
  strict_worker_supervisor:
    allowed_capabilities: [repo_state, branch_state, chantier_read]
    blocked_capabilities: [git_push, merge, branch_delete, service_restart, secret_read, trade_execution]
    required_trace: TRACE_WORKER
    required_eval: EVAL_WORKER_SCOPE_COMPLIANCE
    no_self_approval: true

ollama_lab_policy:
  lab_status: local_non_production
  no_secret: true
  no_trade: true
  no_unrestricted_shell: true
  entries:
    ollama_models_read:
      capability_class: READ_ONLY
      default_status: ALLOWED_IF_METADATA_ONLY
      gate_id: none
      trace_family: TRACE_MCP_CALL
      eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    ollama_health_check:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_RUNTIME
      trace_family: TRACE_RUNTIME_READ
      eval_profile: EVAL_NO_RUNTIME_TOUCH
    gateway_health_check:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_RUNTIME
      trace_family: TRACE_RUNTIME_READ
      eval_profile: EVAL_NO_RUNTIME_TOUCH
    smoke_test_no_trade:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_RUNTIME
      trace_family: TRACE_RUNTIME_GATED_ACTION
      eval_profile: EVAL_GATE_APPROVAL_VALID
      trade_allowed: false
    provider_routing_read:
      capability_class: READ_ONLY
      default_status: ALLOWED_IF_DOC_OR_CONFIG_SUMMARY_ONLY
      gate_id: none
      trace_family: TRACE_MCP_CALL
      eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    model_pull:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_MODEL_PULL
      trace_family: TRACE_RUNTIME_GATED_ACTION
      eval_profile: EVAL_GATE_APPROVAL_VALID
    provider_switch:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_MCP_WRITE
      secondary_gate_id: GATE_RUNTIME
      trace_family: TRACE_RUNTIME_GATED_ACTION
      eval_profile: EVAL_GATE_APPROVAL_VALID
    service_restart:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_SERVICE_RESTART
      trace_family: TRACE_RUNTIME_GATED_ACTION
      eval_profile: EVAL_GATE_APPROVAL_VALID
    install:
      capability_class: RUNTIME_GATED
      default_status: BLOCKED_UNTIL_GATE
      gate_id: GATE_OLLAMA_INSTALL
      trace_family: TRACE_RUNTIME_GATED_ACTION
      eval_profile: EVAL_GATE_APPROVAL_VALID

capabilities:
  repo_state:
    capability_class: READ_ONLY
    default_status: ALLOWED_IF_SCOPE_MATCH
    allowed_actor: [Codex, OpenClaw_Governor, Repo_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [git_status_read]
    input_policy: bounded_repo_path
    output_policy: summary_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_WITH_REASON]
  branch_state:
    capability_class: READ_ONLY
    default_status: ALLOWED_IF_SCOPE_MATCH
    allowed_actor: [Codex, OpenClaw_Governor, Repo_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [branch_state_read]
    input_policy: docs_index_read_only
    output_policy: summary_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_WITH_REASON]
  go_index_read:
    capability_class: READ_ONLY
    default_status: ALLOWED_IF_SCOPE_MATCH
    allowed_actor: [Codex, OpenClaw_Governor, Repo_Auditor, DocOps_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [go_index_read]
    input_policy: docs_index_read_only
    output_policy: excerpt_or_summary_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_WITH_REASON]
  chantier_read:
    capability_class: READ_ONLY
    default_status: ALLOWED_IF_SCOPE_MATCH
    allowed_actor: [Codex, OpenClaw_Governor, Repo_Auditor, DocOps_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [chantier_doc_read]
    input_policy: chantier_path_only
    output_policy: summary_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    trace_required: true
    trace_family: TRACE_MCP_CALL
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_WITH_REASON]
  logs_tail_sanitized:
    capability_class: READ_SANITIZED
    default_status: ALLOWED_IF_SANITIZED
    allowed_actor: [Runtime_Safety_Reviewer, MCP_Security_Reviewer]
    blocked_actor: [unscoped_worker, raw_log_reader]
    machine_scope: [db-layer, student, admin-trading]
    tool_scope: [sanitized_log_excerpt]
    input_policy: named_log_source_and_redaction_rule
    output_policy: sanitized_excerpt_only
    secret_policy: redact_values_and_raw_env
    gate_required: false
    gate_id: required_if_raw_logs_or_live_command
    trace_required: true
    trace_family: TRACE_RUNTIME_READ
    eval_required: true
    eval_profile: EVAL_NO_SECRET_LEAK
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, PASS_RUNTIME_READ_ONLY, FAIL_SECRET_RISK, BLOCKED_BY_GATE]
  runtime_health_summary:
    capability_class: READ_SANITIZED
    default_status: ALLOWED_IF_EXISTING_ARTIFACT
    allowed_actor: [Runtime_Safety_Reviewer, Ollama_Lab_Inspector]
    blocked_actor: [unscoped_worker]
    machine_scope: [db-layer, student, admin-trading]
    tool_scope: [existing_health_report_summary]
    input_policy: existing_artifact_only_or_gate_for_live_probe
    output_policy: sanitized_summary_only
    secret_policy: no_secret_allowed
    gate_required: conditional
    gate_id: GATE_RUNTIME_IF_LIVE_PROBE
    trace_required: true
    trace_family: TRACE_RUNTIME_READ
    eval_required: true
    eval_profile: EVAL_NO_RUNTIME_TOUCH
    rollback_required: false
    verdicts: [PASS_DOC_ONLY, PASS_RUNTIME_READ_ONLY, FAIL_RUNTIME_TOUCH, BLOCKED_BY_GATE]
  create_doc_file:
    capability_class: WRITE_GATED
    default_status: BLOCKED_UNTIL_GATE_OR_EXPLICIT_GO_SCOPE
    allowed_actor: [Codex, DocOps_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [apply_patch_docs_chantier]
    input_policy: go_id_and_target_path_required
    output_policy: diff_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_DOC_WRITE
    trace_required: true
    trace_family: TRACE_CODEX_PATCH
    eval_required: true
    eval_profile: EVAL_DOC_ONLY_COMPLIANCE
    rollback_required: true
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_BY_GATE]
  create_inbox_entry:
    capability_class: WRITE_GATED
    default_status: BLOCKED_UNTIL_GATE_OR_EXPLICIT_GO_SCOPE
    allowed_actor: [Codex, DocOps_Auditor]
    blocked_actor: [unscoped_worker]
    machine_scope: [repo]
    tool_scope: [apply_patch_docs_index_inbox]
    input_policy: go_id_and_inbox_path_required
    output_policy: diff_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_DOC_WRITE
    trace_required: true
    trace_family: TRACE_CODEX_PATCH
    eval_required: true
    eval_profile: EVAL_DOC_ONLY_COMPLIANCE
    rollback_required: true
    verdicts: [PASS_DOC_ONLY, FAIL_POLICY, BLOCKED_BY_GATE]
  git_push:
    capability_class: HUMAN_APPROVAL_REQUIRED
    default_status: BLOCKED_UNTIL_HUMAN_APPROVAL
    allowed_actor: [human_repo_owner_after_gate]
    blocked_actor: [worker, proposer, bot_without_explicit_approval]
    machine_scope: [repo, GitHub]
    tool_scope: [git_push]
    input_policy: branch_remote_diff_no_force_proof
    output_policy: push_result_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_GIT_PUSH
    trace_required: true
    trace_family: TRACE_GIT_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE, FAIL_POLICY]
  merge:
    capability_class: HUMAN_APPROVAL_REQUIRED
    default_status: BLOCKED_UNTIL_HUMAN_APPROVAL
    allowed_actor: [human_maintainer_after_gate]
    blocked_actor: [worker, proposer, pr_reviewer_alone]
    machine_scope: [repo, GitHub]
    tool_scope: [merge_pr_or_branch]
    input_policy: pr_diff_tests_review_status
    output_policy: merge_result_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_MERGE
    trace_required: true
    trace_family: TRACE_GIT_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE, FAIL_POLICY]
  branch_delete:
    capability_class: HUMAN_APPROVAL_REQUIRED
    default_status: BLOCKED_UNTIL_HUMAN_APPROVAL
    allowed_actor: [human_repo_owner_after_gate]
    blocked_actor: [cleanup_worker_alone, unscoped_worker]
    machine_scope: [repo, GitHub]
    tool_scope: [branch_delete]
    input_policy: exact_ref_and_merged_or_obsolete_proof
    output_policy: delete_result_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_BRANCH_DELETE
    trace_required: true
    trace_family: TRACE_GIT_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE, FAIL_POLICY]
  service_restart:
    capability_class: RUNTIME_GATED
    default_status: BLOCKED_UNTIL_GATE
    allowed_actor: [human_runtime_owner_after_gate]
    blocked_actor: [worker, runtime_tool_alone]
    machine_scope: [db-layer, student, admin-trading]
    tool_scope: [service_restart_stop_start]
    input_policy: service_command_impact_rollback_window
    output_policy: runtime_report_sanitized
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_SERVICE_RESTART
    trace_required: true
    trace_family: TRACE_RUNTIME_GATED_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, FAIL_RUNTIME_TOUCH, BLOCKED_BY_GATE]
  model_pull:
    capability_class: RUNTIME_GATED
    default_status: BLOCKED_UNTIL_GATE
    allowed_actor: [human_lab_owner_after_gate]
    blocked_actor: [ollama_tool_alone, unscoped_worker]
    machine_scope: [student]
    tool_scope: [model_pull_download]
    input_policy: model_id_source_size_license_destination
    output_policy: pull_result_summary
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_MODEL_PULL
    trace_required: true
    trace_family: TRACE_RUNTIME_GATED_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, BLOCKED_BY_GATE, NEED_MORE_EVIDENCE, FAIL_POLICY]
  ollama_health_check:
    capability_class: RUNTIME_GATED
    default_status: BLOCKED_UNTIL_GATE
    allowed_actor: [Ollama_Lab_Inspector_after_gate]
    blocked_actor: [unscoped_worker]
    machine_scope: [student]
    tool_scope: [ollama_health_probe]
    input_policy: exact_command_no_install_no_pull
    output_policy: sanitized_health_report
    secret_policy: no_secret_allowed
    gate_required: true
    gate_id: GATE_RUNTIME
    trace_required: true
    trace_family: TRACE_RUNTIME_READ
    eval_required: true
    eval_profile: EVAL_NO_RUNTIME_TOUCH
    rollback_required: false
    verdicts: [PASS_RUNTIME_READ_ONLY, FAIL_RUNTIME_TOUCH, BLOCKED_BY_GATE]
  smoke_test_no_trade:
    capability_class: RUNTIME_GATED
    default_status: BLOCKED_UNTIL_GATE
    allowed_actor: [human_runtime_owner_after_gate]
    blocked_actor: [worker_alone, trading_worker]
    machine_scope: [student, db-layer, admin-trading]
    tool_scope: [smoke_test_no_trade]
    input_policy: exact_command_timeout_no_trade_proof
    output_policy: sanitized_smoke_report
    secret_policy: no_secret_allowed
    trade_policy: trade_allowed_false
    gate_required: true
    gate_id: GATE_RUNTIME
    trace_required: true
    trace_family: TRACE_RUNTIME_GATED_ACTION
    eval_required: true
    eval_profile: EVAL_GATE_APPROVAL_VALID
    rollback_required: true
    verdicts: [PASS_GATE_APPROVED, FAIL_RUNTIME_TOUCH, BLOCKED_BY_GATE]
  unrestricted_shell:
    capability_class: NEVER_ALLOWED
    default_status: NEVER_ALLOWED
    allowed_actor: []
    blocked_actor: [all]
    machine_scope: [all]
    tool_scope: [none]
    input_policy: not_accepted
    output_policy: blocked_reason_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    approval_path: none
    trace_required: true
    trace_family: TRACE_VERDICT
    eval_required: true
    eval_profile: EVAL_FINAL_VERDICT_VALIDITY
    rollback_required: not_applicable
    verdicts: [BLOCKED_BY_POLICY, NEVER_ALLOWED]
  sudo:
    capability_class: NEVER_ALLOWED
    default_status: NEVER_ALLOWED
    allowed_actor: []
    blocked_actor: [all]
    machine_scope: [all]
    tool_scope: [none]
    input_policy: not_accepted_inside_mcp
    output_policy: blocked_reason_only
    secret_policy: no_secret_allowed
    gate_required: false
    gate_id: none
    approval_path: none
    trace_required: true
    trace_family: TRACE_VERDICT
    eval_required: true
    eval_profile: EVAL_FINAL_VERDICT_VALIDITY
    rollback_required: not_applicable
    verdicts: [BLOCKED_BY_POLICY, NEVER_ALLOWED]
  secret_read:
    capability_class: NEVER_ALLOWED
    default_status: NEVER_ALLOWED
    allowed_actor: []
    blocked_actor: [all]
    machine_scope: [all]
    tool_scope: [none]
    input_policy: not_accepted
    output_policy: no_value_output
    secret_policy: values_never_read_or_displayed
    gate_required: false
    gate_id: none
    approval_path: none
    trace_required: true
    trace_family: TRACE_SECRET_BLOCK
    eval_required: true
    eval_profile: EVAL_NO_SECRET_LEAK
    rollback_required: not_applicable
    verdicts: [FAIL_SECRET_RISK, BLOCKED_BY_POLICY, NEVER_ALLOWED]
  credential_export:
    capability_class: NEVER_ALLOWED
    default_status: NEVER_ALLOWED
    allowed_actor: []
    blocked_actor: [all]
    machine_scope: [all]
    tool_scope: [none]
    input_policy: not_accepted
    output_policy: no_credential_output
    secret_policy: export_forbidden
    gate_required: false
    gate_id: none
    approval_path: none
    trace_required: true
    trace_family: TRACE_SECRET_BLOCK
    eval_required: true
    eval_profile: EVAL_NO_SECRET_LEAK
    rollback_required: not_applicable
    verdicts: [FAIL_SECRET_RISK, BLOCKED_BY_POLICY, NEVER_ALLOWED]
  trade_execution:
    capability_class: NEVER_ALLOWED
    default_status: NEVER_ALLOWED
    allowed_actor: []
    blocked_actor: [all]
    machine_scope: [admin-trading, all]
    tool_scope: [none]
    input_policy: not_accepted_without_dedicated_live_trading_go
    output_policy: blocked_reason_only
    secret_policy: no_secret_allowed
    trade_policy: execution_forbidden_by_this_policy
    gate_required: false
    gate_id: none
    approval_path: none
    trace_required: true
    trace_family: TRACE_TRADE_BLOCK
    eval_required: true
    eval_profile: EVAL_MCP_BOUNDARY_COMPLIANCE
    rollback_required: not_applicable
    verdicts: [BLOCKED_BY_POLICY, NEVER_ALLOWED]

governor_decision_rules:
  - if capability_id is missing then BLOCKED_BY_DEFAULT
  - if capability_class is missing then BLOCKED_BY_POLICY
  - if capability_class is NEVER_ALLOWED then NEVER_ALLOWED
  - if forbidden_field is present then FAIL_POLICY
  - if secret value is detected then FAIL_SECRET_RISK
  - if runtime mutation has no gate then FAIL_RUNTIME_TOUCH
  - if gate is required and no valid gate decision exists then BLOCKED_BY_GATE
  - if trace is missing then FAIL_POLICY
  - if eval binding is missing then FAIL_POLICY
  - if worker approves own action then BLOCKED_BY_POLICY

never_allowed:
  approval_path: none
  capabilities: [unrestricted_shell, sudo, secret_read, credential_export, trade_execution]
  actions:
    - secret_exfiltration
    - credential_display
    - credential_export
    - unrestricted_shell_exposure
    - sudo_inside_mcp
    - suppress_audit_trace
    - bypass_human_gate
    - auto_approval_by_same_worker
    - trade_execution_without_explicit_live_trading_go

blocked_by_default:
  unknown_capability: true
  unclassified_action: true
  missing_required_field: true
  missing_gate_binding: true
  missing_trace_binding: true
  missing_eval_binding: true
  global_index_write_without_gate: true
  destructive_action_without_rollback: true

examples:
  repo_state:
    expected_decision: PASS_DOC_ONLY
    reason: read-only bounded repo status summary
  logs_tail_sanitized:
    expected_decision: PASS_DOC_ONLY
    reason: sanitized excerpt only, no raw secret value
  create_doc_file:
    expected_decision: PASS_DOC_ONLY
    reason: explicit GO scope acts as doc-write gate for chantier files only
  git_push:
    expected_decision: BLOCKED_BY_GATE
    reason: human gate required, no push in doc-only GO
  model_pull:
    expected_decision: BLOCKED_BY_GATE
    reason: GATE_MODEL_PULL required, no runtime in this GO
  secret_read:
    expected_decision: NEVER_ALLOWED
    reason: no secret values can be read or displayed
  trade_execution:
    expected_decision: NEVER_ALLOWED
    reason: governance policy cannot execute trades
  unrestricted_shell:
    expected_decision: NEVER_ALLOWED
    reason: MCP cannot expose shell libre
```

## 12_INVARIANTS

- This YAML is documentary only.
- It must not be saved as active runtime policy in this GO.
- It must not be loaded by any process.
- It must not create a validator.
- `NEVER_ALLOWED` entries have `approval_path: none`.
- Unknown capability is blocked.

## 13_ESTABLISHED

The draft encodes the established chain:

```text
MCP Boundary
-> Human Review Gates
-> Trace / Evals Profile
-> MCP Policy Schema
-> MCP Policy YAML Draft
```

## 14_HYPOTHESIS

Future YAML may split capabilities into multiple files or a registry folder. This GO keeps all content in Markdown to avoid accidental runtime use.

## 15_REMAINING_GAP

- YAML syntax not automatically validated.
- JSON equivalence not mechanically generated.
- Runtime policy loader not defined.

## 16_TODO

- Map this YAML to a JSON shape in `03_POLICY_JSON_MAPPING_DRAFT.md`.
- Expand capability tables in `04_CAPABILITY_CLASS_ENTRIES.md`.
- Bind gates/traces/evals in `05_GATE_TRACE_EVAL_BINDINGS.md`.

## 17_RESUME_POINT

Use this file as the canonical draft payload for the rest of this chantier.

## 18_TO_DOCUMENT

Document strict worker and Ollama Lab entries in their dedicated files so this YAML remains readable.

## 19_TO_REMEMBER

The YAML is intentionally inert. Runtime promotion requires a distinct GO and a validator/gateway design.
