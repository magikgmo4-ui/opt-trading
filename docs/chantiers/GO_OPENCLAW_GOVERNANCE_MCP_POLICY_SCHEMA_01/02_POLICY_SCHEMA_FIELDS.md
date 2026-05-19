---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_FIELDS
doc_type: policy_schema_fields
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

# 02_POLICY_SCHEMA_FIELDS

## 1_MASTER_TARGET

Definir les champs conceptuels du schema policy MCP.

## 2_INITIAL_PROJECT_DOC

Base : MCP capability matrix, gate taxonomy, MCP tool call trace schema et eval profile.

## 3_INITIAL_NEED

Rendre chaque policy entry verifiable et traduisible plus tard en YAML/JSON, sans execution.

## 4_MASTER_PROJECT_PLAN

Chaque champ indique :

- nom ;
- type conceptuel ;
- obligatoire ou optionnel ;
- valeurs permises ;
- exemple ;
- erreurs possibles ;
- lien avec gate/trace/eval.

## 6_FINAL_TARGET

Schema conceptuel complet pour une entree `capability_policy`.

## 7_CANONICAL_STATE

| Champ | Type conceptuel | Obligation | Valeurs permises | Exemple | Erreurs possibles | Lien gate/trace/eval |
| --- | --- | --- | --- | --- | --- | --- |
| `policy_id` | string stable | obligatoire | id unique policy | `POLICY_REPO_STATE_READ` | duplicate, empty | reference trace/eval |
| `policy_version` | string semver/doc version | obligatoire | `draft_01`, `v1` later | `draft_01` | missing version | eval schema completeness |
| `capability_id` | string stable | obligatoire | lowercase snake/canonical id | `repo_state` | unknown, duplicate | trace field `CAPABILITY` |
| `capability_class` | enum | obligatoire | `READ_ONLY`, `READ_SANITIZED`, `WRITE_GATED`, `RUNTIME_GATED`, `HUMAN_APPROVAL_REQUIRED`, `BLOCKED_BY_DEFAULT`, `NEVER_ALLOWED` | `READ_ONLY` | invalid class | gate binding + MCP boundary eval |
| `default_status` | enum | obligatoire | `ALLOW_IF_BOUNDED`, `ALLOW_IF_SANITIZED`, `BLOCKED_BY_DEFAULT`, `NEEDS_GATE`, `NEVER_ALLOWED` | `BLOCKED_BY_DEFAULT` | implicit default | deny eval |
| `allowed_actor` | list enum/string | obligatoire | `Codex`, `OpenClawGovernor`, `StrictWorker:<role>`, `HumanOwner`, `MCPTool:<id>` | `Codex` | actor too broad | worker scope eval |
| `blocked_actor` | list enum/string | obligatoire | same namespace plus `any_unlisted` | `any_unlisted` | missing blocked actor | deny eval |
| `machine_scope` | list enum | obligatoire | `repo`, `cursor-ai`, `db-layer`, `student`, `admin-trading`, `fantome`, `all_repo_machines` | `repo` | wildcard unsafe | machine split compliance |
| `tool_scope` | list string | obligatoire | named tool ids only | `git_status_read` | unrestricted shell, empty for action | MCP call trace |
| `input_policy` | object | obligatoire | input summary, allowed params, forbidden params | `path=docs/chantiers/<GO>` | raw secret, raw env, command payload | no secret eval |
| `output_policy` | object | obligatoire | summary, artifact type, sanitization | `status summary` | raw logs, secret values | trace completeness |
| `secret_policy` | enum/object | obligatoire | `NO_SECRET_VALUES`, `METADATA_ONLY`, `REDACT_REQUIRED`, `NEVER_READ` | `NO_SECRET_VALUES` | absent secret policy | no secret eval |
| `gate_required` | boolean | obligatoire | `true`, `false` | `true` | omitted for sensitive class | gate required eval |
| `gate_id` | enum or null | obligatoire when `gate_required=true`; explicit `none` otherwise | Human gate taxonomy ids | `GATE_MCP_WRITE` | missing, wrong family | gate approval eval |
| `trace_required` | boolean | obligatoire | always `true` for current schema | `true` | false or omitted | trace completeness |
| `trace_family` | enum/list | obligatoire | `TRACE_MCP_CALL`, `TRACE_HUMAN_GATE`, `TRACE_RUNTIME_READ`, etc. | `TRACE_MCP_CALL` | missing binding | trace completeness |
| `eval_required` | list enum | obligatoire | `EVAL_*` ids | `EVAL_MCP_BOUNDARY_COMPLIANCE` | missing eval | final verdict validity |
| `rollback_required` | boolean | obligatoire | `true`, `false` | `false` | missing for destructive/runtime | rollback eval |
| `rollback_policy` | object/string | obligatoire if rollback required; explicit `none` otherwise | plan, artifact, owner | `revert patch` | vague rollback | rollback eval |
| `verdicts` | list enum | obligatoire | final verdicts allowed for this capability | `PASS_DOC_ONLY`, `BLOCKED_BY_POLICY` | unsupported PASS | verdict eval |
| `escalation_path` | list enum/string | obligatoire | `HumanOwner`, `OpenClawGovernor`, `SecurityOwner`, `TradingOwner`, `OpsGO` | `HumanOwner` | self-approval path | gate approval eval |
| `forbidden_fields` | list string | obligatoire | field names/payload keys forbidden in input/output/trace | `secret_value`, `raw_env`, `api_key` | absent forbidden list | no secret eval |
| `evidence_required` | list string | obligatoire | refs required before verdict | `diff_summary`, `source_refs` | PASS without evidence | final verdict eval |
| `risk_level` | enum | obligatoire | `low`, `medium`, `high`, `critical` | `medium` | risk omitted | gate selection |
| `promotion_status` | enum | obligatoire | `doc_only`, `candidate_for_yaml`, `blocked`, `never` | `doc_only` | executable status in doc GO | doc-only eval |

## 8_VALIDATED_PLAN

Minimal conceptual shape :

```text
capability_policy:
  policy_id:
  policy_version:
  capability_id:
  capability_class:
  default_status:
  allowed_actor:
  blocked_actor:
  machine_scope:
  tool_scope:
  input_policy:
  output_policy:
  secret_policy:
  gate_required:
  gate_id:
  trace_required:
  trace_family:
  eval_required:
  rollback_required:
  rollback_policy:
  verdicts:
  escalation_path:
  forbidden_fields:
  evidence_required:
  risk_level:
  promotion_status:
```

## 9_SELECTED_SOLUTION

The schema is positive and explicit. Optional fields are avoided for safety-critical bindings; use explicit `none` instead of omission.

## 12_INVARIANTS

- `trace_required` is always true.
- `secret_policy` is never optional.
- `default_status` is never inferred.
- `tool_scope` cannot contain generic shell.
- `NEVER_ALLOWED` cannot have approving `gate_id`.

## 13_ESTABLISHED

The required prompt fields are covered and extended with validation-support fields.

## 14_HYPOTHESIS

Future YAML/JSON may split nested objects into typed schemas.

## 15_REMAINING_GAP

No JSON Schema file generated in this GO.

## 16_TODO

Map these fields to classes in `03_CAPABILITY_POLICY_CLASSES.md`.

## 17_RESUME_POINT

Any missing field in a future policy entry should return `FAIL_POLICY`.

## 18_TO_DOCUMENT

When the runtime schema GO opens, convert this table into JSON Schema or YAML schema.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
An OpenClaw MCP policy entry is complete only when class, default, actors, scopes, secret policy, gate, trace, eval, rollback, verdicts and escalation are explicit.
```
