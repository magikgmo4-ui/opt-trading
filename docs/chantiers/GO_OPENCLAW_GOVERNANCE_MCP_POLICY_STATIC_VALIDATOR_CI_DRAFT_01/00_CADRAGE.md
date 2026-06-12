# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 00_CADRAGE

## 1_MASTER_TARGET

Prepare the documentary CI draft for the OpenClaw MCP Policy static validator and fixture harness without creating an active CI workflow.

## 2_INITIAL_PROJECT_DOC

Source chain:

- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`
- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01`

## 3_INITIAL_NEED

OpenClaw needs a future CI path able to run the static validator tests, fixture harness tests, full 37-fixture corpus comparison, `git diff --check`, and safety controls before any runtime or active workflow activation.

## 4_MASTER_PROJECT_PLAN

This GO creates only a local chantier and one local inbox entry. It documents future CI steps, fail conditions, no-secret/no-runtime/no-network policy, fixture harness integration, warning policy, a Markdown-only workflow draft, and a future activation gate.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

Git state observed before edits in the dedicated worktree:

```text
git status --short --branch
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01

git branch --show-current
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01

git log --oneline -5
b4b3e53f feat: add OpenClaw MCP policy fixture harness
561a3ed5 feat: implement OpenClaw MCP policy static validator
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
248b6c38 docs: specify OpenClaw MCP policy static validator
1403a3e6 docs: draft OpenClaw MCP policy YAML

git remote -v
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

## 8_VALIDATED_PLAN

Deliverables for this GO:

1. `00_CADRAGE.md`
2. `01_CI_DRAFT_PRINCIPLES.md`
3. `02_CI_COMMAND_MATRIX.md`
4. `03_CI_FAIL_CLOSED_RULES.md`
5. `04_CI_NO_SECRET_NO_RUNTIME_POLICY.md`
6. `05_CI_FIXTURE_HARNESS_INTEGRATION.md`
7. `06_CI_WARNING_POLICY.md`
8. `07_CI_WORKFLOW_DRAFT_MARKDOWN_ONLY.md`
9. `08_CI_ACTIVATION_GATE.md`
10. `90_CLOSEOUT.md`

Local inbox entry:

- `docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01.md`

## 9_SELECTED_SOLUTION

The selected solution is a Markdown-only CI draft. No `.github/workflows` file is created. No active YAML or JSON CI file is added. Any workflow example remains inside a Markdown fence and is not executable by GitHub Actions.

## 12_INVARIANTS

- Documentation only.
- No active workflow.
- No `.github/workflows/*.yml` file.
- No `.github/workflows/*.yaml` file.
- No active CI YAML.
- No runtime OpenClaw action.
- No live MCP call.
- No Ollama call.
- No trade.
- No sudo.
- No network call in this GO.
- No secret read.
- No environment dump.
- No merge.
- No force push.
- No cleanup.
- No global index modification.
- `git add -A` is forbidden.
- Only current chantier files and the local inbox entry are eligible for staging.

## 13_ESTABLISHED

Sources read:

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/09_FIXTURE_INDEX_AND_EXPECTED_VERDICTS.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01/02_HARNESS_TEST_RESULTS.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01/90_CLOSEOUT.md`
- `modules/governance/openclaw_mcp_policy_validator/`
- `tests/test_openclaw_mcp_policy_validator.py`
- `tests/test_openclaw_mcp_policy_fixture_harness.py`

Prior harness evidence:

```text
validator tests: 12 passed
harness tests: 4 passed
corpus: 37/37 PASS
mismatches: 0
warnings inline/index: 4
```

## 14_HYPOTHESIS

Future CI can run the same static local commands after a dedicated activation GO, provided the inline/index warnings are either corrected or explicitly accepted as non-blocking with the fixture index remaining canonical.

## 15_REMAINING_GAP

Remaining gap for this GO:

- no active CI workflow exists by design;
- no CI activation is authorized by this GO;
- 4 inline/index warnings remain exposed by the harness;
- no strict warning failure mode is enabled in CI;
- no workflow file is created until `GATE_CI_ACTIVATION` passes.

## 16_TODO

This GO must document:

- future CI commands;
- fail-closed rules;
- no-secret/no-runtime/no-network policy;
- fixture harness integration;
- warning handling;
- Markdown-only workflow draft;
- activation gate.

## 17_RESUME_POINT

Fixture Harness PASS at commit `b4b3e53f` is the base state. This GO prepares the next documentary step only.

## 18_TO_DOCUMENT

Future closeout must state:

- files created;
- files modified;
- no active workflow created;
- no global index touched;
- no runtime touched;
- no secret read;
- warnings documented;
- NEXT_GO recommended.

## 19_TO_REMEMBER

Expected verdict for this GO:

```text
PASS_DOC_ONLY
```

If an active workflow, runtime touch, secret read, network call, global index edit, or out-of-scope file edit appears, the expected verdict becomes:

```text
BLOCKED_WITH_REASON
```

## RISKS

- À qualifier.
