# 30_RETRY_DRY_RUN_RESULTS

## 1_MASTER_TARGET

Documenter les resultats du retry operateur avec guard TTY.

## 2_VALIDATE_RESULT

Commande :

```bash
npx -y tmux-ide@1.3.1 validate --json
```

Sortie :

```json
{
  "valid": true,
  "errors": []
}
```

Verdict :

```text
VALIDATE_PASS
```

## 3_TTY_GUARD_RESULT

```text
STTY_BEFORE=0 0
STTY_GUARD_BEFORE=0 0
STTY_GUARD_AFTER=50 200
```

Interpretation :

- le cas racine `TTY size 0x0` est reproduit ;
- le guard applique une taille non nulle avant `tmux-ide` ;
- le start n'utilise plus le chemin `-x 0 -y 0`.

## 4_START_RESULT

Commande :

```bash
timeout 12s npx -y tmux-ide@1.3.1
```

Sorties utiles :

```text
Starting "opt-trading-admin-trading" (2 rows, 3 panes)...
SESSION_PRESENT_AFTER_START=YES
START_EXIT=124
```

Interpretation :

- `124` correspond au timeout attendu de l'attache interactive ;
- la session a bien ete creee ;
- le blocage precedent `tmux command failed` n'est pas reproduit.

## 5_STATUS_RESULT

Commande :

```bash
npx -y tmux-ide@1.3.1 status --json
```

Synthese :

```text
session = opt-trading-admin-trading
running = true
configExists = true
panes = 3
```

Panes observees :

```text
Shell width=99 height=32 active=true
Git   width=100 height=32 active=false
Docs  width=200 height=14 active=false
```

## 6_INSPECT_RESULT

Commande :

```bash
npx -y tmux-ide@1.3.1 inspect --json
```

Synthese :

```text
valid = true
session = opt-trading-admin-trading
summary.rows = 2
summary.panes = 3
focus = rows.0.panes.0
tmux.running = true
```

Commandes de panes confirmees :

```text
Shell: pwd && git status --short --branch
Git: git log --oneline -5 && git status --short --branch
Docs: find docs/chantiers -maxdepth 1 -type d -name 'GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_*' | sort | tail -20
```

## 7_STOP_AND_CLEANUP_RESULT

Commande :

```bash
npx -y tmux-ide@1.3.1 stop
```

Sortie :

```text
Stopped session "opt-trading-admin-trading"
```

Checks post-run :

```text
POST_SESSION_ABSENT=YES
POST_IDE_YML_ABSENT=YES
POST_TEMP_SCRIPT_ABSENT=YES
RETRY_GUARD_SCRIPT_PASS
```

Checks independants apres retour local :

```text
POST_IDE_YML_ABSENT=YES
POST_SESSION_ABSENT=YES
POST_TEMP_SCRIPT_ABSENT=YES
```

## 8_REMOTE_GIT_RESULT

Etat Git distant apres cleanup :

```text
## sot/mainline...origin/sot/mainline
?? docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/
?? docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/
?? docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/
?? docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/
?? docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/
?? docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/
?? docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/
?? docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/
?? docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/
?? docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01.md
?? docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01.md
?? docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01.md
?? docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01.md
?? docs/index/inbox/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01.md
?? docs/index/inbox/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01.md
?? docs/index/inbox/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01.md
?? docs/index/inbox/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01.md
?? docs/index/inbox/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01.md
```

Interpretation :

- les deltas distants preexistants restent inchanges dans le cadre observe ;
- le `ide.yml` temporaire n'est plus present ;
- aucune mutation Git distante n'a ete executee.

## 18_VERDICT

```text
PASS_OPERATOR_DRY_RUN
```
