# 30_EXECUTION_PROTOCOL

## 1_MASTER_TARGET

Documenter le protocole d'execution non destructif du futur dry-run operateur.

## 2_EXECUTION_STATUS

Ce document ne lance rien.

Statut :

```text
PROTOCOL_ONLY
```

Toute execution reelle doit etre faite dans un GO separe apres gate `ALLOW_OPERATOR_DRY_RUN`.

## 3_PRECHECK_SEQUENCE

Prechecks obligatoires :

```bash
ssh admin-trading "test -d /opt/trading"
ssh admin-trading "cd /opt/trading && pwd && git status --short --branch"
ssh admin-trading "cd /opt/trading && test ! -e ide.yml"
ssh admin-trading "! tmux has-session -t opt-trading-admin-trading"
```

Interpretation :

- si `/opt/trading` est absent : `BLOCKED` ;
- si `ide.yml` existe : `HOLD` ou `BLOCKED`, aucune suppression automatique ;
- si la session existe deja : `HOLD`, aucune prise de controle automatique ;
- si `git status` expose des deltas : continuer seulement si l'operateur accepte un dry-run read-only sans correction.

## 4_REMOTE_SCRIPT_TEMPLATE

Script distant propose pour le GO de dry-run :

```bash
#!/usr/bin/env bash
set -euo pipefail

SESSION="opt-trading-admin-trading"
REPO="/opt/trading"
SCRIPT="/tmp/tmux_ide_operator_workflow_minimal_01.sh"
CREATED_IDE_YML="NO"
STARTED_SESSION="NO"

cleanup() {
  set +e
  cd "$REPO" 2>/dev/null || true
  if [ "$STARTED_SESSION" = "YES" ]; then
    npx -y tmux-ide@1.3.1 stop >/tmp/tmux_ide_operator_workflow_minimal_01.stop.log 2>&1 || true
  fi
  if [ "$CREATED_IDE_YML" = "YES" ]; then
    rm -f "$REPO/ide.yml"
  fi
  rm -f "$SCRIPT"
}

trap cleanup EXIT INT TERM

test -d "$REPO"
cd "$REPO"
test ! -e ide.yml
! tmux has-session -t "$SESSION"

cat > "$REPO/ide.yml" <<'YAML'
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
YAML
CREATED_IDE_YML="YES"

npx -y tmux-ide@1.3.1 validate --json
set +e
# --- PREFLIGHT : TTY size guard ---
_STTY_BEFORE="$(stty size 2>/dev/null || echo 'no-stty')"
if [ -t 1 ]; then
  _STTY_COLS="$(echo "$_STTY_BEFORE" | awk '{print $2}')"
  _STTY_ROWS="$(echo "$_STTY_BEFORE" | awk '{print $1}')"
  if [ "${_STTY_COLS:-0}" = "0" ] || [ "${_STTY_ROWS:-0}" = "0" ]; then
    stty rows 50 cols 200 2>/dev/null || true
  fi
fi
_STTY_AFTER="$(stty size 2>/dev/null || echo 'no-stty')"
echo "STTY_BEFORE=$_STTY_BEFORE"
echo "STTY_AFTER=$_STTY_AFTER"
# --- END PREFLIGHT ---
timeout 12s npx -y tmux-ide@1.3.1
START_EXIT="$?"
if tmux has-session -t "$SESSION" 2>/dev/null; then
  STARTED_SESSION="YES"
fi
set -e

if [ "$START_EXIT" != "0" ] && [ "$START_EXIT" != "124" ]; then
  echo "START_EXIT=$START_EXIT"
  exit "$START_EXIT"
fi

npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
! tmux has-session -t "$SESSION"
STARTED_SESSION="NO"
rm -f "$REPO/ide.yml"
CREATED_IDE_YML="NO"
test ! -e "$REPO/ide.yml"
```

## 5_LOCAL_UPLOAD_AND_RUN_PATTERN

Pattern autorise pour le GO de dry-run :

```bash
ssh admin-trading "printf '%s' '<base64-script>' | base64 -d > /tmp/tmux_ide_operator_workflow_minimal_01.sh && chmod 700 /tmp/tmux_ide_operator_workflow_minimal_01.sh"
ssh -tt admin-trading "TERM=xterm-256color bash /tmp/tmux_ide_operator_workflow_minimal_01.sh"
```

Le script doit etre encode depuis une source relue dans le GO de dry-run. Il ne doit pas etre improvise dans un shell interactif.

## 6_NON_DESTRUCTIVE_PROPERTIES

Le protocole est non destructif car il :

- verifie l'absence de `ide.yml` avant creation ;
- ne modifie pas Git ;
- ne lance aucune commande applicative ;
- ne touche pas aux services ;
- borne le client interactif par `timeout 12s` ;
- declenche un `stop` au cleanup seulement pour une session creee par le protocole ;
- ne supprime que les artefacts temporaires qu'il cree.

## 7_STOP_CRITERIA

Stop immediat avant lancement si :

- host inaccessible ;
- repo absent ;
- `ide.yml` deja present ;
- session deja presente ;
- validation echouee ;
- demande de commande interdite ;
- doute sur le fait que le fichier temporaire a ete cree par le protocole.

Stop immediat apres lancement si :

- `status --json` ou `inspect --json` echoue ;
- le nombre de panes n'est pas observable ;
- l'operateur perd le controle de l'attache ;
- la session reste presente apres `stop` ;
- cleanup incomplet.

## 8_CLEANUP_CRITERIA

Cleanup PASS si :

```text
POST_SESSION_ABSENT
POST_IDE_YML_ABSENT
POST_TEMP_SCRIPT_ABSENT
NO_GLOBAL_INSTALL
NO_GIT_MUTATION
```

Cleanup FAIL si :

- `tmux has-session -t opt-trading-admin-trading` reussit apres cleanup ;
- `/opt/trading/ide.yml` existe apres cleanup ;
- `/tmp/tmux_ide_operator_workflow_minimal_01.sh` existe apres cleanup ;
- une mutation Git ou runtime est observee.

## 9_OUTPUT_EXPECTED_FROM_DRY_RUN

Le GO de dry-run devra capturer :

- sortie `validate --json` ;
- `START_EXIT`, en acceptant `124` comme timeout de l'attache ;
- sortie `status --json` ;
- sortie `inspect --json` ;
- resultat `stop` ;
- preuves de cleanup.

## 17_RESUME_POINT

```text
REPRISE:
Protocole d'execution pret pour un GO de dry-run separe.

NEXT:
Lire 40_GATE_DECISION.md pour le verdict.
```

## RISKS

- À qualifier.
