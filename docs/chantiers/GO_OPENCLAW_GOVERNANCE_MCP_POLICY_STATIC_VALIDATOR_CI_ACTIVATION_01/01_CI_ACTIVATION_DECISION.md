# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01 -- 01_CI_ACTIVATION_DECISION

## 1_MASTER_TARGET

Decide whether local active CI workflow creation is admissible for the OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

This decision closes the previously defined `GATE_CI_ACTIVATION` locally, without push, merge, or PR.

## 3_INITIAL_NEED

Creating `.github/workflows/openclaw-mcp-policy-static-validator.yml` changes repository behavior for future GitHub Actions runs, so the activation must be justified by concrete local static evidence.

## 4_MASTER_PROJECT_PLAN

Use only the validated local evidence commands and verify the warning reconciliation outcome remains intact.

## 6_FINAL_TARGET

`PASS_CI_ACTIVATION_LOCAL_ONLY`

## 7_CANONICAL_STATE

Why CI activation is admissible now:

- the validator tests pass locally;
- the harness tests pass locally;
- the real fixture corpus passes locally;
- the warning reconciliation evidence has been re-confirmed;
- the workflow remains read-only and static;
- no runtime or secret boundary is crossed.

## 8_VALIDATED_PLAN

Proof warnings = 0:

```text
python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01

verdict=PASS_FIXTURE_HARNESS
total_fixtures=37
pass_count=37
fail_count=0
mismatches=0
warnings=[]
```

Proof corpus = `37/37 PASS`:

```text
total_fixtures=37
pass_count=37
fail_count=0
mismatches=[]
```

Proof targeted tests pass:

```text
python -m pytest tests/test_openclaw_mcp_policy_validator.py -q
12 passed in 1.61s

python -m pytest tests/test_openclaw_mcp_policy_fixture_harness.py -q
4 passed in 5.03s
```

## 9_SELECTED_SOLUTION

Local `GATE_CI_ACTIVATION` status:

```text
APPROVED_CI_ACTIVATION_LOCAL_ONLY
```

Interpretation:

- admissible for local repository creation of the workflow file;
- not executed remotely in this GO;
- not equivalent to push approval;
- not equivalent to merge approval;
- not equivalent to PR approval.

## 12_INVARIANTS

- No push.
- No merge.
- No PR.
- No workflow run triggered remotely by this session.
- No secret usage.
- No env dump.
- No runtime touched.

## 13_ESTABLISHED

The previous blocker from `08_CI_ACTIVATION_GATE.md` tied to warning handling is cleared locally because the harness now returns an empty `warnings` array.

## 14_HYPOTHESIS

Future remote execution should reproduce the same outcomes if GitHub-hosted Python remains compatible with the validator module and `pytest` installation succeeds.

## 15_REMAINING_GAP

This GO does not produce the first remote CI run result. It only prepares the active workflow file locally.

## 16_TODO

- Review workflow YAML for forbidden features.
- Record rollback path.
- Stage only allowed files.

## 17_RESUME_POINT

The CI activation gate is satisfied locally on the dedicated branch with clean validator, harness, and corpus evidence.

## 18_TO_DOCUMENT

Document the final workflow path, exact triggers, commands, permissions, and residual risks in the workflow review.

## 19_TO_REMEMBER

Local admissibility is not a license to push or merge.
