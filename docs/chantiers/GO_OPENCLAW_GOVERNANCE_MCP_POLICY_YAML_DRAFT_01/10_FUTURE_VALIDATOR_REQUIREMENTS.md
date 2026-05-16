---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_FUTURE_VALIDATOR
doc_type: future_validator_requirements
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 10_FUTURE_VALIDATOR_REQUIREMENTS

## 1_MASTER_TARGET

Decrire le futur GO de validator MCP Policy sans l'implementer.

## 2_INITIAL_PROJECT_DOC

Inputs futurs probables :

- `02_POLICY_YAML_DRAFT.md`
- `03_POLICY_JSON_MAPPING_DRAFT.md`
- `04_CAPABILITY_CLASS_ENTRIES.md`
- `05_GATE_TRACE_EVAL_BINDINGS.md`
- `09_POLICY_DRAFT_VALIDATION_CHECKLIST.md`

## 3_INITIAL_NEED

Un futur validator devra transformer les regles documentaires en checks fail-closed. Ce GO ne doit pas creer ce validator.

## 4_MASTER_PROJECT_PLAN

Le futur GO devrait definir :

- parser YAML ;
- modele JSON interne ;
- champs obligatoires ;
- enums de classes ;
- references gates/traces/evals ;
- forbidden fields ;
- fail closed ;
- output verdict.

## 6_FINAL_TARGET

Specification future de validator, non executable dans ce chantier.

## 7_CANONICAL_STATE

Statut de ce fichier :

```text
validator_created: false
parser_created: false
runtime_binding: false
script_created: false
test_runner_created: false
```

## 8_VALIDATED_PLAN

Exigences futures :

| requirement_id | requirement | expected behavior |
| --- | --- | --- |
| `REQ_PARSE_YAML` | Parser un fichier YAML policy futur | reject invalid syntax, no implicit defaults except fail-closed |
| `REQ_VALIDATE_REQUIRED_FIELDS` | Valider champs requis | fail if id, version, default, class, gate, trace or eval missing |
| `REQ_VALIDATE_CLASS` | Valider `capability_class` | allow only canonical classes |
| `REQ_VALIDATE_DEFAULT_STATUS` | Valider default status explicite | fail if missing or permissive by omission |
| `REQ_VALIDATE_GATE_BINDING` | Verifier gate required/gate id | fail if sensitive capability lacks gate |
| `REQ_VALIDATE_TRACE_BINDING` | Verifier trace family exists | fail if unknown or missing |
| `REQ_VALIDATE_EVAL_BINDING` | Verifier eval profile exists | fail if unknown or missing |
| `REQ_VALIDATE_SECRET_POLICY` | Verifier no-secret policy | fail on missing policy or forbidden field |
| `REQ_VALIDATE_NEVER_ALLOWED` | Verifier no approval path | fail if gate or approval exists |
| `REQ_VALIDATE_ROLLBACK` | Verifier rollback for destructive actions | fail if absent |
| `REQ_VALIDATE_STRICT_WORKERS` | Verifier allowed/blocked and no self-approval | fail on overlap or missing no-self-approval |
| `REQ_VALIDATE_OLLAMA` | Verifier model pull/switch/restart/install gates | fail if any are read-only by mistake |
| `REQ_FAIL_CLOSED` | Unknown field/capability/action | return `BLOCKED_BY_DEFAULT` or `FAIL_POLICY` |
| `REQ_OUTPUT_VERDICT` | Output standard verdict | `PASS`, `FAIL`, `BLOCKED`, `NEED_MORE_EVIDENCE` with reason |

## 9_SELECTED_SOLUTION

Recommended future GO :

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01
```

Scope recommended for that GO :

- produce validator design only first, or implementation only if explicitly allowed ;
- decide YAML source path ;
- decide JSON Schema or custom checks ;
- define failure codes ;
- define fixture corpus ;
- prove no secret handling ;
- prove no runtime binding.

## 12_INVARIANTS

- This file is not a script.
- No parser is created here.
- No validator command is created here.
- No policy runtime is touched.
- Future validator must fail closed.
- Future validator must not display secret values.

## 13_ESTABLISHED

Validator requirements are now documented, but implementation remains future work.

## 14_HYPOTHESIS

JSON Schema may be sufficient for structural checks, but custom rules may be needed for cross-references and fail-closed decision order.

## 15_REMAINING_GAP

- No validator GO opened.
- No schema language selected.
- No fixture files.
- No command contract.
- No CI integration.

## 16_TODO

- Open a future GO only when policy draft content is accepted.
- Keep any validator separate from this doc-only GO.
- Require explicit approval before creating runtime-adjacent files.

## 17_RESUME_POINT

Next work should start from this requirements file and the YAML/JSON mapping, not from an ad hoc parser.

## 18_TO_DOCUMENT

Future validator must document how it handles `none`, `null`, missing fields, unknown fields and aliases.

## 19_TO_REMEMBER

A validator can check a policy, but it cannot make a forbidden action safe.
