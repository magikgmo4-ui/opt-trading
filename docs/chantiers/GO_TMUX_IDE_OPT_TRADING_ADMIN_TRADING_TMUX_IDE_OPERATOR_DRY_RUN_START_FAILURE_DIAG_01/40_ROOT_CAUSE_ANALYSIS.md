# 40_ROOT_CAUSE_ANALYSIS

## 1_MASTER_TARGET

Isoler la cause du `tmux command failed` et decider la suite.

## 2_FINDINGS

Findings etablis :

```text
F1: admin-trading exposes Debian-compatible tmux 3.3a.
F2: Node.js v18.20.4 and npx 9.2.0 satisfy tmux-ide declared prerequisites.
F3: SSH allocates a TTY: SSH_TTY=/dev/pts/0, STDIN_TTY=YES, STDOUT_TTY=YES.
F4: The allocated TTY reports STTY_SIZE=0 0.
F5: Node reports process.stdout.columns=0, rows=0, isTTY=true in the problematic SSH/TTY context.
F6: PATH resolves tmux/node/npm/npx/timeout/bash/sh to expected /usr/bin locations.
F7: no /etc/tmux.conf, ~/.tmux.conf, or ~/.config/tmux/tmux.conf was present.
F8: tmux minimal isolated with -f /dev/null -L opt-trading-diag-baseline-01 succeeds.
F9: tmux-ide --verbose generates tmux new-session ... -x 0 -y 0 when TTY size is 0x0.
F10: tmux directly rejects -x 0 -y 0 with width too small.
F11: redirected-output tmux-ide --verbose --json uses fallback -x 200 -y 50 and succeeds.
F12: stty rows 50 cols 200 makes tmux-ide generate -x 200 -y 50 and start succeeds.
```

## 3_REJECTED_HYPOTHESES

Rejected or demoted :

- tmux version incompatibility : rejected ;
- Node.js version incompatibility : rejected ;
- missing tmux binary : rejected ;
- broken tmux minimal socket : rejected ;
- PATH mismatch : rejected ;
- user/global tmux config : rejected ;
- operator layout as root cause : rejected ;
- `&&` or pipe pane commands as root cause : rejected ;
- timeout as primary cause : rejected for the blocked run because `START_EXIT=1`, not `124`.

## 4_ROOT_CAUSE

```text
PASS_ROOT_CAUSE_ISOLATED
```

Root cause :

```text
In this Codex -> ssh -tt execution context, the remote TTY exists but reports size 0 rows x 0 columns.

tmux-ide@1.3.1 reads stdout dimensions and passes them to tmux:
tmux new-session ... -x 0 -y 0

tmux rejects that command with:
width too small
```

Important nuance :

```text
When tmux-ide stdout is redirected to a log file, process.stdout dimensions are undefined instead of zero.
tmux-ide@1.3.1 then uses its fallback 200x50 and the minimal verbose/json probe succeeds.
```

## 5_DECISION

```text
PASS_ROOT_CAUSE_ISOLATED
```

## 6_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_RETRY_TTY_SIZE_GUARD_01
```

Retry delta :

```bash
echo "STTY_BEFORE=$(stty size 2>/dev/null || echo no-stty)"
stty rows 50 cols 200 2>/dev/null || true
echo "STTY_AFTER=$(stty size 2>/dev/null || echo no-stty)"
TERM=xterm-256color timeout 12s npx -y tmux-ide@1.3.1
```

## 7_INVARIANTS_FOR_NEXT_GO

- no global install ;
- no durable `ide.yml` ;
- no global `tmux kill-server` ;
- no Git remote realignment ;
- no application runtime ;
- cleanup session, temp `ide.yml`, and temp script ;
- document `STTY_BEFORE` and `STTY_AFTER`.

## 17_RESUME_POINT

```text
REPRISE:
Root cause isolated: TTY size 0x0.
Next retry must set stty rows/cols before tmux-ide launch.

GATE:
PASS_ROOT_CAUSE_ISOLATED
```
