# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir un GO diagnostic distinct pour isoler la cause du blocage :

```text
tmux command failed
START_EXIT=1
SESSION_PRESENT_AFTER_START=NO
```

Ce diagnostic ne relance pas le workflow operateur complet.

## 2_GO_ID

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_START_FAILURE_DIAG_01
```

## 3_BRANCH

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_START_FAILURE_DIAG_01
```

Base locale :

```text
origin/sot/mainline @ e3289a67
```

## 4_SOURCE_CONTEXT

Source amont :

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_01
STATE=BLOCKED_START_TMUX_COMMAND_FAILED
```

Doc support lue :

```text
C:/Users/ghost/Downloads/tmux_ide_deb_12_operator_support_diag_01.md
TMUX_IDE_DEB12_OPERATOR_SUPPORT_DIAG_01
```

## 5_SCOPE

Inclus :

- baseline TTY, PATH, socket, shell, `TERM`, `SSH_TTY`, `TMUX`, `TMUX_TMPDIR` ;
- probes `tmux` minimaux sur socket dedie `tmux -L opt-trading-diag-*` ;
- commandes `tmux-ide` de lecture : `--version`, `doctor --json`, `status --json`, `inspect --json` ;
- reconciliation avec le diagnostic deja observe sur `tmux-ide --verbose` ;
- gate de decision.

Exclus :

- `npm install -g` ;
- `apt install` ;
- `tmux kill-server` global ;
- suppression de `/tmp/tmux-*` ;
- `ide.yml` durable ;
- dry-run operateur complet ;
- modification des index globaux ;
- cleanup de fichiers hors scope.

## 6_EXPECTED_DECISION

Verdicts autorises :

```text
PASS_ROOT_CAUSE_ISOLATED
PARTIAL_PASS_DIAG_SIGNAL
BLOCKED_NEEDS_MORE_STDERR
HOLD_NO_REPRO
```

## 17_RESUME_POINT

```text
REPRISE:
GO diagnostic ouvert apres #521 mergee.

NEXT:
Lire 10_BASELINE_TTY_PATH_SOCKET_SHELL.md puis 20_TMUX_MINIMAL_ISOLATED_PROBES.md.
```
