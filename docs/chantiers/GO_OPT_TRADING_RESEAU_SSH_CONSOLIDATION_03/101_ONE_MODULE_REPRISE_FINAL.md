---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_REPRISE_FINAL
doc_type: reprise
repo: opt-trading
project: opt-trading
status: pass
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 101_ONE_MODULE_REPRISE_FINAL

## Resume point

```text
SSH family final state: ONE_MODULE_CANONIZED
Canonical top-level owner: modules/reseau_ssh
Canonical implementation: modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2
Residuals: shim-only or archival-candidate
Verdict: PASS
```

## Operational meaning

- use `modules/reseau_ssh` as the only SSH family owner
- do not reopen `reseau_ssh_step1b` as an active sibling module
- do not reopen `scripts/reseau_ssh` as an active backend

## Optional future cleanup

1. archive `modules/reseau_ssh_step1b`
2. archive `scripts/reseau_ssh`
3. trim dead shim bodies if desired

These are hygiene tasks only, not blockers to canonization.

## Verdict

`PASS`
