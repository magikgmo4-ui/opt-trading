# Inbox - GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01

## 1_MASTER_TARGET

Implement the first local static read-only OpenClaw MCP Policy validator.

## 2_INITIAL_PROJECT_DOC

Chantier path:

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01/
```

Validator path:

```text
modules/governance/openclaw_mcp_policy_validator/
```

## 3_INITIAL_NEED

Move from doc-only static validator specification to a controlled implementation without runtime binding.

## 4_MASTER_PROJECT_PLAN

Create parser, validator, CLI, tests, safe README, chantier docs, and local inbox entry.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`

## 7_CANONICAL_STATE

Branch:

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01
```

Base:

```text
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
```

## 8_VALIDATED_PLAN

Expected checks:

- local unit tests pass;
- no global indexes modified;
- no runtime touched;
- no secret read;
- no live MCP call;
- no policy auto-fix;
- scoped staging only.

## 9_SELECTED_SOLUTION

Use a Python module under `modules/governance/` and invoke it via `python -m`.

## 12_INVARIANTS

- Static read-only implementation.
- No runtime binding.
- No live MCP.
- No trade.
- No sudo.
- No secret.
- No unrestricted shell action.
- No merge.
- No force push.
- No branch cleanup.
- Do not modify global indexes.
- Do not use `git add -A`.

## 13_ESTABLISHED

Primary output verdict expected after verification:

```text
PASS_IMPLEMENTATION_STATIC_VALIDATOR
```

## 14_HYPOTHESIS

The first implementation can use a local strict YAML subset parser until dependency policy authorizes a full YAML parser.

## 15_REMAINING_GAP

The full 37-fixture Markdown harness remains future work.

## 16_TODO

- Verify tests.
- Verify diff checks.
- Stage only scoped files.
- Commit implementation.

## 17_RESUME_POINT

Previous GO:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01
```

Previous commit:

```text
2889d1d1 docs: add OpenClaw MCP policy validator fixture corpus
```

## 18_TO_DOCUMENT

Document final commit hash, test command, and remaining next GO.

## 19_TO_REMEMBER

Recommended next GO:

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_HARNESS_01
```
