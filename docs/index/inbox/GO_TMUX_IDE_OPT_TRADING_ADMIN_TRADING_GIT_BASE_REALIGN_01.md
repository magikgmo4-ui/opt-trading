---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
status: active
scope: doc-only
---

# GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01

Ouverture doc-only du realignement Git `admin-trading` avant toute qualification `tmux-ide`.

Constat de depart:
- `/opt/trading` existe sur `admin-trading`
- repo propre
- branche et upstream non canoniques pour le GO courant
- `tmux-ide` et `ide.yml` encore absents

Invariant:
- aucun `db-layer`
- aucun OpenClaw
- aucun runtime
