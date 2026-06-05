# Collectors derivatives mapping 01

## 1. Scope

This note maps `modules/derivatives_collector` against the collector-family doctrine and the current baseline convergence work.

It does not migrate runtime code.
It does not rewrite derivatives semantics.
It does not attempt schema unification with spot collectors.

## 2. Current derivatives role

`derivatives_collector` currently acts as:
- the canonical derivatives collector module
- a multi-source metrics collector
- a downstream export producer for derivatives-oriented consumers

Its documented scope includes:
- Open Interest
- Funding Rates
- Liquidations
- Long/Short Ratios
- JSON / CSV downstream exports

## 3. Mapping against collector-family doctrine

### 3.1 File-first doctrine
- status: `aligned`
- mapping: keep `derivatives_collector` as a file-first collector module
- action: no runtime change required

### 3.2 Explicit module boundaries
- status: `aligned`
- mapping: `derivatives_collector` remains a family module, not a provider module
- action: preserve this role explicitly in docs

### 3.3 Shared runtime foundation usage
- status: `not_aligned`
- mapping: `derivatives_collector` is not currently built on `collectors_core`
- action: do not force migration now; only evaluate selective extraction later

### 3.4 Config doctrine
- status: `partially_aligned`
- mapping: current `.env`-style config should be documented against the family doctrine of defaults, local overrides, and env overrides
- action: add compatibility mapping first, not an abrupt config rewrite

### 3.5 Lifecycle/status vocabulary
- status: `not_aligned`
- mapping: `derivatives_collector` should eventually map its lifecycle to the family vocabulary around module identity, provider identity when applicable, run identity, timestamps, state, freshness, and error class
- action: document target vocabulary before changing files or runtime

### 3.6 Artifact family
- status: `not_aligned`
- mapping: current JSON / CSV exports should remain valid, but the module should be mapped against the family artifact doctrine:
  - `manifest.json`
  - `status.json`
  - `latest.json`
  - `events.jsonl`
  - `errors.jsonl`
- action: define a compatibility layer before any implementation patch

### 3.7 Operator surface
- status: `partially_aligned`
- mapping: wrappers already exist, but expectations should be compared against the newer collector-family operator surface
- action: align naming and runbook expectations first

### 3.8 Normalized contract discipline
- status: `partially_aligned`
- mapping: derivatives outputs should remain derivatives-specific and should not be forced into spot contracts
- action: define derivatives-specific contract discipline under the family doctrine rather than reusing spot contracts

## 4. What should converge first

Priority A:
- vocabulary
- artifact family doctrine
- operator surface expectations
- config doctrine wording

Priority B:
- compatibility mapping from derivatives exports into the family lifecycle/artifact model
- compatibility mapping from `.env`-style config into the family config doctrine

Priority C:
- selective runtime extraction only if cost/benefit is clearly positive

## 5. What must remain separate

- derivatives metrics semantics
- derivatives downstream export semantics
- derivatives-specific normalized contracts
- provider-specific source adapters
- any fake schema unification with spot collectors

## 6. Minimal compatibility target

A minimal non-breaking target for `derivatives_collector` would be:
- keep existing derivatives exports
- document and later add family lifecycle artifacts without removing current outputs
- align runbook language with collector-family doctrine
- align wrapper expectations where safe
- leave business logic and metrics semantics unchanged

## 7. Decision gate after this mapping

Only after this mapping is accepted should the repo decide:
- whether to add a lifecycle/artifact compatibility layer to `derivatives_collector`
- whether to add a config compatibility layer
- whether any small shared runtime extraction into `collectors_core` is worth doing

## 8. Next trigger

GO_COLLECTORS_LIFECYCLE_COMPAT_SCOPE_01

## RISKS

- À qualifier.
