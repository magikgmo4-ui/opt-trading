# BUILDER_ARCHITECTURE_VIEW

## Scope

This document describes the builder documentation workflow architecture at child GO level.

## Components

```text
Operator
  -> Git branch / child GO directory
  -> Gate document
  -> Builder invocation
  -> Execution log / decision document
  -> Closeout
  -> PR toward sot/mainline
```

## Builder role

The builder is treated as a constrained agent capable of producing structured planning or documentation support. It must not be treated as an unrestricted runtime actor.

## Gateway / fallback distinction

```text
DIRECT_GATEWAY:
- preferred when token configuration is valid
- must respect gateway auth constraints

EMBEDDED_FALLBACK:
- acceptable for documentation dry-run validation
- must be logged clearly
- does not prove gateway token correctness
```

## Known warning

```text
WARNING:
gateway token mismatch was observed in the previous dry-run chain.

STATUS:
not fixed in this child

IMPLICATION:
builder documentation flow can continue, but gateway hardening requires a separate GO.
```

## Boundary

This architecture view is not a runtime deployment spec. It only documents the controlled builder documentation workflow.
