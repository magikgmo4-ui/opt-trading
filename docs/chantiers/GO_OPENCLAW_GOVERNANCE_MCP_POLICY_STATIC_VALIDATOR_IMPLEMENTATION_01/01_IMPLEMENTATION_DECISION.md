# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01 -- 01_IMPLEMENTATION_DECISION

## 1_MASTER_TARGET

Define the implementation decision for the first OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

Primary source documents:

- MCP Policy Schema;
- MCP Policy YAML Draft;
- Static Validator Spec;
- Fixture Corpus.

## 3_INITIAL_NEED

The implementation must turn the static validator spec into a local tool without weakening the governance boundary.

## 4_MASTER_PROJECT_PLAN

Create a module that validates explicitly provided local policy text or files, emits deterministic output, and never mutates inputs.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`

## 7_CANONICAL_STATE

Implementation files:

```text
modules/governance/__init__.py
modules/governance/openclaw_mcp_policy_validator/__init__.py
modules/governance/openclaw_mcp_policy_validator/__main__.py
modules/governance/openclaw_mcp_policy_validator/parser.py
modules/governance/openclaw_mcp_policy_validator/validator.py
modules/governance/openclaw_mcp_policy_validator/cli.py
modules/governance/openclaw_mcp_policy_validator/README.md
tests/test_openclaw_mcp_policy_validator.py
```

## 8_VALIDATED_PLAN

The module supports:

- strict local YAML subset parsing;
- schema completeness checks;
- policy version checks;
- runtime binding disabled check;
- no-secret policy check;
- canonical class checks;
- gate catalog checks;
- trace catalog checks;
- eval catalog checks;
- capability gate/trace/eval binding checks;
- never-allowed approval path checks;
- deny-by-default checks;
- strict worker scope checks;
- Ollama Lab bounded-action checks;
- deterministic JSON output;
- deterministic exit code.

## 9_SELECTED_SOLUTION

Parser decision:

```text
Use a local strict YAML subset parser instead of adding PyYAML.
```

Reason:

- `PyYAML` is not present in the local environment;
- no dependency installation is authorized by this GO;
- the parser can fail closed on unsupported YAML features;
- the accepted policy subset is enough for the current static tests.

Rejected features:

- YAML anchors;
- aliases;
- tabs;
- odd indentation;
- complex flow maps;
- ambiguous nested content.

CLI decision:

```powershell
python -m modules.governance.openclaw_mcp_policy_validator path\to\policy.yaml
```

Optional capability check:

```powershell
python -m modules.governance.openclaw_mcp_policy_validator path\to\policy.yaml --capability missing_tool
```

Exit code behavior:

- `0` for `PASS_POLICY_STATIC_VALIDATION`;
- `1` for fail, blocked, or need-more-evidence verdicts;
- argparse errors retain normal Python CLI failure behavior.

## 12_INVARIANTS

- The CLI reads only the local file explicitly passed as argument.
- The validator does not write policies.
- The validator does not create runtime config.
- The validator does not call MCP, Ollama, broker, Docker, or network.
- The validator does not read secrets.
- Secret-like detections are reported without echoing the risky value.
- Unknown capability remains blocked by default.
- `NEVER_ALLOWED` cannot have approval path.
- Runtime binding must be false.

## 13_ESTABLISHED

Implemented validation behaviors:

| Rule | Implemented behavior |
|---|---|
| `policy.id` required | Missing field returns `FAIL_SCHEMA_MISSING_FIELD`. |
| `policy.version` or `policy.policy_version` required | Missing field returns `FAIL_SCHEMA_MISSING_FIELD`. |
| `policy.runtime_binding` false only | `true` returns `FAIL_RUNTIME_BINDING_ENABLED`. |
| no-secret policy required | unsafe value returns `FAIL_SECRET_RISK`. |
| unknown class | returns `FAIL_UNKNOWN_CLASS`. |
| `WRITE_GATED` without gate | returns `FAIL_GATE_BINDING`. |
| `RUNTIME_GATED` without gate | returns `FAIL_GATE_BINDING`. |
| missing trace binding | returns `FAIL_TRACE_BINDING`. |
| missing eval binding | returns `FAIL_EVAL_BINDING`. |
| `NEVER_ALLOWED` approval path | returns `FAIL_NEVER_ALLOWED_APPROVAL_PATH`. |
| unknown capability request | returns `BLOCKED_WITH_REASON`. |
| secret-like value | returns `FAIL_SECRET_RISK` with value suppressed. |

## 14_HYPOTHESIS

The local YAML subset should remain acceptable until OpenClaw adopts a dedicated dependency and parser policy in a later GO.

## 15_REMAINING_GAP

Remaining implementation gaps:

- no Markdown fixture corpus extractor;
- no CI job;
- no JSON Schema export;
- no duplicate-key test beyond parser behavior;
- no policy migration assistant;
- no runtime policy loader by design.

## 16_TODO

Future implementation hardening:

- expand fixture coverage from the 37-documentary-fixture corpus;
- add parser tests for unsupported YAML features;
- add JSON report schema documentation;
- add CI draft only after governance approval.

## 17_RESUME_POINT

This file records the implementation choice so future work can extend the validator without changing its static/read-only boundary.

## 18_TO_DOCUMENT

Future docs should distinguish:

- static validation pass;
- human approval;
- runtime policy loading;
- CI enforcement.

## 19_TO_REMEMBER

`PASS_POLICY_STATIC_VALIDATION` is not runtime approval. It only means the draft passed static checks.

## RISKS

- À qualifier.
