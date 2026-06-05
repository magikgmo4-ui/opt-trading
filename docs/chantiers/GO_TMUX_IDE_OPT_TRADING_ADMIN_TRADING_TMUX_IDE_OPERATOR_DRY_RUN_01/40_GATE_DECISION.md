# 40_GATE_DECISION

## 1_MASTER_TARGET

Decider la suite apres le premier dry-run operateur non destructif.

## 2_ALLOWED_VERDICTS

Verdicts attendus pour ce GO :

```text
PASS_OPERATOR_DRY_RUN
HOLD
BLOCKED
```

## 7_CANONICAL_STATE

Elements etablis :

- prechecks distants bloquants : PASS ;
- `ide.yml` absent avant execution ;
- session cible absente avant execution ;
- repo distant en retard et sale, conserve read-only ;
- `ide.yml` temporaire cree ;
- `validate --json` : PASS ;
- lancement `tmux-ide` : FAIL ;
- `START_EXIT=1` ;
- message observe : `tmux command failed` ;
- session apres start : absente ;
- cleanup : PASS ;
- aucun `ide.yml` durable ;
- aucune installation globale ;
- aucune mutation Git distante ;
- aucun workflow applicatif.

## 8_GATE_VERDICT

```text
BLOCKED
```

Motif :

- le dry-run n'a pas atteint l'etat running ;
- `status --json` et `inspect --json` n'ont pas pu etre captures ;
- le blocage est au lancement `tmux-ide`, apres validation statique OK ;
- le cleanup est propre, donc le blocage ne porte pas sur une session persistante.

## 9_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_DRY_RUN_START_FAILURE_DIAG_01
```

Objectif recommande :

- diagnostiquer `tmux command failed` sans installation globale ;
- comparer le layout operator avec le layout controle precedent qui avait demarre ;
- verifier les contraintes de terminal/tmux et de commandes de pane ;
- ne pas creer de `ide.yml` durable ;
- ne pas realigner le repo distant dans ce diagnostic ;
- ne pas relancer un workflow applicatif.

## 10_RETRY_CONDITIONS

Un retry du dry-run ne doit etre autorise qu'apres un GO de diagnostic ou une decision explicite qui etablit :

- cause probable du `tmux command failed` ;
- changement minimal de protocole ou de layout ;
- cleanup attendu ;
- interdiction maintenue des commandes runtime et des mutations Git.

## 11_HOLD_CONDITIONS

Basculer en `HOLD` si la suite exige :

- arbitrage sur les deltas distants preexistants ;
- realignement de `/opt/trading` ;
- changement de layout operateur ;
- decision humaine avant nouveau lancement.

## 12_INVARIANTS_CONFIRMED

- `BLOCKED` ne vaut pas echec de cleanup.
- `BLOCKED` ne vaut pas autorisation de config durable.
- `BLOCKED` ne vaut pas autorisation de realignement Git distant.
- `BLOCKED` ne vaut pas autorisation de workflow trading.
- Toute suite doit rester separee et documentee.

## 17_RESUME_POINT

```text
REPRISE:
Dry-run operator bloque au start tmux-ide.
Validate PASS, start FAIL, cleanup PASS.

NEXT:
ouvrir un GO de diagnostic start failure avant retry.

GATE:
BLOCKED
```

## 18_VERDICT

```text
BLOCKED
```

## RISKS

- À qualifier.
