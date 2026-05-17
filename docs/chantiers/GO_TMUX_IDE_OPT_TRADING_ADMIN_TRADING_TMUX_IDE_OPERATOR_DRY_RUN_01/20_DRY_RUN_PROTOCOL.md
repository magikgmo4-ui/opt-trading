# 20_DRY_RUN_PROTOCOL

## 1_MASTER_TARGET

Documenter le protocole effectivement execute pour le dry-run operateur.

## 2_REMOTE_TARGET

```text
host: admin-trading
repo: /opt/trading
session: opt-trading-admin-trading
script: /tmp/tmux_ide_operator_dry_run_01.sh
package: npx -y tmux-ide@1.3.1
```

## 3_LOCAL_UPLOAD_AND_RUN

Pattern utilise :

```powershell
ssh admin-trading "printf '%s' '<base64-script>' | base64 -d > /tmp/tmux_ide_operator_dry_run_01.sh && chmod 700 /tmp/tmux_ide_operator_dry_run_01.sh"
ssh -tt admin-trading "TERM=xterm-256color bash /tmp/tmux_ide_operator_dry_run_01.sh"
```

## 4_TEMPORARY_IDE_YML

Fichier temporaire cree par le script :

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

## 5_GUARDS

Le script a execute les guards suivants avant creation du fichier :

```bash
test -d "$REPO"
cd "$REPO"
test ! -e ide.yml
! tmux has-session -t "$SESSION"
```

## 6_EXECUTION_SEQUENCE

Sequence executee :

```bash
cat > "$REPO/ide.yml"
npx -y tmux-ide@1.3.1 validate --json
timeout 12s npx -y tmux-ide@1.3.1
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
rm -f "$REPO/ide.yml"
rm -f "$SCRIPT"
```

Note : `status`, `inspect` et `stop` n'ont pas ete atteints pendant le chemin nominal, car le lancement a echoue avant creation de session.

## 7_CLEANUP_MODEL

Le `trap` de cleanup supprimait uniquement les artefacts temporaires crees par le protocole :

- `/opt/trading/ide.yml` si cree ;
- `/tmp/tmux_ide_operator_dry_run_01.sh` ;
- session `opt-trading-admin-trading` seulement si observee comme creee par le protocole.

## 17_RESUME_POINT

```text
REPRISE:
Protocole execute selon gate amont, avec script temporaire et ide.yml temporaire.

NEXT:
Lire 30_DRY_RUN_RESULTS.md.
```
