# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01 -- 00_CADRAGE

## 1_MASTER_TARGET

Reconcile the 4 inline/index metadata warnings reported by the OpenClaw MCP Policy fixture harness.

## 2_INITIAL_PROJECT_DOC

Source chain:

- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 3_INITIAL_NEED

The fixture harness reported 4 metadata warnings where inline fixture expectations differed from the canonical fixture index. The warnings blocked clean CI activation review.

## 4_MASTER_PROJECT_PLAN

Use the canonical fixture index as source of truth, align only inline metadata fields, preserve fixture snippets and semantic intent, rerun local tests and harness, and document the result.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01`

## 7_CANONICAL_STATE

Git state observed in the dedicated worktree before edits:

```text
git status --short --branch
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01

git branch --show-current
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01

git log --oneline -5
5ba5963c docs: draft OpenClaw MCP policy validator CI
b4b3e53f feat: add OpenClaw MCP policy fixture harness
561a3ed5 feat: implement OpenClaw MCP policy static validator
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
248b6c38 docs: specify OpenClaw MCP policy static validator

git remote -v
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Pre-change harness reproduction:

```text
verdict=PASS_FIXTURE_HARNESS
total_fixtures=37
pass_count=37
fail_count=0
mismatches=0
warnings=4
```

## 8_VALIDATED_PLAN

Scope:

- read governance and fixture sources;
- reproduce warnings;
- align 4 inline metadata fields with `09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`;
- create 5 chantier documents and 1 inbox entry;
- run validator tests, harness tests, corpus harness, and `git diff --check`.

Out of scope:

- validator logic changes;
- harness logic changes;
- CI activation;
- workflow creation;
- runtime binding;
- fixture semantic changes;
- canonical index changes.

## 9_SELECTED_SOLUTION

Apply the minimal correction: update only `expected_verdict` or `expected_error_code` inline fields where they disagree with the canonical fixture index.

## 12_INVARIANTS

- Correction targeted only.
- No OpenClaw runtime.
- No live MCP call.
- No Ollama call.
- No trade.
- No sudo.
- No network call.
- No secret read.
- No environment dump.
- No active workflow.
- No `.github/workflows` file.
- No push.
- No merge.
- No cleanup.
- No global index modification.
- `git add -A` forbidden.

## 13_ESTABLISHED

Sources read:

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01/06_CI_WARNING_POLICY.md`
- `modules/governance/openclaw_mcp_policy_validator/fixture_harness.py`
- `tests/test_openclaw_mcp_policy_fixture_harness.py`

## 14_HYPOTHESIS

Because all 37 actual validator outcomes already matched the canonical index, the warnings were metadata drift only. Aligning inline metadata should remove warnings without changing fixture semantics.

## 15_REMAINING_GAP

This GO does not activate CI. It only removes the warning blocker that kept `GATE_CI_ACTIVATION` from being cleanly reevaluated.

## 16_TODO

After reconciliation:

- verify warnings are `0`;
- verify tests still pass;
- verify corpus remains at 37 fixtures;
- verify no workflow or global index changed.

## 17_RESUME_POINT

CI Draft PASS at commit `5ba5963c`; warning reconciliation starts from that state.

## 18_TO_DOCUMENT

Document warning inventory, applied decisions, test results, modified files, and post-correction `GATE_CI_ACTIVATION` status.

## 19_TO_REMEMBER

Expected verdict:

```text
PASS_WARNING_RECONCILIATION
```

## RISKS

- À qualifier.
