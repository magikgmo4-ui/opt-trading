---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01_INBOX
doc_type: index/inbox
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
status: active
scope: doc-only + exec-ssh
created_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/00_GO_OPEN.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/90_CLOSEOUT.md
---

# Inbox — GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01

## Résumé

Exécution du réalignement Git sur `admin-trading:/opt/trading` vers `sot/mainline`.

## Statut

- verdict : PENDING_EXECUTION
- branche : `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01`
- base : `sot/mainline` (≥ `6373d455`, PR #304)
- date : 2026-05-12
- scope : doc-only + exec-ssh

## État avant (ETAT_DECLARE, 2026-05-11)

- branche admin-trading : `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01`
- worktree : clean
- SSH : PASS

## Action requise

Exécuter la séquence SSH depuis cursor-ai (voir `20_EXECUTION_LOG.md`), remplir les champs `À_CAPTURER`, puis mettre `90_CLOSEOUT.md` à `PASS` ou `FAIL`.

## Prochain GO après PASS

`GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
