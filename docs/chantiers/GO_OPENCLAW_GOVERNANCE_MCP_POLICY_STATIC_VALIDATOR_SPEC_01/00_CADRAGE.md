# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01 -- 00_CADRAGE

## 1_MASTER_TARGET

OpenClaw governance must define a static MCP policy validator before any policy is loaded by a runtime, gateway, worker, Ollama Lab surface, or trading surface.

The master target is a doc-only, fail-closed validation specification.

## 2_INITIAL_PROJECT_DOC

Source chain:

```text
Reconciliation
-> MCP Boundary
-> Human Review Gates
-> Trace / Evals Profile
-> MCP Policy Schema
-> MCP Policy YAML Draft
-> MCP Policy Static Validator Spec
```

This file opens the local chantier for the static validator specification.

## 3_INITIAL_NEED

OpenClaw needs a future validator able to inspect a policy draft and answer, before runtime use:

- whether the policy is structurally complete;
- whether all capability classes are valid;
- whether gates, traces, evals, strict worker roles, and Ollama Lab bindings are coherent;
- whether deny-by-default and fail-closed behavior are enforced;
- whether `NEVER_ALLOWED` entries have no approval path;
- whether no secret material is present in inputs, outputs, fixtures, or examples.

## 4_MASTER_PROJECT_PLAN

This GO creates only documentation:

- static validator principles;
- input/output contract;
- schema validation rules;
- capability class validation rules;
- gate, trace, and eval binding rules;
- deny-by-default and never-allowed rules;
- no-secret static checks;
- verdict and error catalog;
- conceptual fixtures;
- future implementation plan;
- closeout.

No parser, runner, validator, runtime binding, CI job, config activation, trade action, sudo action, or shell capability is created.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01`

Final target:

```text
Define the canonical static validator specification for OpenClaw MCP policy, doc-only, before any executable implementation.
```

## 7_CANONICAL_STATE

Git state checked in the dedicated worktree:

```text
Worktree:
C:\Users\ghost\opt-trading-mcp-policy-static-validator-spec

git status --short --branch:
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01

git branch --show-current:
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01

git log --oneline -5:
1403a3e6 docs: draft OpenClaw MCP policy YAML
fa7558f2 docs: define OpenClaw MCP policy schema
e34b9952 Merge pull request #343 from magikgmo4-ui/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
b21a6cd1 Merge pull request #344 from magikgmo4-ui/go/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01
7b70b223 docs: global session closeout -- 4 chains closed

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01
```

Base:

```text
1403a3e6 docs: draft OpenClaw MCP policy YAML
```

## 8_VALIDATED_PLAN

Validated doc-only plan:

1. Read governance, boundary, gates, traces/evals, schema, and YAML draft sources.
2. Define validator inputs and outputs without executable files.
3. Define structural and semantic validation rules.
4. Define fail-closed verdicts and errors.
5. Define conceptual fixtures as documentation only.
6. Leave global indexes untouched.
7. Stage only the current chantier and local inbox entry.

## 9_SELECTED_SOLUTION

The selected solution is a specification package under:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01/
```

The local inbox entry is:

```text
docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01.md
```

No executable validator artifact is part of this GO.

## 12_INVARIANTS

- Documentation only.
- No executable code.
- No real validator.
- No runtime binding.
- No trade.
- No sudo.
- No secret.
- No unrestricted shell capability.
- No merge.
- No forced push.
- No branch cleanup.
- No auto-fix.
- Do not modify global indexes.
- Never use `git add -A`.
- Stage only the current chantier and local inbox entry.
- Unknown capability validates as `BLOCKED_BY_DEFAULT`.
- `NEVER_ALLOWED` with approval path other than `none` fails policy validation.
- Future validator behavior must fail closed.

## 13_ESTABLISHED

Sources read or checked:

```text
docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_CHATGPT_ORCHESTRATION_RECONCILIATION_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/ via branch reference
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/02_POLICY_YAML_DRAFT.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/03_POLICY_JSON_MAPPING_DRAFT.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/09_POLICY_DRAFT_VALIDATION_CHECKLIST.md
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/10_FUTURE_VALIDATOR_REQUIREMENTS.md
docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
docs/index/BRANCH_STATE.md
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/REPRISE.md
```

Established governance decisions:

- MCP policy is deny-by-default.
- Static validation must fail closed.
- Runtime binding must remain disabled in policy drafts.
- `NEVER_ALLOWED` has no approval path.
- Secret exposure is a policy failure.
- Missing gates, traces, or evals produce blocking verdicts.
- Strict workers cannot self-approve.
- Ollama Lab is read-only by default and gated for model pull, provider switch, service restart, and install.

## 14_HYPOTHESIS

The future implementation may use YAML parsing and JSON output, but this GO does not choose or create the implementation.

The current YAML draft uses `policy.policy_version` while the validator prompt names `policy.version`. The specification treats these as a compatibility decision for the future validator: at least one canonical version field must be present, and conflicting duplicate version fields must fail policy validation.

## 15_REMAINING_GAP

Remaining gaps after this GO:

- no executable parser exists;
- no validator CLI exists;
- no machine-readable fixture corpus exists;
- no CI job exists;
- no runtime integration exists;
- no signed policy artifact exists.

These gaps are intentional for a doc-only specification GO.

## 16_TODO

- Create all validator spec files.
- Create local inbox entry.
- Verify no global indexes changed.
- Verify no executable files were created.
- Verify staged scope is limited to the chantier and inbox.
- Commit the doc-only chantier.

## 17_RESUME_POINT

Resume from:

```text
MCP Policy YAML Draft PASS_DOC_ONLY on branch go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01 with commit 1403a3e6.
```

Current work:

```text
Specify the future static validator before implementation.
```

## 18_TO_DOCUMENT

The validator specification must document:

- expected input files;
- expected YAML structure;
- required fields;
- allowed enum values;
- class consistency;
- gate binding consistency;
- trace binding consistency;
- eval binding consistency;
- strict worker binding consistency;
- Ollama Lab binding consistency;
- deny-by-default enforcement;
- never-allowed enforcement;
- no-secret checks;
- fail-closed behavior;
- output verdicts.

## 19_TO_REMEMBER

This chantier is not an implementation GO.

The correct closeout verdict is:

```text
PASS_DOC_ONLY
```

unless documentation scope or git isolation fails, in which case:

```text
BLOCKED_WITH_REASON
```

## RISKS

- À qualifier.
