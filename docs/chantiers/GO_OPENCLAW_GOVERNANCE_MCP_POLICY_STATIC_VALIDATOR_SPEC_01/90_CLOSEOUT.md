# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 90_CLOSEOUT

## 1_MASTER_TARGET

Close the doc-only static validator specification chantier.

## 2_INITIAL_PROJECT_DOC

The governance chain now extends to a static validator specification:

```text
Reconciliation
-> MCP Boundary
-> Human Review Gates
-> Trace / Evals Profile
-> MCP Policy Schema
-> MCP Policy YAML Draft
-> MCP Policy Static Validator Spec
```

## 3_INITIAL_NEED

OpenClaw needed a complete non-executable specification for a future static validator before creating code, fixture files, or runtime integration.

## 4_MASTER_PROJECT_PLAN

Completed documentation set:

```text
00_CADRAGE.md
01_STATIC_VALIDATOR_PRINCIPLES.md
02_INPUT_OUTPUT_CONTRACT.md
03_SCHEMA_VALIDATION_RULES.md
04_CAPABILITY_CLASS_VALIDATION_RULES.md
05_GATE_TRACE_EVAL_BINDING_RULES.md
06_NEVER_ALLOWED_AND_DENY_DEFAULT_RULES.md
07_NO_SECRET_STATIC_CHECKS.md
08_VERDICT_AND_ERROR_CATALOG.md
09_CONCEPTUAL_FIXTURES.md
10_FUTURE_IMPLEMENTATION_PLAN.md
90_CLOSEOUT.md
```

Local inbox entry:

```text
docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01.md
```

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01`

Target met if verification confirms:

- validator spec complete;
- no executable validator created;
- fail-closed explicit;
- deny-by-default explicit;
- `NEVER_ALLOWED` approval path rule explicit;
- no-secret checks defined;
- verdicts and errors standardized;
- fixtures conceptual only;
- global indexes untouched;
- runtime untouched;
- next GO clear.

## 7_CANONICAL_STATE

Documented outputs:

- static validator principles;
- input and output contract;
- required schema fields;
- capability class validation rules;
- gate, trace, and eval binding rules;
- never-allowed and deny-by-default rules;
- no-secret static checks;
- verdict and error catalog;
- conceptual fixtures;
- future implementation plan.

## 8_VALIDATED_PLAN

Validation scope covered:

| Area | Covered |
|---|---:|
| Input files | Yes |
| Expected YAML structure | Yes |
| Required fields | Yes |
| Allowed enum values | Yes |
| Class consistency | Yes |
| Gate binding consistency | Yes |
| Trace binding consistency | Yes |
| Eval binding consistency | Yes |
| Strict worker binding consistency | Yes |
| Ollama Lab binding consistency | Yes |
| Deny-by-default enforcement | Yes |
| Never-allowed enforcement | Yes |
| No-secret checks | Yes |
| Fail-closed behavior | Yes |
| Output verdicts | Yes |

## 9_SELECTED_SOLUTION

The selected solution is doc-only:

```text
Specification now.
Fixture corpus later.
Implementation later.
Runtime binding not in scope.
```

Recommended NEXT_GO:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
```

Purpose:

```text
Create a no-secret, non-runtime fixture corpus for the static validator before implementation.
```

## 12_INVARIANTS

Maintained:

- documentation only;
- no executable code;
- no real validator;
- no runtime;
- no trade;
- no sudo;
- no secret;
- no unrestricted shell capability;
- no merge;
- no forced push;
- no cleanup;
- no auto-fix;
- no global index modification;
- no `git add -A`;
- stage only current chantier and inbox;
- unknown capability blocked by default;
- `NEVER_ALLOWED` has no approval path;
- future validator must fail closed.

## 13_ESTABLISHED

Established by this chantier:

- static validation is read-only evidence, not approval;
- `PASS_POLICY_STATIC_VALIDATION` does not authorize runtime use;
- `runtime_binding: true` must produce `FAIL_RUNTIME_BINDING_ENABLED`;
- missing required schema fields produce `FAIL_SCHEMA_MISSING_FIELD`;
- unknown class produces `FAIL_UNKNOWN_CLASS`;
- missing gate, trace, or eval bindings produce dedicated failures;
- secret risk produces `FAIL_SECRET_RISK` with value suppression;
- `NEVER_ALLOWED` with approval path other than `none` produces `FAIL_NEVER_ALLOWED_APPROVAL_PATH` and final policy failure;
- conceptual fixtures are documentation only.

Force-add exception:

```text
Path:
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/07_NO_SECRET_STATIC_CHECKS.md

Reason:
the repository ignore rule blocks paths containing SECRET.

Decision:
force-add is acceptable for this exact documentation file because the content is a no-secret static check specification, contains no secret value, and is part of the required chantier deliverables.
```

## 14_HYPOTHESIS

Future implementation may choose Python, Node.js, Rust, or another repo-approved language, but must preserve this specification.

## 15_REMAINING_GAP

Remaining gaps:

- fixture corpus not created;
- validator implementation not created;
- parser behavior not implemented;
- JSON output schema not implemented;
- CI integration not drafted;
- runtime binding not created.

These are intentionally out of scope for this GO.

## 16_TODO

Before future implementation:

- accept this spec;
- create fixture corpus or approve direct implementation GO;
- define parser behavior for duplicate keys and YAML anchors;
- define JSON output schema version;
- define static tests.

## 17_RESUME_POINT

Resume point:

```text
Static validator spec is ready for review.
Next recommended step: fixture corpus GO.
```

## 18_TO_DOCUMENT

When closing future fixture or implementation GO, document:

- files created;
- no-secret verification;
- no runtime touch;
- no policy mutation;
- expected verdict coverage;
- failure precedence.

## 19_TO_REMEMBER

Verdict for this GO after verification:

```text
PASS_DOC_ONLY
```

If verification finds executable artifacts, global index edits, runtime touch, or secret risk, the verdict becomes:

```text
BLOCKED_WITH_REASON
```

## RISKS

- À qualifier.
