---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
opened_at: 2026-05-11
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
parent_go: GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/01_plan.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`

## Objet immediat

Poser un cadrage court de verification de topologie avant toute implementation reelle `tmux-ide`.

## Perimetre de cette ouverture

- doc-only
- aucun runtime
- aucun `modules/`
- aucune installation `tmux-ide`
- aucune modification OpenClaw
- aucune ecriture hors `docs/`

## Question a trancher

Sur quelle topologie doit s'ouvrir l'implementation de base `tmux-ide`, sans casser le runtime
OpenClaw deja PASS sur `db-layer` ?

## Decision attendue

- `cursor-ai` reste le poste operateur / IDE / Git / PR
- `db-layer` reste le runtime OpenClaw / gateway tmux existant
- la premiere cible `tmux-ide` a valider n'est pas `db-layer`
- la cible a verifier en priorite est `admin-trading`, deja creditee dans les surfaces `tmux-ide`

## Livrables

- `10_SOURCE_STATE.md`
- `20_TARGET_TOPOLOGY_CHECK.md`
- `30_MACHINE_DECISION.md`
- `40_IMPL_OPENING_GATES.md`
- `90_CLOSEOUT.md`

## Suite attendue

Si le check est PASS, la phase suivante de `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` pourra viser
une validation reelle `cursor-ai -> SSH -> admin-trading`, sans intervention sur `db-layer`.

## RISKS

- À qualifier.
