---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01_GATES
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

# 88_LEGACY_BACKEND_EXIT_GATES

## Hard gates before physical exit of `scripts/reseau_ssh`

1. explicit decision made for `wg-server-init`
2. explicit decision made for `wg-client-init`
3. explicit decision made for `wg-add-peer`
4. canonical facade no longer references the legacy backend as the escape hatch for removed commands
5. legacy installer fallback `install_reseau_ssh.sh` is either retired or deliberately preserved outside active family flow
6. documentation no longer instructs operators to use `scripts/reseau_ssh` for family operations

## Earliest safe sequence

1. resolve legacy WireGuard commands
2. remove canonical facade references to legacy backend
3. reclassify `scripts/reseau_ssh` from active rollback path to archival candidate
4. only then execute a bounded archive or retirement lot

## Not allowed yet

- archiving `scripts/reseau_ssh`
- deleting `scripts/reseau_ssh`
- removing the installer fallback without a replacement decision

## Verdict

`BLOCKED_WITH_REASON`
