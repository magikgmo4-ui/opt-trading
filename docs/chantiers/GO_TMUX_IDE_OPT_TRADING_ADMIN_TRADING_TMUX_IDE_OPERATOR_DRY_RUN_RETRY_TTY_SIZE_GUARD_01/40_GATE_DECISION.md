# 40_GATE_DECISION

## 1_MASTER_TARGET

Decider la suite apres retry operateur avec guard TTY.

## 2_ALLOWED_VERDICTS

Verdicts pour ce GO :

```text
PASS_OPERATOR_DRY_RUN
HOLD
BLOCKED
```

## 7_CANONICAL_STATE

Elements etablis :

- PR #523 merged ;
- worktree GO isole ouvert depuis `origin/sot/mainline @ d9210be3` ;
- worktree principal non avance car des fichiers non suivis locaux seraient ecrases ;
- prechecks distants bloquants PASS ;
- `ssh -tt` expose encore `STTY_SIZE=0 0` ;
- guard `stty rows 50 cols 200` applique ;
- `validate --json` PASS ;
- start `tmux-ide@1.3.1` PASS avec session presente ;
- `START_EXIT=124`, attendu pour l'attache bornee par `timeout` ;
- `status --json` PASS ;
- `inspect --json` PASS ;
- `stop` PASS ;
- cleanup PASS ;
- aucun `ide.yml` durable ;
- aucune installation globale ;
- aucun `tmux kill-server` global ;
- aucune mutation Git distante ;
- aucun workflow applicatif lance ;
- aucun index global modifie.

## 8_GATE_VERDICT

```text
PASS_OPERATOR_DRY_RUN
```

Motif :

- le guard TTY corrige le mode de defaillance isole ;
- la session operateur demarre avec 2 rows et 3 panes ;
- `status --json` et `inspect --json` confirment la session ;
- cleanup complet confirme l'absence d'artefact durable.

## 9_PROTOCOL_RULE

Regle operatoire a conserver pour les prochains lancements `tmux-ide` via SSH/Codex :

```bash
printf 'STTY_BEFORE='
stty size 2>/dev/null || echo no-stty
stty rows 50 cols 200 2>/dev/null || true
printf 'STTY_AFTER='
stty size 2>/dev/null || echo no-stty
```

Le start est autorise seulement si :

```text
STTY_AFTER != 0 0
```

## 10_NEXT_OPTIONS

Options apres publication/merge de ce GO :

- documenter la regle comme invariant d'execution tmux-ide pour `admin-trading` ;
- ouvrir un GO de stabilisation du workflow operateur si un protocole durable est souhaite ;
- rester en `HOLD` avant toute creation de `ide.yml` durable.

## 17_RESUME_POINT

```text
REPRISE:
Retry operateur avec guard TTY = PASS.
Guard obligatoire: stty rows 50 cols 200 avant tmux-ide sous ssh -tt quand stty size vaut 0 0.

GATE:
PASS_OPERATOR_DRY_RUN
```
