---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_VALIDATION_CHECKLIST
doc_type: policy_draft_validation_checklist
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 09_POLICY_DRAFT_VALIDATION_CHECKLIST

## 1_MASTER_TARGET

Fournir une checklist documentaire pour relire le draft YAML/JSON avant toute promotion future.

## 2_INITIAL_PROJECT_DOC

Sources :

- MCP Policy Schema validation rules.
- Trace/Evals final verdict validity.
- Human Gates gate decision requirements.

## 3_INITIAL_NEED

Le draft doit pouvoir etre audite sans script et sans validator. La checklist documente les controles attendus.

## 4_MASTER_PROJECT_PLAN

La checklist couvre :

- schema completeness ;
- class validity ;
- gate binding ;
- trace binding ;
- eval binding ;
- secret policy ;
- default status ;
- forbidden fields ;
- rollback ;
- no executable script ;
- no runtime binding.

## 6_FINAL_TARGET

Une checklist PASS/FAIL/BLOCKED pour le draft documentaire.

## 7_CANONICAL_STATE

Expected verdict for this GO : `PASS_DOC_ONLY` if all checklist items are satisfied.

## 8_VALIDATED_PLAN

Checklist documentaire :

| check_id | check | expected result | failure verdict |
| --- | --- | --- | --- |
| `CHECK_DOC_ONLY` | Draft is stored in Markdown, not active `.yaml`/`.json` runtime file | pass | `FAIL_POLICY` |
| `CHECK_RUNTIME_BINDING_FALSE` | `runtime_binding: false` present | pass | `FAIL_RUNTIME_TOUCH` |
| `CHECK_VALIDATOR_NOT_CREATED` | no validator script, command or executable created | pass | `FAIL_POLICY` |
| `CHECK_SCHEMA_FIELDS_PRESENT` | metadata, policy_version, default_policy, classes, gates, traces, evals, roles and examples present | pass | `FAIL_POLICY` |
| `CHECK_DENY_BY_DEFAULT` | `default_status: BLOCKED_BY_DEFAULT` and unknown capability blocked | pass | `FAIL_POLICY` |
| `CHECK_CLASS_VALIDITY` | every class is one of the seven canonical classes | pass | `FAIL_POLICY` |
| `CHECK_CAPABILITY_IDS` | minimum capabilities from prompt are present | pass | `FAIL_POLICY` |
| `CHECK_GATE_BINDING` | sensitive capabilities have gate binding | pass | `BLOCKED_BY_POLICY` |
| `CHECK_TRACE_BINDING` | every capability has trace family | pass | `FAIL_POLICY` |
| `CHECK_EVAL_BINDING` | every capability has eval profile | pass | `FAIL_POLICY` |
| `CHECK_SECRET_POLICY` | every capability has no-secret policy | pass | `FAIL_SECRET_RISK` |
| `CHECK_FORBIDDEN_FIELDS_ABSENT` | forbidden fields are not used as data fields with values | pass | `FAIL_POLICY` |
| `CHECK_NEVER_ALLOWED_NO_APPROVAL` | every `NEVER_ALLOWED` entry has no gate and `approval_path: none` | pass | `FAIL_POLICY` |
| `CHECK_ROLLBACK_FOR_DESTRUCTIVE` | destructive/gated actions include rollback requirement | pass | `EVAL_ROLLBACK_READY` fail |
| `CHECK_STRICT_WORKERS_BOUNDED` | workers have allowed/blocked capabilities and no self-approval | pass | `BLOCKED_BY_POLICY` |
| `CHECK_OLLAMA_BOUNDED` | model pull, provider switch, restart and install are gated | pass | `BLOCKED_BY_GATE` |
| `CHECK_NO_TRADE` | no trade execution path exists | pass | `NEVER_ALLOWED` |
| `CHECK_NO_SUDO` | sudo not exposed by MCP | pass | `NEVER_ALLOWED` |
| `CHECK_NO_SHELL_LIBRE` | unrestricted shell not exposed by MCP | pass | `NEVER_ALLOWED` |
| `CHECK_INDEX_GLOBALS_UNTOUCHED` | global indexes are not modified by this GO | pass | `FAIL_POLICY` |
| `CHECK_ADMIN_PATHS_UNTOUCHED` | admin-trading out-of-scope paths are not modified/staged | pass | `FAIL_POLICY` |

## 9_SELECTED_SOLUTION

Manual validation flow :

1. Review file list.
2. Confirm only chantier and local inbox are changed.
3. Confirm no runtime/config/script file is created.
4. Confirm YAML/JSON remains fenced Markdown.
5. Confirm `NEVER_ALLOWED` has no approval path.
6. Confirm strict workers and Ollama Lab are bounded.
7. Confirm final closeout states `PASS_DOC_ONLY` or `BLOCKED_WITH_REASON`.

## 12_INVARIANTS

- Checklist is not a validator.
- Checklist is not executable.
- Checklist must fail closed when evidence is missing.
- A manual PASS does not authorize runtime loading.

## 13_ESTABLISHED

The checklist maps policy schema requirements to reviewable controls.

## 14_HYPOTHESIS

A future static validator can convert each checklist row into a machine check.

## 15_REMAINING_GAP

- No automated evidence collection.
- No parser.
- No output report format.

## 16_TODO

- Future GO should add test fixtures for positive and negative policy drafts.
- Future GO should choose JSON Schema or a custom validator approach.

## 17_RESUME_POINT

Use this checklist before any future conversion of the Markdown draft into active YAML/JSON.

## 18_TO_DOCUMENT

Future validator docs should explain how each checklist row maps to a parser check and a verdict.

## 19_TO_REMEMBER

Checklist pass is documentation quality, not runtime permission.

## RISKS

- À qualifier.
