---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_CALLERS_AUDIT
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: modules
source_kind: repo_read
machine_owner: db-layer
---

# 10_CALLERS_AUDIT

## Method

- repo-side static audit only
- no machine-side execution in this GO
- caller means any repo-side entrypoint delegating into `step1b`, nested `step2`, or legacy compat backend

## Caller matrix

| Source caller | Calls into | Evidence | Classification |
| --- | --- | --- | --- |
| `modules/reseau_ssh/scripts/cmd.sh` | nested `reseau_ssh_step2` | direct delegation through `RESEAU_SSH_IMPL_CMD` in `_reseau_ssh_common.sh`; commands `wg-*`, `fw-*` | `ACTIVE_CALLER` |
| `modules/reseau_ssh/scripts/cmd.sh` | `modules/reseau_ssh_step1b` | direct delegation through `RESEAU_SSH_STEP1B_CMD`; commands `baseline-*` | `ACTIVE_CALLER` |
| `modules/reseau_ssh/scripts/cmd.sh` | `scripts/reseau_ssh` | explicit fallback path for legacy compat commands and removed commands guidance | `ACTIVE_COMPAT_CALLER` |
| `modules/reseau_ssh/scripts/menu.sh` | `modules/reseau_ssh/scripts/cmd.sh` | canonical operator menu dispatch | `ACTIVE_CALLER` |
| nested `reseau_ssh_step2/scripts/reseau_ssh_menu.sh` | nested `reseau_ssh_step2/scripts/reseau_ssh_cmd.sh` | internal implementation menu | `IMPLEMENTATION_LOCAL_CALLER` |
| `modules/reseau_ssh_step1b/scripts/menu.sh` | `modules/reseau_ssh_step1b/scripts/cmd.sh` | top-level step1b menu wrapper | `STEP1B_LOCAL_CALLER` |
| `scripts/reseau_ssh/reseau_ssh_menu.sh` | `scripts/reseau_ssh/reseau_ssh_cmd.sh` | legacy rollback menu | `LEGACY_LOCAL_CALLER` |

## Step1b commands still consumed

These are still routed from the canonical facade and therefore block any declaration that `step1b` is fully retired:

- `baseline-dry-run`
- `baseline-apply`
- `baseline-hostname`
- `baseline-sanity`
- `baseline-show-hosts`
- `baseline-show-ssh`

Underlying target:

- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh`

## Step2 commands really active

These are the real implementation commands consumed by the canonical facade:

- `wg-install`
- `wg-genkeys`
- `wg-showpub`
- `wg-render`
- `wg-render-windows`
- `wg-apply`
- `wg-up`
- `wg-down`
- `wg-status`
- `fw-dry-run`
- `fw-apply`

Underlying target:

- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh`

## External caller conclusion

No repo-side proof was found of active code callers directly importing `modules/reseau_ssh_step1b` or nested `reseau_ssh_step2` as standalone top-level modules.

The proven entrypoint is the canonical facade:

- `modules/reseau_ssh/scripts/cmd.sh`
- `modules/reseau_ssh/scripts/menu.sh`
- `modules/reseau_ssh/scripts/sanity_check.sh`

## Decision impact

- `step1b` cannot be downgraded to pure legacy yet
- nested `step2` is active, but only as internal implementation
- legacy `scripts/reseau_ssh` remains bounded to transition and rollback semantics

## Verdict

`PASS`
