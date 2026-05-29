---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: APPLIED_CLEANUP
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 20_APPLIED_CLEANUP

## Runtime behavior changes

- active commands now require an explicit archival override environment flag
- interactive menu no longer advertises an active operator surface by default
- sanity becomes an archival-status check rather than a full runtime pipeline assertion
- shortcut installation is blocked by default and requires explicit legacy opt-in
- gate-replay wrapper no longer behaves as a live scheduler entrypoint by default

## Archive signaling changes

- `README.md` is updated to describe the module as archival/residual
- `LEGACY.md` is added as the canonical archive-state explainer
- systemd unit files are kept as historical/runtime residue, not removed
