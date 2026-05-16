# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01 -- 02_WORKFLOW_REVIEW

## 1_MASTER_TARGET

Review the active local workflow created for the OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

This review covers the newly created GitHub Actions workflow file only.

## 3_INITIAL_NEED

The workflow must remain minimal, fail-closed, and strictly bounded to static validator evidence.

## 4_MASTER_PROJECT_PLAN

Inspect the workflow path, triggers, jobs, commands, permissions, secrets, runtime scope, residual risks, and rollback path.

## 6_FINAL_TARGET

Workflow reviewed as compliant with local activation constraints.

## 7_CANONICAL_STATE

Chemin workflow cree:

```text
.github/workflows/openclaw-mcp-policy-static-validator.yml
```

Triggers:

- `pull_request` toward `sot/mainline` only;
- `workflow_dispatch` manual only;
- no `push` trigger.

Jobs:

- one job: `static-validator`.

## 8_VALIDATED_PLAN

Commandes executees by the workflow:

1. `python -m pip install --upgrade pip`
2. `python -m pip install pytest`
3. `python -m pytest tests/test_openclaw_mcp_policy_validator.py -q`
4. `python -m pytest tests/test_openclaw_mcp_policy_fixture_harness.py -q`
5. `python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`
6. `git diff --check`

Permissions GitHub Actions:

```yaml
permissions:
  contents: read
```

## 9_SELECTED_SOLUTION

Compliance review:

- `actions/checkout@v4`: yes;
- `actions/setup-python@v5`: yes;
- minimal dependency install: `pytest` only;
- validator tests: yes;
- harness tests: yes;
- corpus harness: yes;
- `git diff --check`: yes;
- secrets used: none;
- runtime touched: none;
- MCP live: none;
- Ollama: none;
- sudo: none;
- docker: none;
- service container: none;
- business network: none in validator/harness logic.

## 12_INVARIANTS

- The workflow is read-only from the repository permission perspective.
- The workflow has no `push` trigger.
- The workflow has no `secrets.*` reference.
- The workflow has no `env` dump step.
- The workflow has no runtime action step.

## 13_ESTABLISHED

The final YAML is a direct activation of the prior Markdown draft, with the workflow filename normalized to the path required by this GO prompt.

## 14_HYPOTHESIS

Using `python-version: "3.x"` keeps setup minimal while avoiding a local-only pin that was not mandated by repository metadata.

## 15_REMAINING_GAP

Risques residuels:

- remote runner Python minor version may differ from the local `3.14.2` validation environment;
- `pip install pytest` depends on GitHub Actions platform package availability when the workflow is later run remotely;
- `git diff --check` on a clean checkout cannot detect staged-only local issues because the workflow runs from checkout state.

Rollback local:

```text
Remove or rename .github/workflows/openclaw-mcp-policy-static-validator.yml on the local branch.
```

## 16_TODO

- Run final diff checks locally.
- Stage only allowed files.

## 17_RESUME_POINT

The active workflow is locally present, read-only, and constrained to static evidence commands.

## 18_TO_DOCUMENT

Record local diff-check results after staging in `03_LOCAL_TEST_RESULTS.md` and `90_CLOSEOUT.md`.

## 19_TO_REMEMBER

The workflow file is active as repository configuration, but this GO does not authorize remote use by push or PR.
