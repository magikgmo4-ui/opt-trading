---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
status: pass
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 84_STEP1B_REPRISE

## Resume point

```text
CURRENT_BASELINE: 98
SSH canonical top-level: modules/reseau_ssh
Current sub-go: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
Mode: doc-only
Verdict: PASS
```

## Established

- `step1b` remains alive only because baseline capabilities still route through it
- most `step1b` value is absorbable into the canonical module
- `baseline-hostname` is the only capability requiring explicit extra caution

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_STEP1B_PHYSICAL_ABSORPTION_01`

## Scope for next GO

- absorb low-risk baseline scripts and templates into `modules/reseau_ssh`
- keep public `baseline-*` names stable
- avoid deleting `step1b` in the same lot
- decide separately whether `baseline-hostname` is kept or retired

## Verdict

`PASS`
