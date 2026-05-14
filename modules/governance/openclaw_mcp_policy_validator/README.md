# OpenClaw MCP Policy Static Validator

This module validates OpenClaw MCP policy drafts in static read-only mode.

## Command

```powershell
python -m modules.governance.openclaw_mcp_policy_validator path\to\policy.yaml
```

Optional unknown-capability check:

```powershell
python -m modules.governance.openclaw_mcp_policy_validator path\to\policy.yaml --capability unknown_tool
```

## Contract

- Reads only the local file explicitly provided.
- Does not mutate the policy file.
- Does not load a policy into OpenClaw runtime.
- Does not call a live MCP server.
- Does not call Ollama.
- Does not execute trade actions.
- Does not read secrets or environment dumps.
- Fails closed on parse errors, missing fields, unknown classes, missing gates, missing traces, missing evals, runtime binding, never-allowed approval paths, and secret risk.

## Output

Default output is deterministic JSON:

```json
{
  "verdict": "PASS_POLICY_STATIC_VALIDATION",
  "passed": true
}
```

Failure output suppresses risky values and includes only the path and reason.

## Limits

The parser supports the simple block YAML subset used by OpenClaw policy drafts. Anchors, aliases, tabs, complex flow maps, and ambiguous indentation are rejected rather than guessed.
