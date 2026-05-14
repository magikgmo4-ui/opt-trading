---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/20_NPM_METADATA.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/30_LINUX_X64_PROBES.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/40_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01.md
---

# 00_GO_OPEN

## Objectif

Comprendre pourquoi `npx -y tmux-ide --version` resout `@opentui/core-darwin-arm64` sur `admin-trading` Linux x64, puis identifier une voie compatible sans installer `tmux-ide` ni creer `ide.yml`.

## Contexte

| Element | Etat |
| --- | --- |
| PR `#321` | merged, `5c827261` |
| `admin-trading:/opt/trading` | `sot/mainline @ 5c82726` |
| `tmux/node/npm/npx` | PASS |
| `tmux-ide@latest` | FAIL, `EBADPLATFORM` |
| `ide.yml` | absent |

## Regles

- Ne pas installer `tmux-ide` dans le repo.
- Ne pas creer `ide.yml`.
- Ne pas modifier runtime.
- Ne pas toucher `modules/`.
- Investigation metadata/probes uniquement.
