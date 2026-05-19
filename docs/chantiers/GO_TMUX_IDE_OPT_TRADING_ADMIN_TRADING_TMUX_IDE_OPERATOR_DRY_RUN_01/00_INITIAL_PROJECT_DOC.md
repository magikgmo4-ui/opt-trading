# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Executer le premier dry-run operateur non destructif `tmux-ide` sur `admin-trading`, en suivant le workflow minimal merge par PR #519.

## 2_GO_ID

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_01
```

## 3_BRANCH

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_01
```

Base locale :

```text
origin/sot/mainline @ d4858f4e
```

## 4_SOURCE_GATE

Source amont :

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01
```

Gate amont :

```text
ALLOW_OPERATOR_DRY_RUN
```

La PR #519 est mergee sur `sot/mainline` avant ouverture de ce GO.

## 5_SCOPE

Inclus :

- prechecks distants read-only sur `admin-trading:/opt/trading` ;
- creation d'un `ide.yml` temporaire si et seulement si le fichier est absent ;
- lancement borne par `timeout 12s` ;
- capture de `validate`, `start`, `status`, `inspect`, `stop` quand atteints ;
- cleanup de la session, du `ide.yml` temporaire et du script temporaire ;
- decision `PASS_OPERATOR_DRY_RUN`, `HOLD` ou `BLOCKED`.

Exclus :

- installation globale de `tmux-ide` ;
- `ide.yml` durable ;
- mutation Git distante ;
- realignement de `admin-trading:/opt/trading` ;
- commande de trading, paper, live, webhook ou runtime applicatif ;
- modification de `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE` ou `BRANCH_STATE`.

## 6_EXPECTED_INVARIANTS

```text
GLOBAL_INSTALL=NO
DURABLE_IDE_YML=NO
REMOTE_GIT_MUTATION=NO
APP_RUNTIME=NO
SESSION_PERSISTENCE=NO
GLOBAL_INDEX_CHANGE=NO
```

## 17_RESUME_POINT

```text
REPRISE:
Dry-run operateur autorise par PR #519 mergee.

NEXT:
Lire 10_PRECHECKS.md puis 30_DRY_RUN_RESULTS.md.
```
