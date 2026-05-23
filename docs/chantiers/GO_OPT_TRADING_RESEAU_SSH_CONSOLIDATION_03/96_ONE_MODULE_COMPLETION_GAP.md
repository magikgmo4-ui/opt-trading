---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01_COMPLETION_GAP
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: repo_read
machine_owner: db-layer
---

# 96_ONE_MODULE_COMPLETION_GAP

## Completion criteria check

| Criterion | Current state | Status |
| --- | --- | --- |
| `modules/reseau_ssh` is the only operationally relevant top-level SSH family module | false | blocked |
| all retained SSH capabilities live under `modules/reseau_ssh` | false | blocked |
| `modules/reseau_ssh_step1b` is retired or fully absorbed | false | blocked |
| `scripts/reseau_ssh` is retired from active flow | false | blocked |
| wrappers and docs point to one owner without compat ambiguity | partially true | blocked |

## Concrete blockers

- `baseline-hostname` still routes to `modules/reseau_ssh_step1b`
- `scripts/reseau_ssh/reseau_ssh_cmd.sh` still supports transition commands `bootstrap`, `ssh-hardening-safe`, `ssh-lockdown`
- `scripts/reseau_ssh/reseau_ssh_menu.sh` still exposes those same transition commands
- `scripts/reseau_ssh/install_reseau_ssh.sh` still exists as legacy delegating installer

## Verdict

`BLOCKED_WITH_REASON`
