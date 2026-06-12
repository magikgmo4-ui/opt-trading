# Collectors migration map 01

## Starting point

This map follows the doctrine already frozen in `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`.

Current state:
- `modules/derivatives_collector` remains the canonical derivatives collector module.
- `packages/collectors_core` is the shared runtime foundation for the newer spot provider modules.
- `modules/collector_coingecko` and `modules/collector_binance_spot` are already validated on top of `collectors_core`.
- immediate runtime migration of `derivatives_collector` into `collectors_core` is explicitly not required.

## Migration goal

The goal is not to collapse all collectors into one fake schema or one large refactor.

The goal is to achieve:
- one collector-family doctrine
- one collector-family lifecycle vocabulary
- one collector-family artifact doctrine
- one collector-family operator surface expectation
- explicit separation between spot-specific and derivatives-specific semantics

## Migration principles

- keep the migration non-breaking
- converge low-risk layers first
- preserve current derivatives downstream behavior
- avoid provider #3 until doctrine and migration map are materially applied
- prefer adapters and doctrine alignment before deep runtime extraction

## Phase 0 — Baseline inventory

Before any migration patch:
- inventory current `derivatives_collector` wrappers, config files, and output artifacts
- inventory which runtime concerns are already duplicated with `collectors_core`
- inventory which downstream consumers depend on current derivatives outputs

Deliverable:
- one bounded inventory note attached to the collector convergence workstream

## Phase 1 — Vocabulary alignment

Align terminology first, without changing runtime behavior.

Converge on the same family vocabulary for:
- module identity
- provider identity when applicable
- run identity
- generated timestamps
- state vocabulary
- freshness vocabulary
- error classification vocabulary

Expected result:
- future collector docs and runbooks use the same family language
- no derivatives business semantics are changed in this phase

## Phase 2 — Artifact family alignment

Define how `derivatives_collector` maps to the collector-family artifact doctrine.

Target family doctrine:
- `manifest.json`
- `status.json`
- `latest.json`
- `events.jsonl`
- `errors.jsonl`

Migration rule for this phase:
- do not remove existing derivatives exports
- add doctrine-compatible artifacts only if they can be introduced without breaking current consumers
- existing JSON / CSV exports remain valid downstream outputs

Expected result:
- `derivatives_collector` becomes family-compatible at the lifecycle/artifact level
- derivatives-specific payloads still stay derivatives-specific

## Phase 3 — Config boundary alignment

Map the existing derivatives config model against the newer doctrine:
- committed defaults
- machine-local overrides
- env overrides
- secrets boundary

Migration rule for this phase:
- document the canonical target boundary first
- only introduce compatibility layers if needed
- do not force a disruptive config migration in one step

Expected result:
- the collector family has one explicit config doctrine
- `derivatives_collector` may remain temporarily on a compatibility path while the doctrine is made explicit

## Phase 4 — Operator surface alignment

Compare and align the operator surface across collector families:
- `cmd`
- `sanity`
- `menu`
- runbook expectations
- install / shortcuts expectations where relevant

Migration rule for this phase:
- align naming and expectations before changing behavior
- avoid breaking existing operator habits abruptly

Expected result:
- a clearer collector-family operator experience
- reduced ambiguity between family modules and provider modules

## Phase 5 — Selective runtime extraction decision

Only after phases 1 to 4 are complete:
- evaluate whether some runtime logic from `derivatives_collector` should move into `collectors_core`
- evaluate cost / benefit of extraction
- keep derivatives-specific business logic out of `collectors_core`

This is a decision gate, not an automatic migration.

Expected result:
- either a small selective extraction plan
- or an explicit decision to keep runtime separation with only doctrine-level convergence

## What must not happen

- no forced schema unification between derivatives and spot outputs
- no broad refactor of `derivatives_collector`
- no provider #3 introduced before this map is applied enough to reduce ambiguity
- no repo-wide collector framework rewrite

## Recommended implementation order

1. baseline inventory
2. vocabulary alignment
3. artifact family alignment
4. config boundary alignment
5. operator surface alignment
6. selective runtime extraction decision

## Next trigger

GO_COLLECTORS_BASELINE_INVENTORY_01

## RISKS

- À qualifier.
