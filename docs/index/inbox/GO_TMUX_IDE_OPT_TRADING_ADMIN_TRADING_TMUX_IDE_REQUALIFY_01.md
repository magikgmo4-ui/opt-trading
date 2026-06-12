---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01_INBOX
doc_type: index/inbox
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
status: active
scope: doc-only
created_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/00_GO_OPEN.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/90_CLOSEOUT.md
---

# Inbox - GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01

## Resume

Requalification `tmux-ide` sur `admin-trading:/opt/trading` apres merge desk-pro et sync complet sur `sot/mainline`.

## Statut

- verdict : BLOCKED
- branche : `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01`
- base : `sot/mainline`
- date : 2026-05-12
- scope : doc-only

## Synthese

| Element | Etat |
| --- | --- |
| `admin-trading` Git | `sot/mainline @ 3e4506b`, clean |
| `tmux` | PASS, `3.3a` |
| `node` | PASS, `v18.20.4` |
| `npm` / `npx` | PASS, `9.2.0` |
| `tmux-ide` | absent |
| `npx tmux-ide` | FAIL, `EBADPLATFORM` |
| `ide.yml` | absent |

## Suite

Ouvrir un GO d'investigation compatibilite Linux x64 / packaging `tmux-ide` avant toute installation ou creation `ide.yml`.

## RISKS

- À qualifier.
