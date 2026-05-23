---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: modules
source_kind: canonical
machine_owner: db-layer
links:
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/14_NORMALIZED_INVENTORY_SUMMARY.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/16_MISSING_CANONICAL_PROOF_REQUIREMENTS.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/10_CALLERS_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/20_WRAPPERS_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/30_TARGET_STRUCTURE.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/40_COMPATIBILITY_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/50_REPRISE.md
---

# GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01

## Purpose

Frame the convergence of the `reseau_ssh*` family toward one canonical SSH module without launching any physical merge or runtime refactor.

## Canonical state

- current module baseline: `CURRENT_BASELINE_2026_05_20 = 98`
- historical audit baseline kept intact: `87`
- historical delta proof gap remains documented and out of scope here
- this GO is allowed to continue family-level consolidation on a `doc-only` basis

## Scope audited

- `modules/reseau_ssh`
- `modules/reseau_ssh_step1b`
- nested implementation `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- legacy compat backend `scripts/reseau_ssh`

## Decision summary

| Element | Decision | Reason |
| --- | --- | --- |
| `modules/reseau_ssh` | `SURVIVOR_CANONICAL_CURRENT` | Current top-level canonical facade, published by `install_canonical_shortcuts.sh`, present in registry and wrappers registry |
| `modules/reseau_ssh_step1b` | `INTERMEDIATE_TRANSITIONAL_PREREQUISITE` | Still consumed by the canonical facade through `baseline-*` commands |
| nested `reseau_ssh_step2` | `ACTIVE_INTERNAL_IMPLEMENTATION` | Real active WireGuard and firewall implementation behind the canonical facade |
| `scripts/reseau_ssh` | `LEGACY_ROLLBACK_AND_TRANSITION_BACKEND` | Explicitly kept for rollback and transition commands, no longer the canonical family surface |

## Answers to the framing questions

1. Which step1b scripts are still consumed?

- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh`
- consumed indirectly by `modules/reseau_ssh/scripts/cmd.sh`
- active command path: `baseline-dry-run`, `baseline-apply`, `baseline-hostname`, `baseline-sanity`, `baseline-show-hosts`, `baseline-show-ssh`

2. Which step2 scripts are really active?

- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh`
- consumed indirectly by `modules/reseau_ssh/scripts/cmd.sh`
- active command path: `wg-install`, `wg-genkeys`, `wg-showpub`, `wg-render`, `wg-render-windows`, `wg-apply`, `wg-up`, `wg-down`, `wg-status`, `fw-dry-run`, `fw-apply`

3. Are external wrappers still pointing to step1b or legacy reseau_ssh?

- short canonical aliases point to `modules/reseau_ssh/scripts/*` via `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh`
- suffixed step2 compat aliases point to `modules/reseau_ssh/scripts/*` or nested step2 installer depending on installer used
- step1b still publishes its own suffixed aliases via `modules/reseau_ssh_step1b/scripts/install_shortcuts.sh`
- legacy `scripts/reseau_ssh/install_reseau_ssh.sh` still exists, but delegates to the canonical installer when available
- no repo proof was found of active non-doc callers requiring `cmd/menu/sanity-reseau_ssh_step1b`

4. What target structure should carry the unique SSH module?

- keep `modules/reseau_ssh` as the only top-level canonical family module
- keep `reseau_ssh_step2` nested as internal implementation until a later physical consolidation GO
- keep `reseau_ssh_step1b` as a temporary prerequisite module until baseline callers are retired or absorbed

5. Should compatibility wrappers be kept temporarily?

- yes for `baseline-*` through `step1b`
- yes for short canonical aliases published by `modules/reseau_ssh`
- yes for explicit rollback path `scripts/reseau_ssh`
- yes for suffixed step2 aliases while operator habits and machine-side state are not re-audited physically

6. Which physical GO should follow if this framing is PASS?

- `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`

## Invariants

- no physical merge in this GO
- no deletion in this GO
- do not mark `step1b` as fully legacy while `baseline-*` still route to it
- do not modify `registry/modules_registry.yaml` in this GO
- do not reopen the global modules audit

## Verdict

`PASS`

The family can continue toward a single canonical SSH module because the current repo shape is now clear:

- `modules/reseau_ssh` is the canonical top-level family surface
- nested `reseau_ssh_step2` is the active implementation layer
- `modules/reseau_ssh_step1b` is still a live prerequisite dependency
- `scripts/reseau_ssh` remains a bounded legacy rollback path
