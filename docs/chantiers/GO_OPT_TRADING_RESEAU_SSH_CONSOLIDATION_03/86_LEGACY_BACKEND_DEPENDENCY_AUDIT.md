---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01_DEPENDENCY_AUDIT
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: repo_read
machine_owner: db-layer
---

# 86_LEGACY_BACKEND_DEPENDENCY_AUDIT

## Repo-side dependency matrix

| Item | Current state | Exit impact |
| --- | --- | --- |
| `scripts/reseau_ssh/install_reseau_ssh.sh` | deprecated delegating installer | can be retired only after explicit decision to drop this fallback entrypoint |
| `scripts/reseau_ssh/reseau_ssh_cmd.sh` | still implements `wg-server-init`, `wg-client-init`, `wg-add-peer` | blocks backend exit |
| `scripts/reseau_ssh/reseau_ssh_menu.sh` | legacy menu exposing those same commands | blocks backend exit |
| `scripts/reseau_ssh/sanity_reseau_ssh.sh` | legacy local sanity | secondary, but bundled with legacy backend |
| `modules/reseau_ssh/scripts/cmd.sh` | does not execute legacy backend directly, but still points users to it for removed commands | documentation/runtime dependency remains |
| `modules/reseau_ssh/scripts/_reseau_ssh_common.sh` | still carries compat path variables | informational dependency remains |

## Strong conclusion

There is no active canonical dispatch into `scripts/reseau_ssh` for normal operator flow anymore.

But there is still a real explicit legacy path because:

- the removed commands are still implemented there
- the canonical facade still documents that explicit escape hatch

## Exit class

`NOT_READY_FOR_PHYSICAL_EXIT`

## Verdict

`BLOCKED_WITH_REASON`
