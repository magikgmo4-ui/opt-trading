# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 02_CI_COMMAND_MATRIX

## 1_MASTER_TARGET

Define the future CI command matrix for the MCP Policy static validator and fixture harness.

## 2_INITIAL_PROJECT_DOC

The commands are derived from the validator and harness closeouts. They are future CI commands only and are not activated by this GO.

## 3_INITIAL_NEED

CI must run the exact local evidence commands that proved the validator and harness, while adding repository hygiene checks that remain no-runtime and no-secret.

## 4_MASTER_PROJECT_PLAN

Document each future command with objective, preconditions, expected output, fail condition, and associated forbidden behavior.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Current known passing evidence from previous GO:

```text
python -m pytest tests\test_openclaw_mcp_policy_validator.py -q
=> 12 passed

python -m pytest tests\test_openclaw_mcp_policy_fixture_harness.py -q
=> 4 passed

python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs\chantiers\GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
=> PASS_FIXTURE_HARNESS, 37 PASS, 0 FAIL, 0 mismatch
```

## 8_VALIDATED_PLAN

| Future command | Objective | Preconditions | Expected output | Fail condition | Forbidden behavior covered |
|---|---|---|---|---|---|
| `python -m pytest tests/test_openclaw_mcp_policy_validator.py -q` | Run validator unit tests. | Python and test dependency available. | `12 passed` or updated passing count. | Any failed test or import error. | Runtime binding, MCP live, Ollama, trade, sudo, secret read. |
| `python -m pytest tests/test_openclaw_mcp_policy_fixture_harness.py -q` | Run harness unit tests. | Corpus and harness module present. | `4 passed` or updated passing count. | Any failed test or import error. | Active repo YAML/JSON creation, ambiguous snippet handling, missing snippet handling. |
| `python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01` | Run real corpus comparison. | Canonical fixture index present. | `PASS_FIXTURE_HARNESS`, total `37`, pass `37`, fail `0`. | Any mismatch, blocked reason, parse error, missing fixture, or unexpected count. | Runtime loading, secret output, uncontrolled fixture extraction. |
| `git diff --check` | Detect whitespace errors in the diff. | Git checkout available. | No output and exit code `0`. | Any whitespace error. | Churn and invalid patch hygiene. |

## 9_SELECTED_SOLUTION

The command matrix intentionally excludes:

- service start or restart;
- Docker;
- network calls from the validator or harness;
- MCP live calls;
- Ollama calls;
- broker or trade calls;
- secret reads;
- environment dumps;
- workflow dispatch.

## 12_INVARIANTS

- Commands are future CI candidates, not executed by this doc.
- Commands must remain local static checks.
- Commands must not create active policy files in the repository.
- Commands must not mutate policy drafts.
- Commands must fail closed.

## 13_ESTABLISHED

The existing validator and harness already support deterministic local execution. The future CI should preserve their current command surfaces.

## 14_HYPOTHESIS

Future CI may install `pytest` if needed. Dependency installation is outside validator behavior and must not be confused with validator network access.

## 15_REMAINING_GAP

No active CI job exists. No workflow permissions, runner image, dependency lock, or report artifact has been approved.

## 16_TODO

Future activation must decide:

- Python version;
- dependency installation method;
- report artifact retention;
- warning strictness;
- workflow trigger paths.

## 17_RESUME_POINT

Use this matrix as the command source when drafting the future workflow.

## 18_TO_DOCUMENT

If test counts change before activation, the activation GO must record the new counts and explain the change.

## 19_TO_REMEMBER

Passing static tests do not approve runtime policy use.

## RISKS

- À qualifier.
