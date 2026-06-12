# 10_PRE_SESSION_BASELINE

## 1_MASTER_TARGET

Documenter la baseline avant lancement de session `tmux-ide`.

## 7_CANONICAL_STATE

Source :

```text
admin-trading:/opt/trading
```

Commande de baseline principale :

```bash
ssh admin-trading "bash -lc 'cd /opt/trading && ...'"
```

## 8_ENVIRONMENT_BASELINE

| Element | Resultat |
| --- | --- |
| Hostname | `admin-trading` |
| OS | `Linux admin-trading 6.1.0-44-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.164-1 (2026-03-09) x86_64 GNU/Linux` |
| `tmux` | `tmux 3.3a` |
| `node` | `v18.20.4` |
| `npm` | `9.2.0` |
| `npx` | `/usr/bin/npx` |
| repo | `/opt/trading` |
| active `ide.yml` avant trial | absent |
| session `opt-trading-admin-trading` avant trial | absente |

## 9_REPO_STATE_NOTE

Le repo distant `admin-trading:/opt/trading` avait deja des modifications et fichiers non suivis hors scope avant ce GO :

```text
## sot/mainline...origin/sot/mainline [derriere 44]
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

Ces deltas etaient preexistants et n'ont pas ete modifies par ce GO.

## 10_PREFLIGHT_RESULT

```text
ACTIVE_IDE_YML_ABSENT
SESSION_PREEXISTS=NO
```

## 12_INVARIANTS

- Ne pas nettoyer les deltas distants preexistants.
- Ne pas toucher aux index globaux distants.
- Ne pas ecraser un `ide.yml` existant.
- Ne pas tuer une session preexistante.

## 17_RESUME_POINT

Baseline compatible avec un trial controle : aucun `ide.yml` actif et aucune session cible avant lancement.

## RISKS

- À qualifier.
