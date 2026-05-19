# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Definir un premier workflow operateur minimal pour `admin-trading` via `tmux-ide`, a partir du `PASS_CONTROLLED_SESSION` deja merge, sans installation durable, sans generalisation et sans lancement destructif.

## 2_GO_ID

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01
```

## 3_BRANCH

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01
```

Base attendue :

```text
origin/sot/mainline
```

## 4_SCOPE

Inclus :

- workflow operateur minimal centre sur `admin-trading:/opt/trading` ;
- commandes autorisees et interdites pour un dry-run operateur ;
- protocole d'execution non destructif ;
- criteres de stop et cleanup ;
- gate vers `ALLOW_OPERATOR_DRY_RUN`, `HOLD` ou `BLOCKED`.

Exclus :

- installation globale de `tmux-ide` ;
- creation d'un `ide.yml` permanent ;
- realignement du repo distant `admin-trading:/opt/trading` ;
- lancement d'un workflow de trading, paper, live, webhook ou runtime applicatif ;
- modification de `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE` ou `BRANCH_STATE` ;
- reouverture des GO fermes.

## 5_SOURCE_CONTEXT

Sources lues en premier :

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01/40_GATE_DECISION.md`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01/90_CLOSEOUT.md`

Contexte retenu :

- PR #518 squash-and-merged ;
- `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01` est clos ;
- verdict precedent : `PASS_CONTROLLED_SESSION` ;
- aucune installation globale n'a ete effectuee ;
- aucun `ide.yml` actif ne doit etre suppose ;
- aucune session permanente ne doit etre supposee.

## 6_NON_REOPEN_RULE

Les GO suivants restent fermes et ne sont pas rouverts par ce chantier :

- `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01`
- `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01`
- `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01`

Ils servent uniquement de sources historiques pour les invariants deja prouves.

## 7_CANONICAL_STATE

Etat canonique de depart :

```text
CONTROLLED_SESSION: PASS
GLOBAL_INSTALL: NO
DURABLE_IDE_YML: NO
PERSISTENT_SESSION: NO
GLOBAL_INDEX_CHANGE: NO
REMOTE_REALIGNMENT: NOT_IN_SCOPE
```

## 8_SUCCESS_CRITERIA

Ce GO est reussi si les documents crees permettent de decider un dry-run operateur limite avec :

- une sequence de commandes explicite ;
- une liste claire de commandes interdites ;
- des guards avant toute creation temporaire de `ide.yml` ;
- un cleanup borne et verifiable ;
- un verdict gate ne promettant ni config durable ni workflow reel.

## 9_LIMITS

Ce GO ne prouve pas :

- l'ergonomie finale du layout ;
- la stabilite d'une session operateur longue ;
- la pertinence d'un `ide.yml` durable ;
- l'absence de deltas preexistants sur le repo distant ;
- la securite d'un workflow de trading reel.

## 17_RESUME_POINT

```text
REPRISE:
Construire un protocole operateur minimal doc-only depuis PASS_CONTROLLED_SESSION.

NEXT:
Lire 10_REQUIREMENTS_FROM_CONTROLLED_SESSION.md puis 20_OPERATOR_WORKFLOW_MINIMAL.md.
```
