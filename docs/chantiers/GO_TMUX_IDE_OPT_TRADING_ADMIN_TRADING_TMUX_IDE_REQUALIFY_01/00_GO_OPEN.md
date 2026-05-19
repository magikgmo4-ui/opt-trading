---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
status: active
scope: doc-only
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/20_PREREQUISITES_RECHECK.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/30_TMUX_IDE_RECHECK.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/40_NEXT_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01.md
---

# 00_GO_OPEN

## Objectif

Requalifier `tmux-ide` sur `admin-trading:/opt/trading` apres merge de la sequence desk-pro et sync complet de la machine cible sur `sot/mainline`.

## Contexte

| Element | Etat |
| --- | --- |
| PR `#318` | merged, desk-pro artifact stability integre |
| PR `#320` | merged, post-merge sync documente |
| `admin-trading:/opt/trading` | `sot/mainline @ 3e4506b` |
| desk-pro post-merge gate | PASS, `62 passed` |

## Regles

- Ne pas installer `tmux-ide`.
- Ne pas creer `ide.yml`.
- Ne pas modifier runtime.
- Ne pas toucher `modules/`.
- Ne pas toucher `db-layer`.
- Ne pas toucher `OpenClaw`.
- Cette PR documente uniquement la requalification.
