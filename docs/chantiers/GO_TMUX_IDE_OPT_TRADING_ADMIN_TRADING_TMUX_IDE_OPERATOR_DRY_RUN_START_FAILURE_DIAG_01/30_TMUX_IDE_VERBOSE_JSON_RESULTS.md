# 30_TMUX_IDE_VERBOSE_JSON_RESULTS

## 1_MASTER_TARGET

Documenter les commandes `tmux-ide` de diagnostic, avec `TMUX_IDE_DEBUG=1`, `--verbose` et `--json`, sans relancer le workflow operateur complet.

## 2_READ_COMMANDS

Commandes executees :

```bash
npx -y tmux-ide@1.3.1 --version
npx -y tmux-ide@1.3.1 doctor --json
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
```

## 3_READ_RESULTS

Version :

```text
tmux-ide v1.3.1
```

`doctor --json` :

```text
ok=false
tmux installed=PASS
tmux version >= 3.0=PASS tmux 3.3a
Node.js >= 18=PASS v18.20.4
256-color terminal=PASS xterm-256color
ide.yml exists=FAIL not found in current directory
Claude Code agent teams=optional FAIL not set
```

`status --json` :

```json
{
  "session": "trading",
  "running": false,
  "configExists": false,
  "panes": []
}
```

`inspect --json` :

```json
{
  "error": "Cannot read ide.yml: ENOENT: no such file or directory, open '/opt/trading/ide.yml'",
  "code": "READ_ERROR"
}
```

Interpretation :

- prerequis `tmux` et Node OK ;
- absence de `ide.yml` actif attendue ;
- aucune session runtime active observee.

## 4_VERBOSE_JSON_MINIMAL_PROBE

Probe minimal dans un repertoire temporaire dedie :

```bash
WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
cat > ide.yml <<'YAML'
name: opt-trading-diag-minimal
rows:
  - panes:
      - title: Shell
        command: pwd
        focus: true
YAML

npx -y tmux-ide@1.3.1 validate --json
TMUX_IDE_DEBUG=1 NO_COLOR=1 TERM=xterm-256color npx -y tmux-ide@1.3.1 --verbose --json > tmux-ide-start.log 2>&1
```

Resultat :

```text
validate --json=PASS
TMUX_IDE_VERBOSE_JSON_EXIT=0
SESSION_AFTER_VERBOSE_JSON=NO after cleanup
```

Commandes `tmux` exposees dans le log :

```text
[tmux] has-session -t opt-trading-diag-minimal
[tmux] new-session -d -P -F #{pane_id} -s opt-trading-diag-minimal -c /tmp/tmp.sTv1VUOBq7 -x 200 -y 50
[tmux] select-pane -t %0 -T Shell
[tmux] send-keys -t %0 -l -- pwd
[tmux] send-keys -t %0 Enter
[tmux] set-option ...
[tmux] attach -t opt-trading-diag-minimal
```

Interpretation :

- with stdout redirected to a log file, `process.stdout.isTTY` is false for the `tmux-ide` process ;
- `process.stdout.columns` and `rows` are undefined in that path, so `tmux-ide@1.3.1` uses its fallback `-x 200 -y 50` ;
- the minimal start succeeds under this redirected-output diagnostic path ;
- this is not the same runtime condition as the blocked operator start, where stdout was a TTY with dimensions `0x0`.

## 5_PRIOR_VERBOSE_FAILURE_CAPTURE

The earlier verbose probe in this GO captured the blocked shape without redirected stdout fallback :

```text
STTY=0 0
[tmux] new-session -d -P -F #{pane_id} -s opt-trading-admin-trading -c /opt/trading -x 0 -y 0
tmux command failed
VERBOSE_EXIT=1
SESSION_AFTER_VERBOSE=NO
```

Direct equivalent:

```bash
tmux new-session -d -P -F '#{pane_id}' -s tmux_ide_diag_zero_size -c /opt/trading -x 0 -y 0
```

Output:

```text
width too small
ZERO_SIZE_TMUX_EXIT=1
ZERO_SIZE_SESSION=NO
```

## 6_FORCED_TTY_RESULT_FROM_PRIOR_VERBOSE_DIAG

The same GO also tested the minimal guard:

```bash
stty rows 50 cols 200
TERM=xterm-256color timeout 8s npx -y tmux-ide@1.3.1 --verbose
```

Result on the operator layout:

```text
OPERATOR_FORCED_STTY_BEFORE=0 0
OPERATOR_FORCED_STTY_AFTER=50 200
[tmux] new-session ... -x 200 -y 50
OPERATOR_FORCED_EXIT=124
OPERATOR_SESSION_AFTER_START=YES
OPERATOR_STATUS=PASS
OPERATOR_INSPECT=PASS
POST_SESSION_ABSENT=YES
POST_IDE_YML_ABSENT=YES
POST_SCRIPT_ABSENT=YES
```

Interpretation :

- the operator layout is not the root cause ;
- pane commands with `&&` and pipe are not the root cause ;
- the TTY size guard prevents `-x 0 -y 0`.

## 7_CLEANUP

Cleanup final confirme :

```text
POST_REPO_IDE_YML_ABSENT=YES
POST_DIAG_SESSION_PRESENT=NO
POST_DIAG_SOCKET_PRESENT=NO
CLEANUP_CONFIRMED
```

## 17_RESUME_POINT

```text
REPRISE:
tmux-ide verbose/json confirms command path.
Redirected stdout uses fallback 200x50; interactive TTY size 0x0 causes -x 0 -y 0.

NEXT:
Lire 40_ROOT_CAUSE_ANALYSIS.md.
```

## RISKS

- À qualifier.
