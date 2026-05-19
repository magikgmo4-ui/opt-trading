---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_VALIDATION_RULES
doc_type: policy_validation_rules
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

# 09_POLICY_VALIDATION_RULES

## 1_MASTER_TARGET

Definir les validations statiques du futur schema policy MCP.

## 2_INITIAL_PROJECT_DOC

Base : field schema, class schema, gate binding, trace/eval binding and deny-by-default rules.

## 3_INITIAL_NEED

Prevenir les policies incompletes, permissives par omission ou incoherentes.

## 4_MASTER_PROJECT_PLAN

Chaque validation donne condition PASS, FAIL et BLOCKED.

## 6_FINAL_TARGET

Regles applicables avant toute promotion YAML/JSON.

## 7_CANONICAL_STATE

| Validation | PASS | FAIL | BLOCKED |
| --- | --- | --- | --- |
| Schema completeness | all mandatory fields present | missing mandatory field | schema source absent |
| Class validity | class in canonical enum | invalid class | class unknown |
| Default status explicit | `default_status` set | inferred/missing default | policy entry incomplete |
| Gate binding exists | sensitive class has correct `gate_id` | gate missing/wrong family | gate taxonomy missing |
| Trace binding exists | `trace_required=true` and family present | missing trace family | trace taxonomy missing |
| Eval binding exists | required eval list present | no eval for class/verdict | eval profile missing |
| Secret policy present | `secret_policy` explicit | absent secret policy | redaction profile unknown |
| Forbidden fields absent | input/output/trace exclude forbidden keys | forbidden key/value present | scan unavailable |
| Rollback rule present | destructive/write/runtime action has rollback or explicit none | required rollback absent | action risk unknown |
| Actor scope bounded | allowed and blocked actors explicit | `any` actor allowed without block | actor registry absent |
| Machine scope bounded | machine list explicit | broad wildcard without reason | machine split unavailable |
| Tool scope named | named tools only | unrestricted shell or free command | tool manifest missing |
| Gate decision valid | action exact, evidence, approver, rollback, no self-approval | vague/self approval | decision absent |
| Trace no-secret | no secret value in trace | secret value present | scan unavailable |
| Final verdict valid | verdict from canonical list with evidence refs | unsupported PASS/FAIL/BLOCKED | evidence missing |
| Doc-only compliance | only chantier docs and inbox local changed | runtime/code/global index changed | diff unavailable |

## 8_VALIDATED_PLAN

Validation order :

```text
1 schema completeness
2 enum validity
3 default_status explicit
4 secret policy
5 actor/machine/tool scope
6 gate binding
7 trace binding
8 eval binding
9 rollback
10 final verdict
```

## 9_SELECTED_SOLUTION

Validation is fail-closed :

```text
unknown -> BLOCKED
missing -> FAIL_POLICY
ambiguous -> NEED_MORE_EVIDENCE
```

## 12_INVARIANTS

- No warning-only promotion for sensitive missing fields.
- No PASS when scanner/evidence is unavailable.
- No runtime fallback.
- No auto-fix.

## 13_ESTABLISHED

The requested validation families are covered :

- schema completeness ;
- class validity ;
- gate binding exists ;
- trace binding exists ;
- eval binding exists ;
- secret policy present ;
- default status explicit ;
- forbidden fields absent ;
- rollback rule present for destructive actions.

## 14_HYPOTHESIS

Future validation can be implemented as static lint without contacting runtime services.

## 15_REMAINING_GAP

No validator implementation is created in this GO.

## 16_TODO

Future GO can create a warning-only static policy linter.

## 17_RESUME_POINT

Use this checklist before accepting any YAML/JSON translation.

## 18_TO_DOCUMENT

Future validator output should map to canonical verdicts.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw policy validation is fail-closed: missing class, gate, trace, eval, secret policy, default or rollback blocks promotion.
```
