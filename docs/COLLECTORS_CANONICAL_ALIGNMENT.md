# Collectors Canonical Alignment

Date: 2026-04-04

Canonical status:
- PR `#6` from `api-collector` is merged into `opt-trading` on `sot/mainline`.
- The temporary branch `api-collector` is deleted locally and remotely.
- The rotated CoinGecko key is no longer a migration blocker.
- The canonical source of truth is now this repository and branch: `opt-trading` / `sot/mainline`.

## Established alignment

- `packages/collectors_core` is now the shared foundation for collector runtime concerns that are intentionally cross-module.
- `modules/collector_coingecko` is the first real provider module built on that shared foundation.
- `modules/collector_binance_spot` is the second real provider module built on the same foundation and validates that the pattern is reusable across providers.
- `modules/derivatives_collector` remains the existing canonical module for the derivatives collection path already present in the repo.

## Relationship between the modules

- `packages/collectors_core`
  - shared package
  - owns common runtime helpers, config layering, artifact helpers, HTTP policy, and shared error/lifecycle behavior
  - does not represent a provider by itself

- `modules/collector_coingecko`
  - provider-specific spot market collector pilot
  - consumes `collectors_core`
  - establishes the first concrete modular provider shape

- `modules/collector_binance_spot`
  - provider-specific spot market collector pilot
  - consumes `collectors_core`
  - confirms the shared package is not CoinGecko-specific

- `modules/derivatives_collector`
  - existing canonical collector module for derivatives-oriented data already used in the repo
  - remains valid as the canonical derivatives path
  - is not yet converged onto the `collectors_core` modular collector structure

## Already established

- the shared collector foundation is landed on `sot/mainline`
- two provider modules exist on top of it: CoinGecko and Binance Spot
- the foundation is validated as reusable for more than one provider
- the canonical repo for this work is now `opt-trading`
- no provider `#3` is required for the current alignment checkpoint

## Not yet converged

- `derivatives_collector` and the new provider modules do not yet share one fully unified execution and packaging model
- downstream contracts are not yet harmonized across derivatives and spot collectors
- operational menus and wrappers are not yet consolidated behind one collector family facade
- migration of older collector logic into `collectors_core` is not done
- this checkpoint does not declare a full collector architecture redesign; it only records the current canonical landing state

## Next recommended trigger

Trigger the next pass only when the goal is explicit:
- either converge `derivatives_collector` toward the shared `collectors_core` runtime model,
- or define the common collector-family contract across spot and derivatives outputs before any provider `#3` is added.

## Stop point

Stop here for this pass.
The canonical alignment is recorded; no code or architecture expansion is part of this note.
