# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01 -- 01_HARNESS_DESIGN

## 1_MASTER_TARGET

Define the fixture harness design for OpenClaw MCP Policy static validation.

## 2_INITIAL_PROJECT_DOC

Design sources:

- fixture corpus principles;
- fixture expected verdict index;
- static validator implementation;
- future harness requirements from the corpus GO.

## 3_INITIAL_NEED

The corpus is Markdown-only and contains conceptual snippets. The harness needs to run those snippets through the validator without turning them into active policy files.

## 4_MASTER_PROJECT_PLAN

The harness:

1. reads the fixture corpus directory;
2. parses `09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`;
3. opens only referenced Markdown fixture files;
4. extracts fenced blocks containing `fixture_id` and `policy_snippet`;
5. materializes each conceptual snippet into a temporary policy YAML input;
6. runs `validate_policy_file` locally;
7. compares actual verdict and primary error code to the index;
8. emits deterministic JSON or text.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01`

## 7_CANONICAL_STATE

Harness entrypoint:

```powershell
python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs\chantiers\GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
```

Output verdicts:

```text
PASS_FIXTURE_HARNESS
FAIL_FIXTURE_EXPECTATION_MISMATCH
BLOCKED_WITH_REASON
```

## 8_VALIDATED_PLAN

Extraction rule:

```text
A fenced block is a fixture block only if it contains:
- fixture_id:
- expected_verdict:
- expected_error_code:
- policy_snippet:
```

The current corpus uses `text` fences. The harness accepts them because the content itself is explicitly fixture-marked.

## 9_SELECTED_SOLUTION

Materialization rule:

- full policy snippets are completed only with safe missing boilerplate when the fixture is not testing that section as absent;
- capability snippets are wrapped in a minimal static policy document;
- strict worker snippets are wrapped under `strict_worker_roles`;
- final verdict trace fixtures can remove `TRACE_VERDICT` from the temporary policy;
- no materialized file is written into the repository.

Expected verdict source:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md
```

Inline fixture expectations are parsed. When inline text differs from the index, the report records a warning and still compares against the index.

## 12_INVARIANTS

- The harness reads Markdown only from the corpus.
- The harness writes temporary YAML only in system temp storage.
- The harness does not create active repo YAML or JSON.
- The harness does not execute snippets.
- The harness calls only the local static validator.
- The harness does not call MCP, Ollama, OpenClaw runtime, Docker, broker, or network.
- The harness does not print snippet bodies.
- The harness fails closed on missing snippet, duplicate fixture block, missing index row, or malformed fixture block.

## 13_ESTABLISHED

Implemented files:

```text
modules/governance/openclaw_mcp_policy_validator/fixture_harness.py
tests/test_openclaw_mcp_policy_fixture_harness.py
```

Validator rule updates:

- strict worker requested capability outside role scope is reported;
- strict worker missing nested output verdict is reported;
- unrestricted shell allowed policy is reported;
- audit trace suppression allowed policy is reported;
- trade execution or human gate bypass allowed policy is reported.

These updates align validator behavior with the 37-fixture corpus.

## 14_HYPOTHESIS

Future fixture files may use explicit `yaml` fixture fences. The current harness can keep accepting fixture-marked `text` fences for backward compatibility.

## 15_REMAINING_GAP

Remaining design gaps:

- no CI integration;
- no fixture result artifact committed to repo;
- no HTML report;
- no runtime policy promotion;
- no mutation of source fixtures.

## 16_TODO

Future hardening:

- add optional strict mode that fails on index vs inline expectation drift;
- add report schema documentation;
- add CI draft after governance approval;
- add more parser edge-case tests.

## 17_RESUME_POINT

The harness now connects the validator to the fixture corpus while keeping the corpus documentary.

## 18_TO_DOCUMENT

Closeout must include total fixtures, pass count, fail count, warnings, and mismatch count.

## 19_TO_REMEMBER

Harness pass proves static expectation alignment only. It does not approve runtime policy use.

## RISKS

- À qualifier.
