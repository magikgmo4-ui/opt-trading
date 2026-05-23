---
doc_id: GO_OPT_TRADING_RESEAU_SSH_FINAL_PLAN_ONE_MODULE
doc_type: consolidation_plan
repo: opt-trading
project: opt-trading
status: pass
mode: doc-only
surface: modules
source_kind: forward_plan
machine_owner: db-layer
---

# 70_FINAL_PLAN_ONE_MODULE

## Final target

Reach exactly one SSH family module survivor at top level:

- survivor: `modules/reseau_ssh`

And remove the need for separate family-level sibling modules or legacy runtime paths.

## Final desired end state

```text
modules/
  reseau_ssh/
    README.md
    scripts/
    implementation/
      step2/
    baseline/
      step1b_absorbed/

scripts/
  reseau_ssh/   <- archived or removed from active flow in a later dedicated GO
```

Meaning:

- no top-level `modules/reseau_ssh_step1b`
- no family-level ambiguity around `step2`
- no active canonical publication from `scripts/reseau_ssh`
- one operator surface and one repo-side family module

## Transition phases

### Phase 1

Current phase, already achieved:

- canonical top-level facade established at `modules/reseau_ssh`
- nested `step2` active internally
- `step1b` preserved as prerequisite
- rollback backend bounded

### Phase 2

Next minimal physical consolidation:

- deduplicate `*_step2` wrapper publishers
- clarify docs and installer ownership
- keep all current compat paths intact

Output GO:

- `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`

### Phase 3

Baseline absorption or retirement decision:

- inventory each `baseline-*` capability
- decide for each command whether to absorb into `modules/reseau_ssh` or retire it
- if absorbed, move implementation under the canonical module
- if retired, first prove there are no remaining operational callers

Output GO candidate:

- `GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01`

### Phase 4

Legacy rollback backend exit:

- prove `scripts/reseau_ssh` is no longer needed for rollback or explicit legacy calls
- cut delegation dependency if any remains
- archive or retire it in a bounded GO

Output GO candidate:

- `GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01`

### Phase 5

Final one-module canonization:

- confirm all SSH family behaviors are owned by `modules/reseau_ssh`
- confirm no sibling SSH family module remains needed at top level
- confirm no legacy wrapper publisher remains active
- freeze the final structure as the family canon

Output GO candidate:

- `GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01`

## Capability migration matrix

| Capability family | Current owner | Final owner | Required condition |
| --- | --- | --- | --- |
| short operator aliases | `modules/reseau_ssh/scripts/*` | `modules/reseau_ssh/scripts/*` | preserve throughout |
| WireGuard / firewall | nested `reseau_ssh_step2` | `modules/reseau_ssh` internal subtree | may remain nested if internal ownership is clear |
| baseline hosts / ssh config / hostname | `modules/reseau_ssh_step1b` | `modules/reseau_ssh` | absorb or retire with proof |
| rollback / old transition commands | `scripts/reseau_ssh` | none or archived compat only | only after explicit retirement proof |

## Hard invariants

- do not rewrite history around the `87` baseline
- do not reopen the global module baseline work here
- do not remove `step1b` before its baseline capabilities are explicitly resolved
- do not claim one-module completion while `scripts/reseau_ssh` still acts as an active family path
- do not change registry in the wrong phase

## Completion criteria for true one-module finish

The family is truly consolidated to one module only when all of these are true:

1. `modules/reseau_ssh` is the only top-level SSH family module that remains operationally relevant
2. all retained SSH capabilities live under `modules/reseau_ssh`
3. `modules/reseau_ssh_step1b` is retired or fully absorbed
4. `scripts/reseau_ssh` is retired from active flow
5. wrappers and docs point to one canonical owner without compat ambiguity

## Recommended next order

1. `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`
2. `GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01`
3. `GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01`
4. `GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01`

## Verdict

`PASS`

The repo now has a stable forward plan to reach one SSH family module without pretending that the remaining transitional and rollback surfaces are already gone.
