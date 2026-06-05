# 20_RETRY_GUARD_PROTOCOL

## 1_MASTER_TARGET

Documenter le protocole execute pour le retry operateur avec guard TTY explicite.

## 2_REMOTE_SCRIPT

Script temporaire :

```text
/tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh
```

Execution :

```powershell
ssh admin-trading "printf '%s' '<base64-script>' | base64 -d > /tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh && chmod 700 /tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh"
ssh -tt admin-trading "TERM=xterm-256color bash /tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh"
```

## 3_GUARDS

Le script arrete avant creation du fichier temporaire si :

```bash
test -d "$REPO"
cd "$REPO"
test ! -e ide.yml
! tmux has-session -t "$SESSION"
```

## 4_TEMPORARY_IDE_YML

Fichier cree temporairement :

```text
/opt/trading/ide.yml
```

Contenu :

```yaml
name: opt-trading-admin-trading
rows:
  - size: 70%
    panes:
      - title: Shell
        command: pwd && git status --short --branch
        focus: true
      - title: Git
        command: git log --oneline -5 && git status --short --branch
  - size: 30%
    panes:
      - title: Docs
        command: find docs/chantiers -maxdepth 1 -type d -name 'GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_*' | sort | tail -20
```

## 5_EXECUTION_SEQUENCE

Sequence executee :

```bash
npx -y tmux-ide@1.3.1 validate --json
stty rows 50 cols 200 2>/dev/null || true
timeout 12s npx -y tmux-ide@1.3.1
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
```

`START_EXIT=124` est accepte uniquement si la session existe apres `timeout`.

## 6_CLEANUP_MODEL

Le cleanup supprime uniquement :

- la session `opt-trading-admin-trading` si elle a ete observee comme creee par le protocole ;
- `/opt/trading/ide.yml` si le script l'a cree ;
- `/tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh`.

Le script n'execute pas :

- `npm install -g` ;
- `apt install` ;
- `tmux kill-server` ;
- `git pull` ;
- `git fetch` ;
- `git reset` ;
- `git clean` ;
- workflow applicatif.

## 7_STOP_CRITERIA

Stop immediat si :

- `/opt/trading` est absent ;
- `ide.yml` existe deja ;
- la session cible existe deja ;
- `validate --json` echoue ;
- `stty` ne peut pas produire une taille non nulle et le start echoue ;
- `START_EXIT` est different de `0` ou `124` ;
- la session est absente apres start ;
- `status --json`, `inspect --json` ou `stop` echoue ;
- cleanup incomplet.

## 17_RESUME_POINT

```text
REPRISE:
Protocole retry execute avec ide.yml temporaire, stty guard, timeout, status, inspect, stop, cleanup.

NEXT:
Lire 30_RETRY_DRY_RUN_RESULTS.md.
```

## RISKS

- À qualifier.
