# 40_GATE_DECISION

## 1_MASTER_TARGET

Decider si le workflow operateur minimal peut passer vers un dry-run operateur non destructif.

## 2_ALLOWED_VERDICTS

Verdicts autorises :

```text
ALLOW_OPERATOR_DRY_RUN
HOLD
BLOCKED
```

## 7_CANONICAL_STATE

Elements etablis par ce GO :

- le workflow reste centre sur `admin-trading:/opt/trading` ;
- le package reste `npx -y tmux-ide@1.3.1` ;
- aucun `npm install -g` n'est autorise ;
- aucun `ide.yml` durable n'est autorise ;
- aucune commande Git distante mutante n'est autorisee ;
- aucun workflow applicatif ou trading n'est autorise ;
- les GO fermes restent des references historiques, pas des chantiers rouverts ;
- les index globaux ne sont pas modifies.

## 8_GATE_VERDICT

```text
ALLOW_OPERATOR_DRY_RUN
```
Motif :

- le `PASS_CONTROLLED_SESSION` precedent prouve que `tmux-ide@1.3.1` peut valider, demarrer, inspecter et stopper une session cible ;
- ce GO reduit la suite a un dry-run read-only ;
- le protocole refuse `ide.yml` preexistant et session preexistante ;
- le cleanup ne supprime que les artefacts temporaires crees par le protocole ;
- aucune decision durable n'est prise.

## 9_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_01
```

Objectif recommande :

- executer le protocole de `30_EXECUTION_PROTOCOL.md` ;
- capturer `validate`, `start`, `status`, `inspect`, `stop` et cleanup ;
- conclure `PASS_OPERATOR_DRY_RUN`, `HOLD` ou `BLOCKED`.

## 10_HOLD_CONDITIONS

Basculer en `HOLD` avant ou pendant le prochain GO si :

- `/opt/trading/ide.yml` existe deja ;
- la session `opt-trading-admin-trading` existe deja ;
- le repo distant montre des deltas que l'operateur refuse d'observer en read-only ;
- l'operateur exige un layout different avant execution ;
- l'execution necessite une commande Git mutante ;
- l'execution necessite une decision de realignement repo.

## 11_BLOCKED_CONDITIONS

Basculer en `BLOCKED` si :

- `admin-trading` est inaccessible ;
- `/opt/trading` est absent ;
- `tmux`, `node`, `npx` ou `tmux-ide@1.3.1` sont indisponibles pour le protocole ;
- `validate --json` echoue ;
- le cleanup ne peut pas garantir `POST_SESSION_ABSENT` et `POST_IDE_YML_ABSENT` ;
- une commande destructrice est requise pour continuer.

## 12_INVARIANTS

- `ALLOW_OPERATOR_DRY_RUN` ne vaut pas installation globale.
- `ALLOW_OPERATOR_DRY_RUN` ne vaut pas session permanente.
- `ALLOW_OPERATOR_DRY_RUN` ne vaut pas `ide.yml` durable.
- `ALLOW_OPERATOR_DRY_RUN` ne vaut pas realignement du repo distant.
- `ALLOW_OPERATOR_DRY_RUN` ne vaut pas autorisation de workflow trading.
- Toute suite doit rester separee et documentee.

## 17_RESUME_POINT

```text
REPRISE:
Workflow operateur minimal defini.

NEXT:
ouvrir GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_01 si execution voulue.

GATE:
ALLOW_OPERATOR_DRY_RUN
```

## 18_VERDICT

```text
ALLOW_OPERATOR_DRY_RUN
```
