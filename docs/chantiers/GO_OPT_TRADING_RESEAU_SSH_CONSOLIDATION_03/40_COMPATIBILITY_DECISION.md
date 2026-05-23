---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_COMPATIBILITY_DECISION
doc_type: compatibility_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: wrappers
source_kind: canonical_decision
machine_owner: db-layer
---

# 40_COMPATIBILITY_DECISION

## Decision table

| Element | Keep now? | Reason | Exit condition |
| --- | --- | --- | --- |
| short aliases `menu/cmd/sanity-reseau_ssh` | yes | current canonical operator surface | only after a later physical GO proves equivalent canonical publication remains intact |
| suffixed aliases `menu/cmd/sanity-reseau_ssh_step2` | yes | explicit transition surface still registered and documented | can be reduced after machine-side revalidation and duplicate installer cleanup |
| step1b aliases `menu/cmd/sanity-reseau_ssh_step1b` | yes | step1b still exposes live prerequisite operations | only after `baseline-*` commands are absorbed or retired |
| `modules/reseau_ssh_step1b` | yes | still called by canonical facade | only after caller audit is closed by proof, not assumption |
| nested `reseau_ssh_step2` | yes | active implementation behind canonical facade | may stay nested even after physical consolidation |
| `scripts/reseau_ssh` | yes, bounded | rollback and transition path still explicitly documented | only after explicit rollback retirement GO |

## Compatibility rules

- `modules/reseau_ssh` remains the only canonical top-level family surface.
- `step2` remains implementation, not a separate top-level survivor.
- `step1b` remains transitional prerequisite, not final survivor.
- `scripts/reseau_ssh` remains legacy rollback path, not the family canon.
- no component is downgraded only because its role is narrower; downgrade requires caller proof.

## What is blocked intentionally

- declaring `step1b` fully legacy
- removing suffixed step2 aliases
- archiving `scripts/reseau_ssh`
- flattening nested `step2` into a new top-level path

## Physical GO preconditions

`GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02` is admissible only if it stays minimal and limited to:

1. wrapper publisher cleanup
2. duplicate installer reduction
3. README and path clarification
4. no runtime contract break on short aliases
5. no removal of `step1b` commands without explicit replacement

## Verdict

`PASS`
