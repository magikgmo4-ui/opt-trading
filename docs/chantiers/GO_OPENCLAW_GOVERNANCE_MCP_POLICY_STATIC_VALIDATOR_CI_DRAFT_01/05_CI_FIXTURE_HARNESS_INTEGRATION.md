# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 05_CI_FIXTURE_HARNESS_INTEGRATION

## 1_MASTER_TARGET

Define how the fixture harness should be integrated into future CI.

## 2_INITIAL_PROJECT_DOC

The fixture harness is implemented in `modules/governance/openclaw_mcp_policy_validator/fixture_harness.py` and validated against the Markdown corpus.

## 3_INITIAL_NEED

Future CI must prove that the static validator still matches the canonical 37-fixture corpus and reports any mismatch or blocked extraction deterministically.

## 4_MASTER_PROJECT_PLAN

Document corpus source, canonical index, extraction rules, temporary storage behavior, comparison behavior, report expectations, and mismatch handling.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Corpus source:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/
```

Canonical index:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md
```

Current result:

```text
PASS_FIXTURE_HARNESS
total_fixtures=37
pass_count=37
fail_count=0
mismatches=0
warnings=4
```

## 8_VALIDATED_PLAN

Future CI harness flow:

1. Read the Markdown corpus directory.
2. Parse `09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`.
3. Open only referenced Markdown fixture files.
4. Extract fixture-marked fenced blocks.
5. Materialize snippets into temporary files outside the repository.
6. Run the local static validator against each temporary snippet.
7. Compare actual verdict and primary error code to the canonical index.
8. Return `PASS_FIXTURE_HARNESS`, `FAIL_FIXTURE_EXPECTATION_MISMATCH`, or `BLOCKED_WITH_REASON`.
9. Report fixture totals, pass count, fail count, mismatches, blocked reasons, and warning count.

## 9_SELECTED_SOLUTION

The fixture index remains canonical for expected verdicts and expected error codes. Inline fixture metadata may be parsed for drift detection, but future CI must not silently replace the index with inline values.

## 12_INVARIANTS

- Markdown corpus remains documentary.
- Snippets are not executed.
- Snippets are not loaded into runtime.
- Snippets are not committed as active YAML/JSON.
- Temporary files are outside the repository.
- Report output must not print snippet bodies.
- Mismatches fail future CI.
- Missing or ambiguous snippets block future CI.

## 13_ESTABLISHED

The harness has proven:

- 37 fixture rows are readable;
- 37 snippets are comparable;
- 0 mismatches exist against the canonical index;
- 4 inline/index warnings exist and are exposed.

## 14_HYPOTHESIS

Future CI can keep accepting current fixture-marked `text` fences. A later fixture hygiene GO can migrate to explicit `yaml` or `policy` fence labels if desired.

## 15_REMAINING_GAP

The harness does not currently fail on the 4 inline/index warnings. Activation must decide whether to resolve, accept, or make them hard failures.

## 16_TODO

Future CI activation must specify:

- exact corpus path;
- expected fixture count;
- expected warning policy;
- report output format;
- failure behavior for changed fixture count.

## 17_RESUME_POINT

Use `37` fixtures and `09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md` as the current baseline.

## 18_TO_DOCUMENT

Future changes to fixture count must update the fixture corpus closeout and CI activation documentation together.

## 19_TO_REMEMBER

Harness PASS is static corpus alignment only. It does not approve runtime policy use.

## RISKS

- À qualifier.
