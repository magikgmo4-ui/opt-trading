---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01_RETIREMENT_GATES
doc_type: compatibility_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
status: pass
mode: doc-only
surface: modules
source_kind: canonical_decision
machine_owner: db-layer
---

# 83_STEP1B_RETIREMENT_GATES

## Hard gates before retiring `modules/reseau_ssh_step1b`

1. `modules/reseau_ssh/scripts/cmd.sh` no longer delegates any `baseline-*` command to `RESEAU_SSH_STEP1B_CMD`
2. absorbed baseline scripts and templates exist under `modules/reseau_ssh`
3. `baseline-dry-run`, `baseline-apply`, `baseline-sanity`, `baseline-show-hosts`, `baseline-show-ssh` still work through the canonical module
4. explicit decision taken on `baseline-hostname`
5. `menu/cmd/sanity-reseau_ssh_step1b` wrappers are no longer needed operationally

## Special caution gate

`baseline-hostname` must not be silently absorbed and retained by default.

It requires an explicit yes/no decision because it mutates machine identity and may deserve either:

- separate retention under canonical module, or
- explicit retirement if no longer operationally justified

## Earliest safe retirement sequence

1. absorb low-risk baseline assets and scripts
2. repoint `baseline-*` canonical dispatch to absorbed scripts
3. verify command parity
4. decide `baseline-hostname`
5. only then retire `step1b` wrappers and module shell

## Not allowed yet

- deleting `modules/reseau_ssh_step1b`
- archiving `modules/reseau_ssh_step1b`
- removing `*_step1b` wrappers before canonical parity is proven

## Verdict

`PASS`
