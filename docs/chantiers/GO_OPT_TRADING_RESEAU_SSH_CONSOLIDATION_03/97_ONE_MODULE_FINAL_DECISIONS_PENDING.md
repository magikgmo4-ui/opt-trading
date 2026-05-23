---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01_DECISIONS_PENDING
doc_type: compatibility_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: canonical_decision
machine_owner: db-layer
---

# 97_ONE_MODULE_FINAL_DECISIONS_PENDING

## Pending decision 1

`baseline-hostname`

Needs an explicit final answer:

- absorb into `modules/reseau_ssh`, or
- retire from supported flow

## Pending decision 2

Legacy transition helpers in `scripts/reseau_ssh`:

- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

Need an explicit final answer:

- keep temporarily as bounded rollback helpers, or
- move/retire them in a final cleanup lot

## Pending decision 3

`scripts/reseau_ssh/install_reseau_ssh.sh`

Needs an explicit final answer:

- archive as legacy installer, or
- remove after proving no operator dependency remains

## Verdict

`BLOCKED_WITH_REASON`
