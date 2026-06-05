# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01 -- 00_CADRAGE

## 1_MASTER_TARGET

Create the local active GitHub Actions workflow for the OpenClaw MCP Policy static validator, in fail-closed mode and without any remote trigger initiated from this session.

## 2_INITIAL_PROJECT_DOC

This chantier activates the workflow that was previously documented only as Markdown in `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`.

## 3_INITIAL_NEED

The warning reconciliation closeout proves that the validator and corpus are clean enough for local CI activation evidence:

- `37/37 PASS`
- `0 mismatch`
- `0 warning`

## 4_MASTER_PROJECT_PLAN

1. Verify real Git state.
2. Move to a dedicated local branch from the validated resume commit.
3. Re-run validator, harness, and corpus evidence commands.
4. Create one minimal active workflow under `.github/workflows/`.
5. Document decision, workflow review, local results, and closeout.
6. Stage only the workflow and chantier deliverables.

## 6_FINAL_TARGET

`PASS_CI_ACTIVATION_LOCAL_ONLY`

## 7_CANONICAL_STATE

Perimetre:

- `.github/workflows/openclaw-mcp-policy-static-validator.yml`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01/`
- `docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01.md`

Hors perimetre:

- push;
- merge;
- PR creation;
- OpenClaw runtime;
- MCP live;
- Ollama;
- trade;
- secrets;
- env dump;
- global index mutation.

Sources lues:

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01/07_CI_WORKFLOW_DRAFT_MARKDOWN_ONLY.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01/08_CI_ACTIVATION_GATE.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_WARNING_RECONCILIATION_01/03_TEST_RESULTS.md`
- `modules/governance/openclaw_mcp_policy_validator/`
- `tests/test_openclaw_mcp_policy_validator.py`
- `tests/test_openclaw_mcp_policy_fixture_harness.py`

Etat Git reel observed before branch creation:

```text
git status --short --branch
## go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_SMOKE_REPORT_01_COMMIT_01...origin/go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_SMOKE_REPORT_01_COMMIT_01
?? docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_ARTIFACT_REVIEW_01.md
?? docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_CLOSEOUT_01.md
?? docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/00_INITIAL_PROJECT_DOC.md
?? docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md
?? docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_POST_OPENCLAW_RECONCILIATION_01/
?? docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SURFACES_INVENTORY_01/
?? docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01.md

git branch --show-current
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_SMOKE_REPORT_01_COMMIT_01

git log --oneline -5
e3724f00 docs: close out WHY lint rule refinement
921a20ab docs: add OpenClaw runtime security aggregator smoke report
365f8c70 Merge pull request #462 from magikgmo4-ui/go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
c3091bdc feat: implement validation_gate V1 — SANITY PASS (30 tests, dry-run gate OK)
ddaac2e3 Merge pull request #461 from magikgmo4-ui/go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01

git remote -v
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Etat Git reel for this chantier branch:

```text
git switch -c go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01 bbb573b5

git status --short --branch
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01

git branch --show-current
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01

git log --oneline -5
bbb573b5 docs: reconcile OpenClaw MCP policy fixture warnings
5ba5963c docs: draft OpenClaw MCP policy validator CI
b4b3e53f feat: add OpenClaw MCP policy fixture harness
561a3ed5 feat: implement OpenClaw MCP policy static validator
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
```

## 8_VALIDATED_PLAN

The activation uses the already approved command matrix and converts the inert Markdown workflow into a scoped active workflow with read-only permissions and cautious triggers only.

## 9_SELECTED_SOLUTION

Selected branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01
```

Selected workflow path:

```text
.github/workflows/openclaw-mcp-policy-static-validator.yml
```

## 12_INVARIANTS

- No push.
- No merge.
- No PR.
- No runtime OpenClaw.
- No MCP live.
- No Ollama call.
- No trade.
- No sudo.
- No secret.
- No env dump.
- No global index change.
- Stage only the allowed workflow and chantier files.

## 13_ESTABLISHED

The resume commit `bbb573b5` contains the validator module, harness, corpus, draft workflow documentation, and the warning reconciliation evidence required by `GATE_CI_ACTIVATION`.

## 14_HYPOTHESIS

`actions/checkout` and `actions/setup-python` will require platform-level GitHub Actions network access when the workflow is later run remotely, but the validator and harness themselves stay local-static and no-runtime.

## 15_REMAINING_GAP

The workflow is created locally only in this GO. No remote execution is performed or observed here.

## 16_TODO

- Create workflow file.
- Record local proof.
- Run `git diff --check` and `git diff --cached --check`.
- Stage only allowed paths.

## 17_RESUME_POINT

Local CI workflow activation is based on `bbb573b5` after warning reconciliation, with the dedicated branch already created and proofs re-run locally.

## 18_TO_DOCUMENT

Closeout must capture the final workflow path, trigger scope, job commands, local test outputs, diff checks, and the next GO.

## 19_TO_REMEMBER

The workflow becomes active only as a local repository artifact in this session. No remote trigger is authorized by this GO.

## RISKS

- À qualifier.
