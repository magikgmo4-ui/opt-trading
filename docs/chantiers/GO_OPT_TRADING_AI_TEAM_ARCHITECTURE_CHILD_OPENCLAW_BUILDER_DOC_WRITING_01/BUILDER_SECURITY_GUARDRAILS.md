# BUILDER_SECURITY_GUARDRAILS

## Scope

These guardrails apply only to controlled OpenClaw builder documentation jobs.

They do not replace global project security policy.

## Hard prohibitions

```text
NO_SSH = true
NO_RUNTIME_PATCH = true
NO_GLOBAL_INDEX_UPDATE = true
NO_UNGATED_MUTATION = true
NO_SECRET_EXPOSURE = true
NO_TOKEN_FIX_INSIDE_DOC_CHILD = true
```

## Token boundary

A gateway token mismatch was observed previously. Documentation jobs may record this warning, but must not attempt token reconciliation unless a separate operational hardening GO is opened.

## Mutation boundary

Documentation children may write their own child GO artifacts only after the relevant gate or decision step.

They must not modify:

```text
runtime modules
gateway configuration
global indexes
active stream registries
machine split files
external services
```

## Response requirements

Builder responses used for validation should be structured and auditable.

Recommended fields:

```json
{
  "status": "string",
  "mode": "dry_run",
  "mutation": false,
  "ssh": false,
  "risk_notes": [],
  "next_gate": "string"
}
```

## Escalation

Open a separate GO if any of the following are required:

```text
gateway token reconciliation
runtime patch
SSH validation
security policy expansion
global index update
multi-machine execution
```
