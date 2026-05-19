# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01 -- 00_CADRAGE

## 1_MASTER_TARGET

Create a local read-only fixture harness for the OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

This GO follows:

```text
MCP Policy Static Validator Spec
-> MCP Policy Static Validator Fixture Corpus
-> MCP Policy Static Validator Implementation
-> MCP Policy Static Validator Fixture Harness
```

## 3_INITIAL_NEED

The validated Markdown corpus has 37 conceptual fixtures. The static validator now needs a harness that extracts those fixtures, materializes safe temporary policy files, runs the validator, and compares actual results with expected verdicts.

## 4_MASTER_PROJECT_PLAN

Plan:

1. Verify Git state.
2. Create the dedicated branch.
3. Read the static validator implementation.
4. Read the fixture corpus and canonical fixture index.
5. Implement `fixture_harness.py`.
6. Add local unit tests.
7. Update safe usage README.
8. Create chantier docs and inbox.
9. Run targeted tests and checks.
10. Stage only scoped files and commit.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01`

Expected GO verdict:

```text
PASS_FIXTURE_HARNESS
```

## 7_CANONICAL_STATE

Initial principal worktree state:

```text
worktree:
C:\Users\ghost\opt-trading

git status --short --branch:
## sot/mainline...origin/sot/mainline

git branch --show-current:
sot/mainline

git log --oneline -5:
53b5811f docs: audit admin-trading monitoring and secrets (#403)
ed4f8dc7 feat: implement risk limits and kill switch for admin-trading
c243df62 Merge pull request #401 from magikgmo4-ui/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_01
7eac3649 docs: closeout PASS_GATED - OpenClaw builder first local execution plan
9b707c94 Merge pull request #400 from magikgmo4-ui/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_CONTROLLED_JOB_01

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Dedicated worktree:

```text
C:\Users\ghost\opt-trading-mcp-policy-static-validator-fixture-harness
```

Dedicated branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01
```

Branch base:

```text
561a3ed5 feat: implement OpenClaw MCP policy static validator
```

Dedicated branch verification:

```text
git status --short --branch:
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01

git branch --show-current:
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01

git log --oneline -5:
561a3ed5 feat: implement OpenClaw MCP policy static validator
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
248b6c38 docs: specify OpenClaw MCP policy static validator
1403a3e6 docs: draft OpenClaw MCP policy YAML
fa7558f2 docs: define OpenClaw MCP policy schema

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

## 8_VALIDATED_PLAN

Sources read:

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01/`
- `modules/governance/openclaw_mcp_policy_validator/`
- `tests/test_openclaw_mcp_policy_validator.py`

## 9_SELECTED_SOLUTION

Add:

```text
modules/governance/openclaw_mcp_policy_validator/fixture_harness.py
tests/test_openclaw_mcp_policy_fixture_harness.py
```

Update:

```text
modules/governance/openclaw_mcp_policy_validator/README.md
modules/governance/openclaw_mcp_policy_validator/validator.py
```

The harness uses the canonical fixture index as the expected verdict source and parses fixture fences for snippets.

## 12_INVARIANTS

- Local static harness only.
- Read Markdown fixtures only.
- No runtime binding.
- No live MCP call.
- No OpenClaw runtime action.
- No Ollama call.
- No trade.
- No sudo.
- No secret read.
- No environment dump.
- No network call.
- No policy auto-fix.
- No active YAML or JSON files added to repo.
- Snippets are written only to system temporary files.
- Reports do not print snippet content.
- Global indexes not modified.
- `git add -A` not used.

## 13_ESTABLISHED

Harness verdicts:

- `PASS_FIXTURE_HARNESS`
- `FAIL_FIXTURE_EXPECTATION_MISMATCH`
- `BLOCKED_WITH_REASON`

Harness report includes:

- total fixture count;
- pass count;
- fail count;
- mismatches;
- per-fixture results;
- warnings;
- blocked reasons.

## 14_HYPOTHESIS

The fixture index is the canonical expected verdict source. Inline expectation fields in fixture blocks are parsed, but index values win when the two differ.

## 15_REMAINING_GAP

Remaining gaps at cadrage:

- no CI integration;
- no active runtime policy loading;
- no repo-level fixture YAML files;
- no network or live service checks;
- no policy auto-fix.

## 16_TODO

- Implement harness.
- Add tests.
- Run validator tests.
- Run harness tests.
- Run harness against real corpus.
- Run Git and content checks.
- Stage scoped files.
- Commit.

## 17_RESUME_POINT

Static validator implementation passed at:

```text
561a3ed5 feat: implement OpenClaw MCP policy static validator
```

This GO connects that validator to the 37-fixture Markdown corpus.

## 18_TO_DOCUMENT

Document:

- extraction rules;
- materialization rules;
- temp-file boundary;
- test commands;
- corpus pass/fail counts;
- metadata warnings;
- remaining next GO.

## 19_TO_REMEMBER

The fixture harness is not a runtime policy loader. It is only a static test runner for documentary fixtures.
