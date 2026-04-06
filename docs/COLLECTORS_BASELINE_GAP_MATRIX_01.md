# Collectors baseline gap matrix 01

## Scope

Collector surfaces compared:
- `modules/derivatives_collector`
- `packages/collectors_core`
- `modules/collector_coingecko`
- `modules/collector_binance_spot`

Status vocabulary used in this matrix:
- `aligned`
- `partially_aligned`
- `not_aligned`
- `not_applicable`

## Gap matrix

| Dimension | derivatives_collector | collectors_core | collector_coingecko | collector_binance_spot | Family verdict |
|---|---|---|---|---|---|
| Module role clarity | partially_aligned | aligned | aligned | aligned | partially_aligned |
| File-first doctrine | aligned | aligned | aligned | aligned | aligned |
| Explicit module boundaries | aligned | aligned | aligned | aligned | aligned |
| Shared runtime foundation usage | not_aligned | aligned | aligned | aligned | partially_aligned |
| Config doctrine clarity | partially_aligned | aligned | aligned | aligned | partially_aligned |
| Secrets boundary clarity | partially_aligned | aligned | aligned | aligned | partially_aligned |
| Lifecycle/status artifact family | not_aligned | aligned | aligned | aligned | partially_aligned |
| Latest/manifest/status/events/errors doctrine | not_aligned | aligned | aligned | aligned | partially_aligned |
| Operator surface predictability | partially_aligned | not_applicable | aligned | aligned | partially_aligned |
| Runbook expectations | partially_aligned | not_applicable | aligned | aligned | partially_aligned |
| Normalized contract discipline | partially_aligned | not_applicable | aligned | aligned | partially_aligned |
| Separation of spot vs derivatives semantics | aligned | not_applicable | aligned | aligned | aligned |

## Interpretation by dimension

### 1. Module role clarity
- `derivatives_collector` is clear as a derivatives family collector, but it is not yet expressed as part of the newer collector-family doctrine.
- `collectors_core` is clear as a shared runtime package.
- the two spot collectors are clear as provider modules.

### 2. Shared runtime foundation usage
- the main structural gap is that `derivatives_collector` does not yet consume `collectors_core`.
- this does not automatically require migration now, but it is the main family-level non-alignment.

### 3. Config doctrine clarity
- the spot collectors already follow the newer doctrine: committed defaults, optional local overrides, env overrides.
- `derivatives_collector` still presents a different config model centered on `.env`.
- this is a family gap, but a low-risk doctrine gap before it is a runtime gap.

### 4. Lifecycle and artifact family
- the spot collectors already expose the newer artifact family:
  - `manifest.json`
  - `status.json`
  - `latest.json`
  - `events.jsonl`
  - `errors.jsonl`
- `derivatives_collector` documents JSON / CSV exports, but not the same lifecycle artifact family explicitly.
- this is the clearest low-risk convergence opportunity.

### 5. Operator surface
- wrappers exist in both families, but the newer spot collectors present a more explicit shared operator expectation.
- `collectors_core` itself is not an operator-facing module, so wrapper expectations are not applicable there.

### 6. Contract discipline
- the spot collectors already live under explicit normalized contract thinking.
- derivatives semantics should not be forced into the same spot entity contracts.
- convergence should happen at the family doctrine layer, not by fake schema unification.

## Convergence priority matrix

### Priority A — low risk / high value
- lifecycle vocabulary alignment
- artifact family doctrine alignment
- operator surface expectation alignment
- config doctrine wording alignment

### Priority B — moderate risk / medium value
- compatibility mapping from derivatives config model into the newer config doctrine
- compatibility mapping from derivatives outputs into a family lifecycle artifact model

### Priority C — high risk / defer
- deep runtime extraction from `derivatives_collector` into `collectors_core`
- schema unification across spot and derivatives payloads
- large collector framework rewrite

## Recommended next moves

1. freeze the exact baseline inventory findings against real files and wrappers
2. freeze a mapping note for `derivatives_collector` against the family doctrine
3. define the smallest lifecycle/artifact compatibility layer for derivatives
4. only later decide whether any runtime extraction is worth doing

## Next trigger

GO_COLLECTORS_DERIVATIVES_MAPPING_01
