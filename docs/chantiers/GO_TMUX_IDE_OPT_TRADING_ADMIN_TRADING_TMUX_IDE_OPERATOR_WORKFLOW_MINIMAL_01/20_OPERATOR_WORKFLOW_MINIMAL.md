# 20_OPERATOR_WORKFLOW_MINIMAL

## 1_MASTER_TARGET

Definir le workflow operateur minimal qui pourra etre teste dans un dry-run separe, sans lancement de workflow reel.

## 2_OPERATOR_INTENT

But du workflow :

```text
ouvrir une session tmux-ide ephemere pour observer l'etat admin-trading et fermer proprement
```

Ce workflow est un cadre de lecture et d'observation. Il ne pilote aucun runtime applicatif.

## 3_SESSION_TARGET

```text
host: admin-trading
repo: /opt/trading
session: opt-trading-admin-trading
tmux-ide: npx -y tmux-ide@1.3.1
```

## 4_LAYOUT_MINIMAL

Layout cible pour dry-run :

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

Raison du layout :

- `Shell` confirme le repertoire et l'etat court ;
- `Git` donne le dernier contexte de commits sans mutation ;
- `Docs` liste les dossiers `tmux-ide` disponibles dans la copie distante sans supposer que le nouveau GO est deja present.

## 5_OPERATOR_STEPS

Workflow minimal :

1. verifier le baseline distant ;
2. refuser toute execution si `ide.yml` existe ;
3. refuser toute execution si la session cible existe ;
4. creer un `ide.yml` temporaire strictement minimal ;
5. valider avec `npx -y tmux-ide@1.3.1 validate --json` ;
6. lancer avec `timeout` pour borner l'attache TUI ;
7. observer `status --json` et `inspect --json` ;
8. stopper avec `npx -y tmux-ide@1.3.1 stop` ;
9. supprimer le `ide.yml` temporaire ;
10. verifier que la session et le fichier temporaire sont absents.

## 6_ALLOWED_COMMANDS

Commandes locales autorisees pour preparer ou auditer le dry-run :

```bash
git status --short --branch
git diff -- docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01
git grep -n "tmux-ide" -- docs/chantiers docs/index
```

Commandes distantes autorisees pour baseline read-only :

```bash
ssh admin-trading "cd /opt/trading && pwd && git status --short --branch"
ssh admin-trading "cd /opt/trading && test ! -e ide.yml"
ssh admin-trading "tmux has-session -t opt-trading-admin-trading"
```

Commandes distantes autorisees uniquement dans un dry-run gate `ALLOW_OPERATOR_DRY_RUN` :

```bash
ssh admin-trading "printf '%s' '<base64-script>' | base64 -d > /tmp/tmux_ide_operator_workflow_minimal_01.sh && chmod 700 /tmp/tmux_ide_operator_workflow_minimal_01.sh"
ssh -tt admin-trading "TERM=xterm-256color bash /tmp/tmux_ide_operator_workflow_minimal_01.sh"
```

Commandes autorisees a l'interieur du script dry-run :

```bash
cd /opt/trading
test ! -e ide.yml
! tmux has-session -t opt-trading-admin-trading
cat > /opt/trading/ide.yml
npx -y tmux-ide@1.3.1 validate --json
timeout 12s npx -y tmux-ide@1.3.1
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
rm -f /opt/trading/ide.yml
rm -f /tmp/tmux_ide_operator_workflow_minimal_01.sh
! tmux has-session -t opt-trading-admin-trading
```

## 7_FORBIDDEN_COMMANDS

Commandes interdites dans ce GO et dans le dry-run operateur minimal :

```bash
npm install -g tmux-ide
apt install tmux-ide
tmux-ide init
tmux-ide detect --write
git pull
git fetch
git reset
git clean
git checkout
git switch
git stash
docker compose up
docker compose down
npm run
python
node
curl
wget
systemctl
pm2
```

Interdits fonctionnels :

- aucun ordre de trading ;
- aucun workflow paper ou live ;
- aucun webhook ;
- aucune modification de config applicative ;
- aucun edit permanent dans `/opt/trading` ;
- aucun cleanup des deltas preexistants ;
- aucun changement des index globaux.

Exception encadree :

- `rm -f /opt/trading/ide.yml` est autorise seulement si le protocole a cree ce fichier temporaire apres avoir verifie son absence initiale ;
- `rm -f /tmp/tmux_ide_operator_workflow_minimal_01.sh` est autorise pour supprimer le script temporaire du dry-run.
- `npx -y tmux-ide@1.3.1 stop` est autorise seulement apres le guard de session absente et uniquement pour fermer la session creee par le protocole.

## 8_OPERATOR_SUCCESS

Un dry-run operateur minimal est PASS si :

- `validate --json` retourne `valid=true` ;
- la session est observee running apres le lancement ;
- `status --json` expose la session cible ;
- `inspect --json` expose 2 rows et 3 panes ;
- `stop` retourne succes ;
- `tmux has-session -t opt-trading-admin-trading` echoue apres stop ;
- `/opt/trading/ide.yml` est absent apres cleanup.

## 9_OPERATOR_FAILURE

Un dry-run operateur minimal est FAIL si :

- un guard initial echoue ;
- une commande interdite est necessaire ;
- `validate --json` echoue ;
- la session ne demarre pas ;
- la session ne peut pas etre arretee ;
- le cleanup laisse un fichier ou une session cible ;
- une commande applicative non read-only est executee.

## 17_RESUME_POINT

```text
REPRISE:
Workflow minimal = session ephemere read-only, 3 panes, timeout, inspect, stop, cleanup.

NEXT:
Lire 30_EXECUTION_PROTOCOL.md avant tout dry-run.
```

## RISKS

- À qualifier.
