---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
status: active
scope: doc-only
opened_at: 2026-05-11
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
parent_go: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/50_REAL_VALIDATION_PREFLIGHT.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/70_GATE_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01`

## But

Remettre `/opt/trading` sur `admin-trading` sur une base Git canonique propre
avant toute qualification `tmux-ide` / `ide.yml`.

## Origine du besoin

Le preflight reel de `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` a prouve:

- la topologie `cursor-ai -> SSH -> admin-trading`
- la presence du repo `/opt/trading`
- l'absence de `tmux-ide`
- l'absence de `ide.yml`
- un etat Git propre mais non canonique pour le GO courant

## Perimetre

- doc-only
- aucun runtime
- aucune installation `tmux-ide`
- aucune modification `db-layer`
- aucune modification OpenClaw
- aucun changement `modules/`

## Resultat attendu

- cible Git canonique definie pour `admin-trading`
- ecart courant documente
- gates d'execution machine-first posees
- suite explicite vers qualification `tmux-ide`

## RISKS

- À qualifier.
