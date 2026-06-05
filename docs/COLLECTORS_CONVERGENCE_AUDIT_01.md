# Collectors convergence audit 01

## 1. Etat observé

Current collector surfaces in the canonical repo:

- `modules/derivatives_collector`
  - canonical derivatives collector
  - multi-source derivatives metrics
  - config via `.env`
  - JSON / CSV exports

- `packages/collectors_core`
  - shared runtime package for new collectors
  - config boundary
  - env resolution
  - HTTP policy
  - lifecycle helpers
  - artifact helpers

- `modules/collector_coingecko`
  - spot provider
  - oneshot
  - uses `collectors_core`

- `modules/collector_binance_spot`
  - spot provider
  - oneshot
  - uses `collectors_core`

## 2. Convergences already present

- all collector surfaces are file-first
- all collector surfaces are module-oriented
- wrappers exist in both families
- downstream export intent already exists in both families
- the newer spot collectors already prove that shared runtime concerns can be centralized

## 3. Divergences really observed

### 3.1 Runtime model
- `derivatives_collector` is still a standalone collector family
- spot providers depend on `collectors_core`

### 3.2 Config model
- `derivatives_collector` uses `.env`
- spot providers use `defaults.toml` + optional `local.toml` + env overrides

### 3.3 Output model
- spot providers expose canonical artifacts:
  - `manifest.json`
  - `status.json`
  - `latest.json`
  - `events.jsonl`
  - `errors.jsonl`
- `derivatives_collector` README documents JSON / CSV exports, but not the same artifact family explicitly

### 3.4 Module role
- `derivatives_collector` is a metrics collector family
- `collector_coingecko` and `collector_binance_spot` are provider modules

## 4. Easy convergence opportunities

- define one collector-family doctrine for lifecycle and status vocabulary
- define one collector-family doctrine for artifact family
- define one collector-family operator surface expectation
- define one config-boundary doctrine, even if implementation remains temporarily different
- document how provider modules and family modules coexist

## 5. Risky convergence areas

- forcing `derivatives_collector` into spot-style schemas
- forcing full runtime migration into `collectors_core` before cost/benefit is proven
- breaking current derivatives downstream consumers
- over-unifying wrappers and menus before family boundaries are frozen

## 6. What should remain separate

- derivatives-specific metrics semantics
- spot-specific normalized entity contracts
- provider-specific endpoint logic
- any fake schema unification across derivatives and spot

## 7. Recommended minimal migration order

### Step 1
Freeze collector-family doctrine for:
- config boundary
- lifecycle/status vocabulary
- canonical artifact family
- operator surface expectations

### Step 2
Document how `derivatives_collector` maps against that doctrine:
- already aligned
- partially aligned
- not aligned

### Step 3
Converge only the lowest-risk layer first:
- docs
- runbook language
- status/artifact conventions
- wrapper surface expectations

### Step 4
Only later decide whether selective runtime extraction into `collectors_core` is justified.

## 8. Verdict

- convergence is justified
- immediate refactor is not justified
- next pass should freeze a collector-family doctrine before any migration patch

## 9. Next trigger

GO_COLLECTORS_FAMILY_DOCTRINE_01

## RISKS

- À qualifier.
