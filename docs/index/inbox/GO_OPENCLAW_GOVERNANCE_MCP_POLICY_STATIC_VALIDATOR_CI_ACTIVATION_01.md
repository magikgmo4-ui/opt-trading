# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01

## 1_MASTER_TARGET

Track the local-only activation of the OpenClaw MCP Policy static validator CI workflow.

## 2_INITIAL_PROJECT_DOC

Inbox entry for the local chantier created on branch `go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01`.

## 3_INITIAL_NEED

The workflow draft is ready for local activation because warning reconciliation is complete and the corpus is clean.

## 4_MASTER_PROJECT_PLAN

Create the workflow locally, document the gate decision, record evidence, and stop before any push, merge, or PR.

## 6_FINAL_TARGET

`PASS_CI_ACTIVATION_LOCAL_ONLY`

## 7_CANONICAL_STATE

Deliverables:

- `.github/workflows/openclaw-mcp-policy-static-validator.yml`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01/`

## 8_VALIDATED_PLAN

Current status:

```text
workflow created locally
tests re-run locally
no push
no merge
no PR
```

## 9_SELECTED_SOLUTION

Resume basis:

```text
WARNING_RECONCILIATION PASS
commit bbb573b5
37/37 PASS
0 mismatch
0 warning
```

## 12_INVARIANTS

- Local only.
- No global index mutation outside this inbox entry.
- No runtime.
- No secret.

## 13_ESTABLISHED

The dedicated branch was created from `bbb573b5` and contains the required activation artifacts.

## 14_HYPOTHESIS

A later GO may promote this local change set to a committed and reviewed remote branch if explicitly approved.

## 15_REMAINING_GAP

Await final local staging and any later human instruction about commit or remote publication.

## 16_TODO

- verify staged diff hygiene;
- keep staging limited to allowed files.

## 17_RESUME_POINT

Reprendre sur `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_ACTIVATION_01` on the dedicated branch with the workflow already created locally.

## 18_TO_DOCUMENT

Reference `90_CLOSEOUT.md` for the final local evidence snapshot.

## 19_TO_REMEMBER

This inbox entry does not authorize push, merge, or PR.
