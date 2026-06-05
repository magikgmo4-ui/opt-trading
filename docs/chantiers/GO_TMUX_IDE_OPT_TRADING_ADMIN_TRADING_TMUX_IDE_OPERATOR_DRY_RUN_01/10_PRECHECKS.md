# 10_PRECHECKS

## 1_MASTER_TARGET

Documenter les prechecks distants executes avant tout lancement `tmux-ide`.

## 2_COMMANDS_EXECUTED

Commandes executees :

```bash
ssh admin-trading "test -d /opt/trading"
ssh admin-trading "cd /opt/trading && pwd && git status --short --branch"
ssh admin-trading "cd /opt/trading && test ! -e ide.yml"
ssh admin-trading "! tmux has-session -t opt-trading-admin-trading"
```

## 3_PRECHECK_RESULTS

| Check | Resultat |
| --- | --- |
| `/opt/trading` existe | PASS |
| repo path | `/opt/trading` |
| `ide.yml` absent avant dry-run | PASS |
| session `opt-trading-admin-trading` absente avant dry-run | PASS |

## 4_REMOTE_GIT_STATE

Etat Git distant observe avant dry-run :

```text
## sot/mainline...origin/sot/mainline [behind 44]
 M docs/index/BRANCH_STATE.md
 M docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
 M webhook_server.py
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

- les deltas distants sont preexistants ;
- ils ne sont pas corriges dans ce GO ;
- le dry-run continue uniquement comme observation read-only ;
- aucune commande `git pull`, `git reset`, `git clean`, `git stash`, `git checkout` ou `git switch` n'est executee sur `admin-trading`.

## 5_PRECHECK_VERDICT

```text
ALLOW_DRY_RUN_EXECUTION_WITH_READONLY_REMOTE_DELTAS
```

## 17_RESUME_POINT

```text
REPRISE:
Prechecks bloquants PASS.
Repo distant sale/en retard, conserve read-only.

NEXT:
Lire 20_DRY_RUN_PROTOCOL.md.
```

## RISKS

- À qualifier.
