# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Transformer le diagnostic `TTY size 0x0` en retry operateur borne pour `admin-trading`.

GO :

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_RETRY_TTY_SIZE_GUARD_01
```

## 2_CONTEXT

PR amont :

```text
#523 docs: isolate tmux-ide TTY size zero start failure
```

Etat PR :

```text
MERGED
merge commit = d9210be3
```

Cause racine amont :

```text
ssh -tt expose une TTY valide mais stty size retourne 0 0.
tmux-ide@1.3.1 transmet donc tmux new-session -x 0 -y 0.
tmux rejette avec width too small.
```

Guard valide par diagnostic :

```bash
stty rows 50 cols 200
```

## 3_LOCAL_WORKTREE

Le worktree principal `C:/Users/ghost/opt-trading` n'a pas pu etre avance en fast-forward apres merge de #523 car des fichiers non suivis locaux seraient ecrases par `origin/sot/mainline`.

Decision :

```text
ne pas deplacer les fichiers non suivis du worktree principal
ouvrir un worktree isole depuis origin/sot/mainline
```

Worktree utilise :

```text
C:/Users/ghost/opt-trading-go-tmux-retry-tty-size-guard
```

Branche :

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_RETRY_TTY_SIZE_GUARD_01
```

Base :

```text
origin/sot/mainline @ d9210be3
```

## 4_SCOPE

Scope autorise :

- `admin-trading` ;
- `tmux-ide@1.3.1` ;
- dry-run operateur non destructif ;
- `ide.yml` temporaire uniquement ;
- script temporaire sous `/tmp` ;
- cleanup de la session creee par le protocole ;
- documentation dans ce dossier GO uniquement.

Hors scope :

- installation globale ;
- upgrade `tmux` ou `tmux-ide` ;
- `git pull`, `git reset`, `git clean`, `git stash` ou realignement distant ;
- `tmux kill-server` global ;
- `ide.yml` durable ;
- workflow applicatif ou trading ;
- modification des index globaux.

## 8_DELIVERABLES

- `00_INITIAL_PROJECT_DOC.md`
- `10_PREFLIGHT_TTY_SIZE_GUARD.md`
- `20_RETRY_GUARD_PROTOCOL.md`
- `30_RETRY_DRY_RUN_RESULTS.md`
- `40_GATE_DECISION.md`
- `90_CLOSEOUT.md`

## 17_RESUME_POINT

```text
REPRISE:
PR #523 merged.
Worktree retry guard ouvert sur origin/sot/mainline @ d9210be3.
Retry operateur avec stty guard execute.

NEXT:
Lire 10_PREFLIGHT_TTY_SIZE_GUARD.md.
```
