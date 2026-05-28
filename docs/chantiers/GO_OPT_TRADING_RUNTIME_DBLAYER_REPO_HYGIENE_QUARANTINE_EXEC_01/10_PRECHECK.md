---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01_PRECHECK
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: CONTROLLED_EXECUTION
source_kind: canonical
updated_at: 2026-05-28
---

# 10 — Precheck: db-layer (/opt/trading) before quarantine move

[12_PROOFS]

```text
ssh db-layer 'hostname; whoami; pwd'
db-layer / ghost / /home/ghost

ssh db-layer 'cd /opt/trading && git status --short --branch'
## sot/mainline...origin/sot/mainline
?? .claude/
?? artifacts/backtests/
?? secrets/

ssh db-layer 'cd /opt/trading && git diff --name-status'
(empty)

ssh db-layer 'cd /opt/trading && git ls-files --others --exclude-standard | head -n 50'
.claude/scheduled_tasks.lock
artifacts/backtests/... (multiple files)
secrets/<redacted>
```
