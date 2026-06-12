---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_CAPABILITY_ENTRIES
doc_type: capability_class_entries
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 04_CAPABILITY_CLASS_ENTRIES

## 1_MASTER_TARGET

Rendre lisible la table canonique des capabilities minimales du draft policy MCP.

## 2_INITIAL_PROJECT_DOC

Sources :

- `02_POLICY_YAML_DRAFT.md`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/03_CAPABILITY_POLICY_CLASSES.md`
- `GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/02_CAPABILITY_CLASSIFICATION_MATRIX.md`

## 3_INITIAL_NEED

Chaque capability doit etre classee avec son default status, son gate, sa trace, son eval, ses acteurs, son scope machine, son risque et ses verdicts possibles.

## 4_MASTER_PROJECT_PLAN

La table ci-dessous sert de vue compacte pour le Governor. Elle ne remplace pas le YAML draft ; elle le rend auditable.

## 6_FINAL_TARGET

Une table complete des capabilities minimales demandees.

## 7_CANONICAL_STATE

Classes retenues :

- `READ_ONLY`
- `READ_SANITIZED`
- `WRITE_GATED`
- `RUNTIME_GATED`
- `HUMAN_APPROVAL_REQUIRED`
- `BLOCKED_BY_DEFAULT`
- `NEVER_ALLOWED`

## 8_VALIDATED_PLAN

La table couvre les 20 capabilities minimales du prompt et conserve les decisions fail-closed.

## 9_SELECTED_SOLUTION

| capability_id | class | default status | gate | trace | eval | allowed actor | blocked actor | machine scope | risk | verdicts possibles |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `repo_state` | `READ_ONLY` | `ALLOWED_IF_SCOPE_MATCH` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | Codex, OpenClaw Governor, Repo Auditor | unscoped worker | repo | low | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_WITH_REASON` |
| `branch_state` | `READ_ONLY` | `ALLOWED_IF_SCOPE_MATCH` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | Codex, OpenClaw Governor, Repo Auditor | unscoped worker | repo | low | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_WITH_REASON` |
| `go_index_read` | `READ_ONLY` | `ALLOWED_IF_SCOPE_MATCH` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | Codex, OpenClaw Governor, Repo Auditor, DocOps Auditor | unscoped worker | repo | low | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_WITH_REASON` |
| `chantier_read` | `READ_ONLY` | `ALLOWED_IF_SCOPE_MATCH` | none | `TRACE_MCP_CALL` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | Codex, OpenClaw Governor, Repo Auditor, DocOps Auditor | unscoped worker | repo | low | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_WITH_REASON` |
| `logs_tail_sanitized` | `READ_SANITIZED` | `ALLOWED_IF_SANITIZED` | conditional if raw/live | `TRACE_RUNTIME_READ` | `EVAL_NO_SECRET_LEAK` | Runtime Safety Reviewer, MCP Security Reviewer | raw log reader, unscoped worker | db-layer, student, admin-trading | high | `PASS_DOC_ONLY`, `PASS_RUNTIME_READ_ONLY`, `FAIL_SECRET_RISK`, `BLOCKED_BY_GATE` |
| `runtime_health_summary` | `READ_SANITIZED` | `ALLOWED_IF_EXISTING_ARTIFACT` | `GATE_RUNTIME` if live probe | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | Runtime Safety Reviewer, Ollama Lab Inspector | unscoped worker | db-layer, student, admin-trading | medium | `PASS_DOC_ONLY`, `PASS_RUNTIME_READ_ONLY`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` |
| `create_doc_file` | `WRITE_GATED` | `BLOCKED_UNTIL_GATE_OR_EXPLICIT_GO_SCOPE` | `GATE_DOC_WRITE` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | Codex, DocOps Auditor | unscoped worker | repo | medium | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_BY_GATE` |
| `create_inbox_entry` | `WRITE_GATED` | `BLOCKED_UNTIL_GATE_OR_EXPLICIT_GO_SCOPE` | `GATE_DOC_WRITE` | `TRACE_CODEX_PATCH` | `EVAL_DOC_ONLY_COMPLIANCE` | Codex, DocOps Auditor | unscoped worker | repo | medium | `PASS_DOC_ONLY`, `FAIL_POLICY`, `BLOCKED_BY_GATE` |
| `git_push` | `HUMAN_APPROVAL_REQUIRED` | `BLOCKED_UNTIL_HUMAN_APPROVAL` | `GATE_GIT_PUSH` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human repo owner after gate | worker, proposer, bot without explicit approval | repo, GitHub | high | `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `NEED_MORE_EVIDENCE`, `FAIL_POLICY` |
| `merge` | `HUMAN_APPROVAL_REQUIRED` | `BLOCKED_UNTIL_HUMAN_APPROVAL` | `GATE_MERGE` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human maintainer after gate | worker, proposer, reviewer alone | repo, GitHub | high | `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `NEED_MORE_EVIDENCE`, `FAIL_POLICY` |
| `branch_delete` | `HUMAN_APPROVAL_REQUIRED` | `BLOCKED_UNTIL_HUMAN_APPROVAL` | `GATE_BRANCH_DELETE` | `TRACE_GIT_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human repo owner after gate | cleanup worker alone, unscoped worker | repo, GitHub | high | `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `NEED_MORE_EVIDENCE`, `FAIL_POLICY` |
| `service_restart` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_SERVICE_RESTART` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human runtime owner after gate | worker, runtime tool alone | db-layer, student, admin-trading | critical | `PASS_GATE_APPROVED`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` |
| `model_pull` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_MODEL_PULL` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human lab owner after gate | model tool alone, unscoped worker | student | high | `PASS_GATE_APPROVED`, `BLOCKED_BY_GATE`, `NEED_MORE_EVIDENCE`, `FAIL_POLICY` |
| `ollama_health_check` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_READ` | `EVAL_NO_RUNTIME_TOUCH` | Ollama Lab Inspector after gate | unscoped worker | student | medium | `PASS_RUNTIME_READ_ONLY`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` |
| `smoke_test_no_trade` | `RUNTIME_GATED` | `BLOCKED_UNTIL_GATE` | `GATE_RUNTIME` | `TRACE_RUNTIME_GATED_ACTION` | `EVAL_GATE_APPROVAL_VALID` | human runtime owner after gate | worker alone, trading worker | student, db-layer, admin-trading | high | `PASS_GATE_APPROVED`, `FAIL_RUNTIME_TOUCH`, `BLOCKED_BY_GATE` |
| `unrestricted_shell` | `NEVER_ALLOWED` | `NEVER_ALLOWED` | none | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` | none | all | all | critical | `BLOCKED_BY_POLICY`, `NEVER_ALLOWED` |
| `sudo` | `NEVER_ALLOWED` | `NEVER_ALLOWED` | none | `TRACE_VERDICT` | `EVAL_FINAL_VERDICT_VALIDITY` | none | all | all | critical | `BLOCKED_BY_POLICY`, `NEVER_ALLOWED` |
| `secret_read` | `NEVER_ALLOWED` | `NEVER_ALLOWED` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` | none | all | all | critical | `FAIL_SECRET_RISK`, `BLOCKED_BY_POLICY`, `NEVER_ALLOWED` |
| `credential_export` | `NEVER_ALLOWED` | `NEVER_ALLOWED` | none | `TRACE_SECRET_BLOCK` | `EVAL_NO_SECRET_LEAK` | none | all | all | critical | `FAIL_SECRET_RISK`, `BLOCKED_BY_POLICY`, `NEVER_ALLOWED` |
| `trade_execution` | `NEVER_ALLOWED` | `NEVER_ALLOWED` | none in this policy | `TRACE_TRADE_BLOCK` | `EVAL_MCP_BOUNDARY_COMPLIANCE` | none | all | admin-trading, all | critical | `BLOCKED_BY_POLICY`, `NEVER_ALLOWED` |

## 12_INVARIANTS

- A missing capability is not read as `READ_ONLY`.
- A capability with missing class is `BLOCKED_BY_POLICY`.
- A capability with `NEVER_ALLOWED` has no gate and no approval path.
- A write capability requires rollback.
- A runtime capability requires exact action evidence before any future approval.

## 13_ESTABLISHED

The capability table binds the minimum requested entries to policy classes and verdicts.

## 14_HYPOTHESIS

Future capabilities such as `provider_switch`, `install`, `gateway_health_check` and `provider_routing_read` can be added by the same pattern, but the minimum prompt set remains the normative baseline for this GO.

## 15_REMAINING_GAP

- No schema uniqueness check.
- No machine-readable enum validation.
- No automated duplicate detection.

## 16_TODO

- Use `05_GATE_TRACE_EVAL_BINDINGS.md` to review action-family bindings.
- Use `09_POLICY_DRAFT_VALIDATION_CHECKLIST.md` before future promotion.

## 17_RESUME_POINT

If a future GO adds a capability, it must add a row with class, gate, trace, eval, actors, scope, risk and verdicts.

## 18_TO_DOCUMENT

Future validator should reject capability entries missing any table column represented here.

## 19_TO_REMEMBER

Capabilities are allowlisted by id. A similar name, alias or inferred action remains blocked until explicitly defined.

## RISKS

- À qualifier.
