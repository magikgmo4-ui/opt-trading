---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_INBOX
doc_type: index/inbox
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
created_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/00_GO_OPEN.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/90_CLOSEOUT.md
---

# Inbox - GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01

## Resume

Investigation compatibilite Linux x64 / packaging `tmux-ide` apres blocage `EBADPLATFORM`.

## Statut

- verdict : PARTIAL_PASS
- branche : `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01`
- base : `sot/mainline`
- date : 2026-05-12
- scope : doc-only

## Synthese

| Element | Etat |
| --- | --- |
| `tmux-ide@latest` | `2.1.5` |
| `tmux-ide@2.x` | force `@opentui/core-darwin-arm64` |
| `@opentui/core-linux-x64` | existe |
| `tmux-ide@1.3.1 --version` | PASS sur `admin-trading` |
| `ide.yml` | absent |
| installation | non effectuee |

## Suite

Ouvrir un GO d'essai controle avec `tmux-ide@1.3.1` pinne avant toute installation durable ou creation `ide.yml`.

## RISKS

- À qualifier.
