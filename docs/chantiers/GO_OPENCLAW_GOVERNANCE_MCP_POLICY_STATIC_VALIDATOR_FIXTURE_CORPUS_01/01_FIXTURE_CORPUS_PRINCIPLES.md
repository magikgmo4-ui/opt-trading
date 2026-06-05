# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01 -- 01_FIXTURE_CORPUS_PRINCIPLES

## 1_MASTER_TARGET

Define the principles for a Markdown-only fixture corpus.

## 2_INITIAL_PROJECT_DOC

This document binds the fixture corpus to the static validator specification.

## 3_INITIAL_NEED

Fixtures must be useful later without becoming active policy inputs now.

## 4_MASTER_PROJECT_PLAN

The fixture corpus uses a stable documentation pattern:

```text
fixture_id:
purpose:
expected_verdict:
expected_error_code:
policy snippet:
why:
related_validator_rule:
related_gate:
related_trace:
related_eval:
```

## 6_FINAL_TARGET

Every fixture is deterministic, no-secret, Markdown-only, and mapped to a validator rule.

## 7_CANONICAL_STATE

Current GO state:

```text
active_yaml_created: false
active_json_created: false
executable_code_created: false
validator_created: false
runtime_binding_created: false
```

## 8_VALIDATED_PLAN

Fixture principles:

| Principle | Requirement |
|---|---|
| Documentation only | Fixtures live in `.md` files. |
| No active YAML/JSON | Snippets are fenced `text`, not standalone policy files. |
| No executable file | No script, runner, parser, command, config, or CI file. |
| No runtime binding | Every valid fixture keeps `runtime_binding: false`. |
| No real secret | Only fake placeholders are allowed in negative no-secret fixtures. |
| Deterministic verdict | Every fixture declares one expected verdict. |
| Error code for invalid fixtures | Every invalid fixture declares one expected error code. |
| Fail closed | Ambiguity maps to fail or blocked verdict. |
| Complete valid evidence | Valid fixtures prove class, gate, trace, and eval coherence. |

## 9_SELECTED_SOLUTION

Use Markdown sections and fenced `text` snippets. This preserves future test intent while preventing runtime interpretation.

Valid fixtures use:

```text
expected_error_code: none
```

Invalid fixtures use a single primary error code from the static validator catalog.

## 12_INVARIANTS

- No real secret values.
- No live token shapes.
- No raw environment dump.
- No executable examples.
- No runtime command execution.
- No active policy file.
- No self-approval.
- No trade permission.
- No unrestricted shell permission.
- `NEVER_ALLOWED` cannot be approvable.

## 13_ESTABLISHED

The prior validator spec established:

- `PASS_POLICY_STATIC_VALIDATION`;
- `FAIL_SCHEMA_MISSING_FIELD`;
- `FAIL_UNKNOWN_CLASS`;
- `FAIL_GATE_BINDING`;
- `FAIL_TRACE_BINDING`;
- `FAIL_EVAL_BINDING`;
- `FAIL_NEVER_ALLOWED_APPROVAL_PATH`;
- `FAIL_SECRET_RISK`;
- `FAIL_RUNTIME_BINDING_ENABLED`;
- `FAIL_POLICY`;
- `BLOCKED_WITH_REASON`;
- `NEED_MORE_EVIDENCE`.

## 14_HYPOTHESIS

Future test harnesses can extract `text` snippets by fixture id, but must not treat this corpus as a runtime policy source.

## 15_REMAINING_GAP

This file does not provide a parser, a fixture schema, or a runner.

## 16_TODO

- Apply this pattern across valid and invalid fixture files.
- Build a single index of expected verdicts.

## 17_RESUME_POINT

Resume point:

```text
All fixture files must follow the same metadata pattern.
```

## 18_TO_DOCUMENT

Future test harness requirements must explain how snippets are extracted, validated, and compared without runtime calls.

## 19_TO_REMEMBER

The corpus prepares tests; it is not itself a test suite.

## RISKS

- À qualifier.
