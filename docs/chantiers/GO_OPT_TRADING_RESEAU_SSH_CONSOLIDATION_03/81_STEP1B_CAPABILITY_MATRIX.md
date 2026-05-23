---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01_CAPABILITY_MATRIX
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
status: pass
mode: doc-only
surface: modules
source_kind: repo_read
machine_owner: db-layer
---

# 81_STEP1B_CAPABILITY_MATRIX

## Matrix

| Baseline command | Underlying target | Behavior | Risk | Decision |
| --- | --- | --- | --- | --- |
| `baseline-dry-run` | `apply_linux.sh` | previews `~/.ssh/config` and `/etc/hosts` changes | low | absorb |
| `baseline-apply` | `apply_linux.sh --apply` | writes `~/.ssh/config` and managed `/etc/hosts` block | medium | absorb |
| `baseline-hostname` | `apply_hostname_linux.sh` | changes system hostname via `hostnamectl` | medium_high | keep transitional then review |
| `baseline-sanity` | `sanity_check.sh` | checks hosts block, ssh config, and best-effort connectivity | low | absorb or inline |
| `baseline-show-hosts` | `templates/hosts.block` | prints canonical hosts block | low | absorb |
| `baseline-show-ssh` | `templates/ssh_config.linux` | prints canonical ssh config template | low | absorb |

## Supporting assets

| Asset | Role | Decision |
| --- | --- | --- |
| `inventory.yaml` | machine metadata | absorb if still useful, otherwise deprecate after template migration |
| `templates/hosts.block` | managed hosts block | absorb |
| `templates/ssh_config.linux` | canonical ssh alias template | absorb |
| `scripts/apply_linux.sh` | baseline mutation logic | absorb |
| `scripts/apply_hostname_linux.sh` | hostname mutation logic | hold separately until explicit review |
| `scripts/sanity_check.sh` | baseline checks | absorb |

## Wrapper layer

| Wrapper | Current value | Decision |
| --- | --- | --- |
| `modules/reseau_ssh_step1b/scripts/cmd.sh` | generic module wrapper, not baseline implementation | retire after canonical baseline commands stop delegating to step1b |
| `modules/reseau_ssh_step1b/scripts/menu.sh` | wrapper shell around module folder | retire after same condition |
| `modules/reseau_ssh_step1b/scripts/sanity_check.sh` | wrapper sanity | retire after same condition |
| `modules/reseau_ssh_step1b/scripts/install_shortcuts.sh` | publishes `*_step1b` aliases | retire after same condition |

## Verdict

`PASS`
