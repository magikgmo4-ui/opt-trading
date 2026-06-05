# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 10_FUTURE_IMPLEMENTATION_PLAN

## 1_MASTER_TARGET

Document a future implementation plan without implementing the validator.

## 2_INITIAL_PROJECT_DOC

This plan follows the static validator specification created in this chantier.

## 3_INITIAL_NEED

After documentation review, a future GO may implement a read-only static validator. That future implementation must preserve fail-closed behavior and no runtime binding.

## 4_MASTER_PROJECT_PLAN

Future implementation may define:

- implementation language;
- module layout;
- parser rules;
- fixture files;
- tests;
- CI hook;
- read-only command;
- JSON output.

None of those artifacts are created in this GO.

## 6_FINAL_TARGET

The final target is a safe bridge from doc specification to later implementation.

## 7_CANONICAL_STATE

Current GO state:

```text
validator_code_created: false
parser_created: false
runner_created: false
runtime_binding_created: false
ci_created: false
fixture_files_created: false
```

## 8_VALIDATED_PLAN

Future implementation options:

| Area | Possible future choice | Constraint |
|---|---|---|
| Language | Python, Node.js, Rust, or another repo-approved toolchain. | Must be read-only and deterministic. |
| Parser | YAML parser plus structural checks. | Must reject ambiguity and fail closed. |
| Output | JSON summary plus human-readable summary. | Must not print secret values. |
| Fixtures | Dedicated fixture directory. | Must be no-secret and explicit expected verdict. |
| Tests | Static unit tests and fixture tests. | No runtime calls, no trade, no sudo. |
| CI | Optional future check. | Must not load runtime policy. |
| Command | Read-only validator command. | No auto-fix and no policy mutation. |

## 9_SELECTED_SOLUTION

Recommended future GO sequence:

1. `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`
   - Create non-secret fixture files from the conceptual fixtures.
   - Still no runtime binding.
2. `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`
   - Implement read-only parser and validator.
   - Validate fixture corpus.
   - Emit JSON output.
   - Fail closed.
3. `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`
   - Draft CI integration after implementation is validated.
   - Keep runtime binding disabled.

Implementation guardrails:

- parser reads policy files only;
- validator does not write policy files;
- no auto-fix;
- no runtime API calls;
- no MCP server start;
- no Ollama service restart;
- no model pull;
- no trade;
- no secret output;
- no unrestricted shell capability;
- no sudo;
- no merge or push as part of validation.

## 12_INVARIANTS

- Future implementation must fail closed.
- Future command must be read-only.
- Future output must suppress secret-like values.
- Future tests must be static.
- Runtime binding remains outside implementation until a dedicated governance GO.

## 13_ESTABLISHED

This spec defines the validation target. Any future implementation that cannot satisfy the spec must fail review before merge.

## 14_HYPOTHESIS

Python may be the simplest future implementation language because of mature YAML parsing and testing tools, but the language is not selected by this GO.

## 15_REMAINING_GAP

Open questions for a future implementation GO:

- exact parser library;
- duplicate key behavior;
- YAML anchor policy;
- path reporting format;
- JSON output schema version;
- fixture directory path;
- CI trigger policy.

## 16_TODO

- Review this spec.
- Choose next GO.
- Create fixture corpus before or together with implementation, depending on governance preference.

## 17_RESUME_POINT

Resume point:

```text
Do not implement validator until this spec is accepted.
```

## 18_TO_DOCUMENT

Future implementation closeout must prove:

- no runtime touched;
- no secret printed;
- no policy file mutated;
- all fixtures pass expected verdicts;
- fail-closed behavior tested.

## 19_TO_REMEMBER

Static validation is a precondition for policy use, not a replacement for human gates or runtime safeguards.

## RISKS

- À qualifier.
