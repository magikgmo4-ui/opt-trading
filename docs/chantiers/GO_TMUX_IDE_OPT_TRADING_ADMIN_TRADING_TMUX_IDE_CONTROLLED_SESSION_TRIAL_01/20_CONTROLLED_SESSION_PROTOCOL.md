# 20_CONTROLLED_SESSION_PROTOCOL

## 1_MASTER_TARGET

Documenter le protocole execute pour la session controlee.

## 7_CANONICAL_STATE

Execution distante :

```text
admin-trading:/opt/trading
```

Package :

```text
npx -y tmux-ide@1.3.1
```

Session :

```text
opt-trading-admin-trading
```

## 8_COMMAND_SEQUENCE

Sequence effective :

```bash
ssh admin-trading "printf '%s' '<base64-script>' | base64 -d > /tmp/tmux_ide_controlled_session_trial.sh && chmod 700 /tmp/tmux_ide_controlled_session_trial.sh"
ssh -tt admin-trading "TERM=xterm-256color bash /tmp/tmux_ide_controlled_session_trial.sh"
```

Le script distant a execute :

```bash
cd /opt/trading
test ! -e ide.yml
tmux has-session -t opt-trading-admin-trading
cat > /opt/trading/ide.yml
npx -y tmux-ide@1.3.1 validate --json
timeout 12s npx -y tmux-ide@1.3.1
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
rm -f /opt/trading/ide.yml
tmux has-session -t opt-trading-admin-trading
```

## 9_TEMPORARY_IDE_YML

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
        command: pwd
        focus: true
      - title: Git
        command: git status --short --branch
  - size: 30%
    panes:
      - title: Docs
        command: ls docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01
```

Hash observe :

```text
IDE_YML_SHA256=0d0412a17800a6e8c5bf9d5c4137791001c2bb9d2790200480a1169b18172980
```

## 10_SAFETY_GATES

Le script bloquait si :

- `/opt/trading` etait absent ;
- `/opt/trading/ide.yml` existait deja ;
- la session `opt-trading-admin-trading` existait deja ;
- `tmux-ide validate --json` echouait.

Le cleanup supprimait :

- la session si encore presente ;
- `/opt/trading/ide.yml` si encore present ;
- le script temporaire distant.

## 12_INVARIANTS

- L'usage de `timeout 12s` borne l'attache TUI.
- Le lancement interactif peut retourner `124` si le client est termine par timeout, tout en ayant cree la session.
- Le verdict depend de la presence observee de la session, puis de sa fermeture propre.

## 17_RESUME_POINT

Lire `30_SESSION_RESULTS.md` pour le resultat observe.

## RISKS

- À qualifier.
