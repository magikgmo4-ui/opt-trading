# 40_GATE_DECISION

## 1_MASTER_TARGET

Decider la suite apres la premiere session controlee `tmux-ide`.

## 7_CANONICAL_STATE

Elements etablis :

- `tmux-ide@1.3.1 validate --json` : PASS ;
- session `opt-trading-admin-trading` creee ;
- `status --json` : session running avec 3 panes ;
- `inspect --json` : config valide, 2 rows, 3 panes ;
- `stop` : PASS ;
- session absente apres stop ;
- `/opt/trading/ide.yml` supprime ;
- aucune installation globale.

## 8_GATE_VERDICT

```text
PASS_CONTROLLED_SESSION
```

Motif :

- la session a demarre ;
- les panes attendues ont ete exposees par `status` et `inspect` ;
- le timeout a seulement borne l'attache TUI ;
- la session a ete fermee proprement ;
- le fichier temporaire `ide.yml` a ete supprime.

## 9_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_SESSION_ERGONOMICS_REVIEW_01
```

Objectif recommande :

- reviewer l'ergonomie du layout observe ;
- decider si le pane `Docs` doit rester a 30% ou etre restructure ;
- decider si le repo distant doit etre realigne avant une config durable ;
- ne pas installer globalement ;
- ne pas creer de session permanente sans nouveau gate.

## 10_HOLD_BEFORE_DURABLE_CONFIG

La config durable reste en attente car `admin-trading:/opt/trading` est derriere `origin/sot/mainline` et contient des deltas preexistants hors scope.

Avant un `ide.yml` durable, il faut un GO separe pour au moins l'une des deux decisions :

- realignement repo distant ;
- review ergonomie/session avant persistance.

## 12_INVARIANTS

- `PASS_CONTROLLED_SESSION` ne vaut pas installation globale.
- `PASS_CONTROLLED_SESSION` ne vaut pas session permanente.
- `PASS_CONTROLLED_SESSION` ne vaut pas `ide.yml` durable.
- Toute suite doit rester separee et documentee.

## 17_RESUME_POINT

```text
REPRISE:
Session controlee PASS.
No active ide.yml.
No running session.

NEXT:
ouvrir une review ergonomie/session ou un realignement repo distant avant config durable.
```

## 18_VERDICT

```text
PASS_CONTROLLED_SESSION
```
