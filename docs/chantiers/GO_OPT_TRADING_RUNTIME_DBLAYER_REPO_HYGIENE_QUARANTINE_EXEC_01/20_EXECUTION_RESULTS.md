---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01_EXECUTION_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: CONTROLLED_EXECUTION
source_kind: canonical
updated_at: 2026-05-28
---

# 20 — Execution results: quarantine .claude + artifacts/backtests (secrets untouched)

[7_CANONICAL_STATE]

```text
base = sot/mainline@bc3f594b
```

[12_PROOFS]

```text
Attempted quarantine root:
- /opt/trading_runtime_quarantine/... => Permission denied (no sudo used)

Executed quarantine root (writable, outside repo):
- /home/ghost/trading_runtime_quarantine/GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01/20260528T072737Z

Post-move git status (db-layer:/opt/trading):
## go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
?? docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/
?? secrets/

Remaining untracked (names redacted for secrets):
- docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/*.md (3 files)
- secrets/<redacted> (size total 8.0K)

Quarantine listing:
- $QROOT/.claude (moved)
- $QROOT/artifacts/backtests (moved)
Total quarantine size: 872K
```

[CONCLUSION]

```text
QUARANTINE_EXEC_STATUS = PASS_WITH_WARNINGS
MOVED_TARGETS = .claude/ ; artifacts/backtests/
UNMOVED_TARGETS = secrets/ ; docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01/
SECRETS_STATUS = UNTOUCHED
DBLAYER_WORKTREE_STATUS = CLEAN_TRACKED_WITH_UNTRACKED
NEXT_GO_CANDIDATE = GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_DOCS_EXEC_01
PARENT_CLOSE_GATE_STATUS = CLOSEOUT_BLOCKED
```
