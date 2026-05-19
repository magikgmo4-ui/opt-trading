# Inbox - GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01

## 1_MASTER_TARGET

Create a local fixture harness for the OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

Chantier path:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01/
```

Harness path:

```text
modules/governance/openclaw_mcp_policy_validator/fixture_harness.py
```

## 3_INITIAL_NEED

Run the existing static validator against the 37 Markdown fixtures and compare actual results to expected verdicts.

## 4_MASTER_PROJECT_PLAN

Implement harness, add tests, update README, document results, stage scoped files only.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01`

## 7_CANONICAL_STATE

Branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01
```

Base:

```text
561a3ed5 feat: implement OpenClaw MCP policy static validator
```

## 8_VALIDATED_PLAN

Expected checks:

- validator tests pass;
- harness tests pass;
- real corpus run passes;
- no global indexes modified;
- no runtime touched;
- no secret read;
- no active YAML/JSON added.

## 9_SELECTED_SOLUTION

Use a Python harness module with `python -m` invocation and deterministic JSON/text reports.

## 12_INVARIANTS

- Local static only.
- No runtime binding.
- No live MCP.
- No Ollama call.
- No trade.
- No sudo.
- No network.
- No secret read.
- No environment dump.
- No policy auto-fix.
- No global index updates.
- Do not use `git add -A`.

## 13_ESTABLISHED

Expected final verdict:

```text
PASS_FIXTURE_HARNESS
```

## 14_HYPOTHESIS

Fixture index remains canonical for expected verdict comparison.

## 15_REMAINING_GAP

CI integration remains future work.

## 16_TODO

- Run tests.
- Verify corpus pass count.
- Stage scoped files.
- Commit.

## 17_RESUME_POINT

Previous GO:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01
```

Previous commit:

```text
561a3ed5 feat: implement OpenClaw MCP policy static validator
```

## 18_TO_DOCUMENT

Document commit hash, test commands, fixture count, mismatch count, and NEXT_GO.

## 19_TO_REMEMBER

Recommended next GO:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01
```
