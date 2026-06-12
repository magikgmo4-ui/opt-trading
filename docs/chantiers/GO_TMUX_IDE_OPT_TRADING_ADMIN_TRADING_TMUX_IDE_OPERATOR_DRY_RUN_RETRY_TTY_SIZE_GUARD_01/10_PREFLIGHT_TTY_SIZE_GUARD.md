# 10_PREFLIGHT_TTY_SIZE_GUARD

## 1_MASTER_TARGET

Documenter les preflights et le guard TTY applique avant relance `tmux-ide`.

## 2_REMOTE_TARGET

```text
host = admin-trading
repo = /opt/trading
session = opt-trading-admin-trading
script = /tmp/tmux_ide_operator_dry_run_retry_tty_size_guard_01.sh
package = npx -y tmux-ide@1.3.1
```

## 3_PREREQUISITES

PR diagnostic amont :

```text
#523 = MERGED
merge commit = d9210be3
```

## 4_PREFLIGHT_RESULTS

Prechecks distants :

```text
PRE_REPO_EXISTS=YES
/opt/trading
PRE_IDE_YML_ABSENT=YES
PRE_SESSION_ABSENT=YES
```

Etat Git distant observe avant retry :

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

- les fichiers non suivis distants sont preexistants ;
- ils sont conserves read-only ;
- aucun realignement Git distant n'est execute ;
- le retry reste limite a une session `tmux-ide` ephemere.

## 5_TTY_BASELINE

Probe `ssh -tt` avant retry :

```text
TTY=/dev/pts/1
STTY_SIZE=0 0
TERM=dumb
SSH_TTY=/dev/pts/1
```

Dans le script de retry, `TERM` est force pour `tmux-ide` :

```text
TERM=xterm-256color
```

## 6_TTY_GUARD

Guard execute apres `validate --json` et avant le lancement :

```bash
printf 'STTY_GUARD_BEFORE='
stty size 2>/dev/null || echo no-stty
stty rows 50 cols 200 2>/dev/null || true
printf 'STTY_GUARD_AFTER='
stty size 2>/dev/null || echo no-stty
```

Resultat observe :

```text
STTY_GUARD_BEFORE=0 0
STTY_GUARD_AFTER=50 200
```

## 7_PREFLIGHT_VERDICT

```text
ALLOW_RETRY_WITH_TTY_SIZE_GUARD
```

## 17_RESUME_POINT

```text
REPRISE:
Prechecks bloquants PASS.
TTY size 0 0 confirme.
Guard stty rows 50 cols 200 applique.

NEXT:
Lire 20_RETRY_GUARD_PROTOCOL.md.
```

## RISKS

- À qualifier.
