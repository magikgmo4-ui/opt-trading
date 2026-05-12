---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_INBOX
doc_type: index/inbox
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: active
scope: doc-only
created_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/00_GO_OPEN.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/90_CLOSEOUT.md
---

# Inbox — GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01

## Résumé

Qualification tmux-ide et ide.yml sur `admin-trading:/opt/trading` après réalignement Git.

## Statut

- verdict : PARTIAL_PASS
- branche : `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01`
- base : `sot/mainline`
- date : 2026-05-12
- scope : doc-only

## Synthèse

| Élément | État |
| --- | --- |
| SSH + Git base | PASS (ETAT_DECLARE) |
| tmux / node / npm / npx | PASS (ETAT_DECLARE) |
| tmux-ide | ABSENT — gate non franchie |
| ide.yml | ABSENT — gate non franchie |
| re-probes live | À_CAPTURER |

## Action requise

Exécuter les re-probes SSH (voir fichiers 10/20/30/40), remplir les champs À_CAPTURER, confirmer PARTIAL_PASS.

## Prochain GO

`GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_INSTALL_01` — installer tmux-ide, créer ide.yml, doctor + validate.
