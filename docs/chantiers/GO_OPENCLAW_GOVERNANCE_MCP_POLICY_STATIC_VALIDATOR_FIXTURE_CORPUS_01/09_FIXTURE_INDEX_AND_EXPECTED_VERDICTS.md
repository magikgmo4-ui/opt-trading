# 09 - Fixture Index And Expected Verdicts

## 1_MASTER_TARGET

OpenClaw must maintain a documentary fixture corpus for the future MCP Policy static validator before any executable validator, runtime binding, active YAML file, or active JSON file exists.

## 2_INITIAL_PROJECT_DOC

Source chain:

- `GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01`
- `GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01`
- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01`

## 3_INITIAL_NEED

The future validator needs a stable fixture index to compare conceptual policy snippets against deterministic expected verdicts and expected error codes.

## 4_MASTER_PROJECT_PLAN

This file creates the complete fixture registry for the corpus. It is documentation only and does not execute, parse, load, or validate any snippet.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`

## 7_CANONICAL_STATE

The fixture registry uses the validator verdict and error taxonomy from the static validator specification.

## 8_VALIDATED_PLAN

Each fixture entry declares:

- fixture identifier;
- owning Markdown file;
- fixture category;
- expected verdict;
- expected error code;
- related validation rule;
- related gate;
- related trace;
- related eval.

## 9_SELECTED_SOLUTION

Use one consolidated Markdown table. The table is intended for future extraction by a read-only harness, but this GO does not implement that harness.

## 12_INVARIANTS

- Markdown only.
- No active YAML file.
- No active JSON file.
- No executable file.
- No runtime binding.
- No real secret.
- No trade action.
- No sudo.
- No unrestricted shell action.
- Unknown capability remains blocked by default.
- Invalid fixture maps to one primary error code.
- Valid fixture maps to `expected_error_code: none`.

## 13_ESTABLISHED

| fixture_id | file | category | expected_verdict | expected_error_code | related_rule | related_gate | related_trace | related_eval |
|---|---|---|---|---|---|---|---|---|
| `VALID_MINIMAL_POLICY_01` | `02_VALID_POLICY_FIXTURES.md` | valid_schema | `PASS_POLICY_STATIC_VALIDATION` | `none` | required minimal schema present | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `VALID_READ_ONLY_REPO_STATE_01` | `02_VALID_POLICY_FIXTURES.md` | valid_capability | `PASS_POLICY_STATIC_VALIDATION` | `none` | `READ_ONLY` trace and eval present | `none` | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `VALID_READ_SANITIZED_LOGS_01` | `02_VALID_POLICY_FIXTURES.md` | valid_capability | `PASS_POLICY_STATIC_VALIDATION` | `none` | `READ_SANITIZED` output is sanitized | `none` | `TRACE_RUNTIME_READ` | `EVAL_NO_SECRET_LEAK` |
| `VALID_WRITE_GATED_DOC_FILE_01` | `02_VALID_POLICY_FIXTURES.md` | valid_gated_write | `PASS_POLICY_STATIC_VALIDATION` | `none` | gated write has gate, trace, eval | `GATE_DOC_WRITE` | `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED` |
| `VALID_RUNTIME_GATED_OLLAMA_HEALTH_01` | `02_VALID_POLICY_FIXTURES.md` | valid_runtime_gated | `PASS_POLICY_STATIC_VALIDATION` | `none` | runtime-gated health check has evidence and rollback rule | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_NO_RUNTIME_TOUCH` |
| `VALID_NEVER_ALLOWED_SECRET_READ_BLOCKED_01` | `02_VALID_POLICY_FIXTURES.md` | valid_never_allowed_block | `PASS_POLICY_STATIC_VALIDATION` | `none` | `NEVER_ALLOWED` has no approval path | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_MISSING_POLICY_ID_01` | `03_SCHEMA_FAILURE_FIXTURES.md` | schema_failure | `FAIL_SCHEMA_MISSING_FIELD` | `ERR_SCHEMA_MISSING_FIELD` | `policy.id` required | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `FAIL_MISSING_DEFAULT_STATUS_01` | `03_SCHEMA_FAILURE_FIXTURES.md` | schema_failure | `FAIL_SCHEMA_MISSING_FIELD` | `ERR_SCHEMA_MISSING_FIELD` | `policy.default_status` required | `none` | `TRACE_VERDICT` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_RUNTIME_BINDING_TRUE_01` | `03_SCHEMA_FAILURE_FIXTURES.md` | schema_failure | `FAIL_RUNTIME_BINDING_ENABLED` | `ERR_RUNTIME_BINDING_ENABLED` | runtime binding must be false | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_NO_RUNTIME_TOUCH` |
| `FAIL_MISSING_CAPABILITY_CLASSES_01` | `03_SCHEMA_FAILURE_FIXTURES.md` | schema_failure | `FAIL_SCHEMA_MISSING_FIELD` | `ERR_SCHEMA_MISSING_FIELD` | `capability_classes` required | `none` | `TRACE_VERDICT` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_MISSING_GOVERNOR_RULES_01` | `03_SCHEMA_FAILURE_FIXTURES.md` | schema_failure | `FAIL_SCHEMA_MISSING_FIELD` | `ERR_SCHEMA_MISSING_FIELD` | `governor_decision_rules` required | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `FAIL_UNKNOWN_CLASS_01` | `04_CAPABILITY_CLASS_FAILURE_FIXTURES.md` | class_failure | `FAIL_UNKNOWN_CLASS` | `ERR_UNKNOWN_CLASS` | capability class enum closed | `none` | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_READ_SANITIZED_WITHOUT_SANITIZED_OUTPUT_01` | `04_CAPABILITY_CLASS_FAILURE_FIXTURES.md` | class_failure | `FAIL_POLICY` | `ERR_READ_SANITIZED_OUTPUT` | sanitized output policy required | `none` | `TRACE_RUNTIME_READ` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_WRITE_GATED_DEFAULT_ALLOWED_01` | `04_CAPABILITY_CLASS_FAILURE_FIXTURES.md` | class_failure | `FAIL_POLICY` | `ERR_DEFAULT_ALLOW_BLOCKED_CLASS` | gated write cannot default allow | `GATE_DOC_WRITE` | `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED` |
| `FAIL_RUNTIME_GATED_WITHOUT_GATE_01` | `04_CAPABILITY_CLASS_FAILURE_FIXTURES.md` | class_failure | `FAIL_GATE_BINDING` | `ERR_RUNTIME_WITHOUT_GATE` | runtime action requires gate | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_NO_RUNTIME_TOUCH` |
| `FAIL_BLOCKED_BY_DEFAULT_ALLOWED_TRUE_01` | `04_CAPABILITY_CLASS_FAILURE_FIXTURES.md` | class_failure | `FAIL_POLICY` | `ERR_DEFAULT_ALLOW_BLOCKED_CLASS` | blocked default cannot allow | `none` | `TRACE_VERDICT` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_WRITE_GATED_WITHOUT_GATE_ID_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | gate_trace_eval_failure | `FAIL_GATE_BINDING` | `ERR_WRITE_WITHOUT_GATE` | write gated requires gate id | `GATE_DOC_WRITE` | `TRACE_HUMAN_GATE` | `EVAL_GATE_REQUIRED` |
| `FAIL_GATE_WITHOUT_TRACE_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | gate_trace_eval_failure | `FAIL_TRACE_BINDING` | `ERR_TRACE_REQUIRED_MISSING` | gate must produce human gate trace | `GATE_DOC_WRITE` | `TRACE_HUMAN_GATE` | `EVAL_TRACE_COMPLETENESS` |
| `FAIL_MCP_CALL_WITHOUT_TRACE_MCP_CALL_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | gate_trace_eval_failure | `FAIL_TRACE_BINDING` | `ERR_TRACE_REQUIRED_MISSING` | MCP call requires MCP call trace | `none` | `TRACE_MCP_CALL` | `EVAL_TRACE_COMPLETENESS` |
| `FAIL_FINAL_VERDICT_WITHOUT_TRACE_VERDICT_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | gate_trace_eval_failure | `FAIL_TRACE_BINDING` | `ERR_TRACE_REQUIRED_MISSING` | final verdict requires verdict trace | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |
| `FAIL_CAPABILITY_WITHOUT_EVAL_01` | `05_GATE_TRACE_EVAL_FAILURE_FIXTURES.md` | gate_trace_eval_failure | `FAIL_EVAL_BINDING` | `ERR_EVAL_REQUIRED_MISSING` | capability requires eval binding | `none` | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_NEVER_ALLOWED_WITH_APPROVAL_PATH_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | `ERR_NEVER_ALLOWED_APPROVAL_PATH` | never allowed approval path must be none | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_SECRET_READ_APPROVABLE_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | `ERR_NEVER_ALLOWED_APPROVAL_PATH` | secret read cannot be approvable | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_CREDENTIAL_EXPORT_APPROVABLE_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_NEVER_ALLOWED_APPROVAL_PATH` | `ERR_NEVER_ALLOWED_APPROVAL_PATH` | credential export cannot be approvable | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_TRADE_EXECUTION_ALLOWED_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_POLICY` | `ERR_GATE_BYPASS_ALLOWED` | trade execution cannot be allowed without explicit live GO | `GATE_TRADE` | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_BYPASS_HUMAN_GATE_ALLOWED_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_POLICY` | `ERR_GATE_BYPASS_ALLOWED` | human gate bypass cannot be allowed | `GATE_RUNTIME` | `TRACE_HUMAN_GATE` | `EVAL_GATE_APPROVAL_VALID` |
| `FAIL_SUPPRESS_AUDIT_TRACE_ALLOWED_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_POLICY` | `ERR_SUPPRESS_TRACE_ALLOWED` | audit trace suppression cannot be allowed | `none` | `TRACE_VERDICT` | `EVAL_TRACE_COMPLETENESS` |
| `FAIL_UNRESTRICTED_SHELL_ALLOWED_01` | `06_NEVER_ALLOWED_FAILURE_FIXTURES.md` | never_allowed_failure | `FAIL_POLICY` | `ERR_GATE_BYPASS_ALLOWED` | unrestricted shell cannot be allowed | `GATE_REMOTE_EXEC` | `TRACE_TOOL_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` |
| `FAIL_SECRET_LIKE_FIELD_NAME_01` | `07_NO_SECRET_FAILURE_FIXTURES.md` | no_secret_failure | `FAIL_SECRET_RISK` | `ERR_SECRET_RISK` | forbidden secret-like field name | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_TOKEN_LIKE_PLACEHOLDER_01` | `07_NO_SECRET_FAILURE_FIXTURES.md` | no_secret_failure | `FAIL_SECRET_RISK` | `ERR_SECRET_RISK` | token-like placeholder blocked even when fake | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_ENV_DUMP_POLICY_01` | `07_NO_SECRET_FAILURE_FIXTURES.md` | no_secret_failure | `FAIL_SECRET_RISK` | `ERR_SECRET_RISK` | env dump policy forbidden | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_CREDENTIAL_DISPLAY_POLICY_01` | `07_NO_SECRET_FAILURE_FIXTURES.md` | no_secret_failure | `FAIL_SECRET_RISK` | `ERR_SECRET_RISK` | credential display forbidden | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_WORKER_SELF_APPROVAL_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | strict_worker_failure | `FAIL_POLICY` | `ERR_SELF_APPROVAL` | worker cannot approve own action | `GATE_DOC_WRITE` | `TRACE_WORKER` | `EVAL_WORKER_SCOPE_COMPLIANCE` |
| `FAIL_WORKER_OUT_OF_SCOPE_TOOL_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | strict_worker_failure | `FAIL_POLICY` | `ERR_OLLAMA_UNBOUNDED_ACTION` | worker tool must be in role scope | `GATE_RUNTIME` | `TRACE_TOOL_CALL` | `EVAL_WORKER_SCOPE_COMPLIANCE` |
| `FAIL_WORKER_RUNTIME_WITHOUT_GATE_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | strict_worker_failure | `FAIL_GATE_BINDING` | `ERR_RUNTIME_WITHOUT_GATE` | worker runtime action requires gate | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_NO_RUNTIME_TOUCH` |
| `FAIL_WORKER_SECRET_ACCESS_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | strict_worker_failure | `FAIL_SECRET_RISK` | `ERR_SECRET_RISK` | worker secret access forbidden | `GATE_SECRET` | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` |
| `FAIL_WORKER_NO_VERDICT_01` | `08_STRICT_WORKER_FAILURE_FIXTURES.md` | strict_worker_failure | `NEED_MORE_EVIDENCE` | `ERR_NEED_MORE_EVIDENCE` | worker output requires explicit verdict | `none` | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` |

## 14_HYPOTHESIS

The future harness can treat this table as the canonical expected-outcome registry, but it must still fail closed if any fixture snippet or metadata disagrees with the table.

## 15_REMAINING_GAP

No parser, extraction logic, validator, or report generator exists in this GO.

## 16_TODO

For a later implementation GO:

- parse the Markdown fixture metadata;
- extract fenced snippets as inert test inputs;
- run the static validator in read-only mode;
- compare output verdict and error code against this table;
- fail closed on missing, ambiguous, or contradictory metadata.

## 17_RESUME_POINT

The corpus now has a deterministic index of valid and invalid fixtures for the future MCP Policy static validator.

## 18_TO_DOCUMENT

Future implementation documentation must preserve the distinction between:

- fixture metadata;
- fixture snippets;
- expected validator outputs;
- executable harness behavior.

## 19_TO_REMEMBER

This file is a documentary registry. It is not a manifest loaded by runtime and must not be treated as an active policy artifact.
