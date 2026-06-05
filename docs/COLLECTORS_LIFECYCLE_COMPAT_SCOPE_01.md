# Collectors lifecycle compat scope 01

## 1. Purpose

This scope defines the smallest valid compatibility layer for bringing `derivatives_collector` closer to the collector-family lifecycle doctrine.

This is a scope note only.
It does not implement runtime changes.
It does not change derivatives business logic.
It does not remove current JSON / CSV exports.

## 2. Starting point

From the baseline work already established:
- `derivatives_collector` is the canonical derivatives collector module
- it is not yet aligned with the newer lifecycle artifact family
- it should not be forced into spot schemas
- the lowest-risk convergence area is lifecycle, artifact, config wording, and operator expectations

## 3. Compatibility goal

The goal is to let `derivatives_collector` become collector-family compatible at the lifecycle layer while preserving its current derivatives-specific outputs.

Target compatibility family:
- `manifest.json`
- `status.json`
- `latest.json`
- `events.jsonl`
- `errors.jsonl`

This target is additive.
It must not invalidate or remove existing derivatives exports.

## 4. In scope

### 4.1 Lifecycle vocabulary scope
Define the target vocabulary for a future compatibility layer:
- `contract_version`
- `module_id`
- `provider_id` when applicable
- `run_id`
- `generated_at`
- `state`
- `freshness_state`
- `retryable`
- `retry_after`
- `error_code`
- `error_class`

### 4.2 Artifact compatibility scope
Define how the family artifacts would coexist with existing derivatives exports:
- `manifest.json` as discovery / compatibility summary
- `status.json` as deterministic current-state file
- `latest.json` as pointer to latest valid derivatives output set
- `events.jsonl` as append-only lifecycle history
- `errors.jsonl` as append-only structured failure history

### 4.3 Preservation rule scope
Define explicit non-breaking preservation rules:
- current JSON / CSV exports stay valid
- derivatives-specific payload semantics stay unchanged
- no fake spot-schema reuse
- no downstream consumer breakage accepted in this phase

### 4.4 Operator/readme scope
Define what would need alignment in docs only:
- runbook language
- wrapper expectations
- lifecycle/artifact explanations
- compatibility notes for downstream consumers

## 5. Explicitly out of scope

- implementing the lifecycle compatibility layer itself
- moving runtime logic into `collectors_core`
- changing current derivatives metrics semantics
- changing current provider/source adapters
- replacing existing JSON / CSV exports
- adding provider #3
- repo-wide collector refactor

## 6. Design constraints

Any later implementation pass must obey these constraints:
- additive only at first
- current consumers remain valid
- artifact family is introduced as a compatibility layer, not as a destructive replacement
- derivatives-specific contracts remain derivatives-specific
- config compatibility can be documented before it is implemented

## 7. Expected deliverable of the next implementation-facing pass

Before any patch, the repo should first freeze:
- the exact lifecycle field set for derivatives compatibility
- the minimal meaning of each family artifact in the derivatives context
- the mapping from current derivatives exports to `latest.json` and `manifest.json`
- the minimal event/error vocabulary for derivatives runs

## 8. Recommended next trigger

GO_COLLECTORS_LIFECYCLE_COMPAT_SPEC_01

## RISKS

- À qualifier.
