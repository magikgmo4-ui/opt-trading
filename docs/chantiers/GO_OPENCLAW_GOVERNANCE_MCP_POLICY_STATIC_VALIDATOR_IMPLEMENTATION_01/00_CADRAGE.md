# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01 -- 00_CADRAGE

## 1_MASTER_TARGET

Implement a local static OpenClaw MCP Policy validator that can inspect policy YAML test inputs before any runtime use.

## 2_INITIAL_PROJECT_DOC

This implementation follows the established governance chain:

```text
MCP Boundary
-> Human Review Gates
-> Trace / Evals Profile
-> MCP Policy Schema
-> MCP Policy YAML Draft
-> MCP Policy Static Validator Spec
-> MCP Policy Static Validator Fixture Corpus
-> MCP Policy Static Validator Implementation
```

## 3_INITIAL_NEED

OpenClaw needs a deterministic validator that can fail closed on incomplete, unsafe, or ambiguous MCP policy drafts without loading the policy into a runtime.

## 4_MASTER_PROJECT_PLAN

Plan:

1. Verify Git state.
2. Create a dedicated implementation branch from the fixture corpus branch.
3. Read the schema, YAML draft, validator spec, fixture corpus, and governance sources.
4. Implement a local Python module with:
   - strict YAML subset parser;
   - schema checks;
   - capability class checks;
   - gate binding checks;
   - trace binding checks;
   - eval binding checks;
   - no-secret checks;
   - never-allowed and deny-by-default checks;
   - deterministic JSON output;
   - deterministic exit code.
5. Add unit tests using temporary fake policy files only.
6. Document usage and closeout.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`

Expected final verdict:

```text
PASS_IMPLEMENTATION_STATIC_VALIDATOR
```

## 7_CANONICAL_STATE

Initial Git state in the principal worktree:

```text
worktree:
C:\Users\ghost\opt-trading

git status --short --branch:
## sot/mainline...origin/sot/mainline

git branch --show-current:
sot/mainline

git log --oneline -5:
ed4f8dc7 feat: implement risk limits and kill switch for admin-trading
c243df62 Merge pull request #401 from magikgmo4-ui/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_01
7eac3649 docs: closeout PASS_GATED - OpenClaw builder first local execution plan
9b707c94 Merge pull request #400 from magikgmo4-ui/go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_CONTROLLED_JOB_01
b0f5393b docs: closeout PASS_GATED - OpenClaw builder first controlled job gate defined

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Dedicated implementation worktree:

```text
C:\Users\ghost\opt-trading-mcp-policy-static-validator-implementation
```

Dedicated branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01
```

Branch base:

```text
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
```

Dedicated branch verification:

```text
git status --short --branch:
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01

git branch --show-current:
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01

git log --oneline -5:
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
248b6c38 docs: specify OpenClaw MCP policy static validator
1403a3e6 docs: draft OpenClaw MCP policy YAML
fa7558f2 docs: define OpenClaw MCP policy schema
e34b9952 Merge pull request #343 from magikgmo4-ui/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

## 8_VALIDATED_PLAN

Validated source reads:

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01` via branch reference
- `GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01` via branch reference
- `GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01` via branch reference
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/08_VERDICT_AND_ERROR_CATALOG.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`

## 9_SELECTED_SOLUTION

Selected implementation location:

```text
modules/governance/openclaw_mcp_policy_validator/
```

Rationale:

- importable Python module;
- compatible with existing `pytest` tests;
- avoids placing a static validator among operational shell scripts;
- keeps CLI local and explicit through `python -m`.

## 12_INVARIANTS

- Static local implementation only.
- Read-only input behavior.
- No OpenClaw runtime binding.
- No live MCP call.
- No Ollama runtime call.
- No trade.
- No sudo.
- No secret read.
- No environment dump.
- No policy auto-fix.
- No merge.
- No force push.
- No branch cleanup.
- No global index modification.
- Do not use `git add -A`.
- Stage only the current chantier, local inbox, validator module, tests, and safe README.
- Validator output must suppress detected secret-like values.
- Validator must fail closed.

## 13_ESTABLISHED

Required verdict set implemented or reserved:

- `PASS_POLICY_STATIC_VALIDATION`
- `FAIL_SCHEMA_MISSING_FIELD`
- `FAIL_UNKNOWN_CLASS`
- `FAIL_GATE_BINDING`
- `FAIL_TRACE_BINDING`
- `FAIL_EVAL_BINDING`
- `FAIL_NEVER_ALLOWED_APPROVAL_PATH`
- `FAIL_SECRET_RISK`
- `FAIL_RUNTIME_BINDING_ENABLED`
- `FAIL_POLICY`
- `BLOCKED_WITH_REASON`
- `NEED_MORE_EVIDENCE`

## 14_HYPOTHESIS

The first implementation can cover the minimum static rules without implementing the full Markdown fixture harness. The conceptual corpus remains a reference set for a future broader harness.

## 15_REMAINING_GAP

Known gaps at cadrage:

- no CI integration in this GO;
- no live runtime policy loading;
- no full Markdown fixture extractor;
- no external YAML dependency;
- no schema file generation.

## 16_TODO

- Implement parser and validator.
- Add CLI.
- Add tests.
- Add safe usage README.
- Add test results documentation.
- Run scoped checks.
- Stage only scoped files.
- Commit implementation.

## 17_RESUME_POINT

Fixture Corpus passed at:

```text
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
```

This GO implements the first static validator on top of that corpus.

## 18_TO_DOCUMENT

Document:

- validator location;
- parser decision;
- CLI command;
- output format;
- exit code behavior;
- tests executed;
- remaining limits;
- no runtime/no secret proof.

## 19_TO_REMEMBER

The validator is a static preflight tool. It does not approve gates and does not authorize runtime policy use.
