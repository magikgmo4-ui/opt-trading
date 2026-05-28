---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_DRIFT_AUDIT_01_AUDIT_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_DRIFT_AUDIT_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-28
---

# 10 — Audit results: db-layer /opt/trading repo drift (read-only)

[7_CANONICAL_STATE]

```text
base (decision) = sot/mainline@8fbcb28
parent = GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
scope = read-only audit (db-layer)
```

[12_PROOFS]

```text
ssh db-layer 'hostname; whoami; pwd'
db-layer / ghost / /home/ghost

ssh db-layer 'cd /opt/trading && git status --short --branch'
## sot/mainline...origin/sot/mainline
?? .claude/
?? artifacts/backtests/
?? secrets/

ssh db-layer 'cd /opt/trading && git branch --show-current'
sot/mainline

ssh db-layer 'cd /opt/trading && git log -1 --oneline --decorate'
c2f766ad (HEAD -> sot/mainline, origin/sot/mainline) docs(closeout-index): close GO_TRADING_LAB_REAL_BROKER_MEASUREMENT_01

ssh db-layer 'cd /opt/trading && git remote -v'
origin git@github.com:magikgmo4-ui/opt-trading.git (fetch)
origin git@github.com:magikgmo4-ui/opt-trading.git (push)

ssh db-layer 'cd /opt/trading && git diff --name-status'
(empty)

ssh db-layer 'cd /opt/trading && git diff --stat'
(empty)

ssh db-layer 'cd /opt/trading && git ls-files --others --exclude-standard'
.claude/scheduled_tasks.lock
artifacts/backtests/... (multiple csv/md files)
secrets/google_oauth_client.json

ssh db-layer 'cd /opt/trading && git show HEAD:scripts/fleet_orchestrator.sh | sed -n "1,80p"'
... contains python selection with `import yaml` gate ...

ssh db-layer 'cd /opt/trading && sed -n "1,80p" scripts/fleet_orchestrator.sh'
... same content as git show (worktree matches HEAD) ...
```

[13_ESTABLISHED]

- Le repo `db-layer:/opt/trading` n'est pas "drifted" cote fichiers trackes : aucun `modified` (diff vide).
- Il existe des untracked, et ils sont exactement sur les surfaces attendues : `.claude/`, `artifacts/backtests/`, `secrets/`.
- `scripts/fleet_orchestrator.sh` sur db-layer contient le guard PyYAML (`import yaml`) et le worktree correspond a `HEAD` : le fix PR #864 est donc present sur ce host (au moins en fichier).

[15_REMAINING_GAP]

- La presence du fichier ne prouve pas l'execution en runtime (le wrapper ecrit dans `$TRADING_ROOT/data/runtime_health` via `mkdir -p`).
- Les untracked `secrets/` et `artifacts/` restent un verrou pour toute action d'alignement ou de deploy controle (hors-scope ici).
- Si un alignement futur est envisage, il faudra d'abord un GO dedie "repo hygiene / quarantine" (ou une procedure d'inventaire + backup).

[CONCLUSION]

```text
DBLAYER_DRIFT_STATUS = CLEAN_TRACKED_WITH_UNTRACKED (no modified tracked files)
FIX_DEPLOYMENT_STATUS = PROVEN_PRESENT_ON_DBLAYER_WORKTREE (fleet_orchestrator.sh includes import-yaml gate)
SAFE_ALIGNMENT_PLAN_CANDIDATE = INVENTORY_ONLY (no reset/pull; classify untracked first)
BLOCKERS = untracked_secrets; untracked_artifacts
NEXT_GO_CANDIDATE = GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01
```
