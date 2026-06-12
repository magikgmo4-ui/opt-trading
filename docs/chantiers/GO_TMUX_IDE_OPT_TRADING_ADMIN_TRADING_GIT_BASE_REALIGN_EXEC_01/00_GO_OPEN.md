---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
status: active
scope: doc-only + exec-ssh
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
parent_go: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/10_BEFORE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/20_EXECUTION_LOG.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/30_AFTER_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01`

## Objectif

Remettre `admin-trading:/opt/trading` sur une base Git canonique propre (`sot/mainline`), sans installer tmux-ide, sans modifier runtime, sans toucher db-layer/OpenClaw.

## Contexte

- PR #304 mergée dans `sot/mainline` (`6373d455`) le 2026-05-12.
- Le GO parent `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01` a documenté et borné le réalignement.
- L'état Git non canonique observé sur `admin-trading:/opt/trading` le 2026-05-11 :
  - branche : `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01`
  - upstream : `origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01`
- Ce GO exécute le réalignement réel.

## Règles

- Ne pas installer tmux-ide.
- Ne pas créer ide.yml.
- Ne pas modifier modules/.
- Ne pas toucher runtime.
- Ne pas toucher db-layer ni OpenClaw.
- Ne pas faire de reset destructif sans backup préalable.
- Documenter l'état avant et après.

## Machine source

cursor-ai (Windows)

## Machine cible

admin-trading, répertoire `/opt/trading`

## Périmètre Git

- Source canonique : `origin/sot/mainline` (HEAD ≥ `6373d455`)
- Opération : fetch/prune → switch `sot/mainline` → pull --rebase

## Structure

| Fichier | Rôle |
| --- | --- |
| `10_BEFORE_STATE.md` | État Git capturé avant toute opération |
| `20_EXECUTION_LOG.md` | Log des commandes exécutées avec sortie réelle |
| `30_AFTER_STATE.md` | État Git capturé après réalignement |
| `90_CLOSEOUT.md` | Verdict PASS/FAIL |

## RISKS

- À qualifier.
