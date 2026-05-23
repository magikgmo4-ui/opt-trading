---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01_COMMANDS_DECISION
doc_type: compatibility_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: canonical_decision
machine_owner: db-layer
---

# 87_LEGACY_COMMANDS_DECISION

## Command decision matrix

| Legacy command | Current owner | Decision before backend exit |
| --- | --- | --- |
| `bootstrap` | canonical facade transition helpers | already rehomed |
| `ssh-hardening-safe` | canonical facade transition helpers | already rehomed |
| `ssh-lockdown` | canonical facade transition helpers | already rehomed |
| `wg-show` | canonical facade alias to `wg-status` | already rehomed |
| `wg-server-init` | legacy backend only | must be explicitly retired or rehomed |
| `wg-client-init` | legacy backend only | must be explicitly retired or rehomed |
| `wg-add-peer` | legacy backend only | must be explicitly retired or rehomed |

## Recommended policy

- do not silently keep these three WireGuard legacy commands forever
- do not retire them without an explicit operator decision
- run a dedicated GO that decides, one by one, whether they are:
  - retired in favor of the canonical `wg-genkeys -> wg-render -> wg-apply -> wg-up` workflow, or
  - rehomed under `modules/reseau_ssh`

## Current safe position

The backend cannot exit while these commands exist only in `scripts/reseau_ssh`.

## Verdict

`BLOCKED_WITH_REASON`
