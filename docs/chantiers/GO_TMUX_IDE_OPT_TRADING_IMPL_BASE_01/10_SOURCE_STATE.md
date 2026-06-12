---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
captured_at: 2026-05-11
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/01_plan.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_RISK_MAP_01/20_MACHINE_RUNTIME_DEPENDENCIES.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
---

# 10_SOURCE_STATE

## Etat Git

- base locale: `sot/mainline`
- branche de travail: `go/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- source de reprise globale: `REPRISE.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`

## Faits etablis retenus

### 1. `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` est le prochain GO canonique

Preuve:

- `docs/index/REPRISE.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`

### 2. Le cadrage `tmux-ide` historique pointe une cible par defaut a revalider

Preuve:

- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`

Etat retenu:

- cible par defaut documentee: `admin-trading`
- statut de cette cible: a revalider contre l'etat reel

### 3. `db-layer` porte deja un runtime tmux/OpenClaw PASS

Preuve:

- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md`

Etat retenu:

- machine: `db-layer`
- session tmux: `openclaw-gateway`
- invariant: ne pas casser ce runtime par un lot `tmux-ide` non qualifie

### 4. `cursor-ai` est une surface operateur, pas un runtime OpenClaw

Preuve:

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_RISK_MAP_01/20_MACHINE_RUNTIME_DEPENDENCIES.md`
- `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md`

Etat retenu:

- `cursor-ai`: observation / docs / transport / Windows IDE
- `db-layer`: orchestration / OpenClaw / infra

### 5. `admin-trading` reste une machine prouvee et recitee dans les surfaces `tmux-ide`

Preuve:

- `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md`

Etat retenu:

- `admin-trading` est prouvee comme machine autonome
- elle reapparait comme cible de travail creditee dans les surfaces `tmux-ide`
- elle ne doit pas etre melangee avec `db-layer`

## Conclusion source-state

Le check de topologie doit arbitrer entre:

- `cursor-ai` comme poste operateur
- `admin-trading` comme premiere cible `tmux-ide` a valider
- `db-layer` comme zone runtime protegee a ne pas reutiliser par defaut pour `tmux-ide`

## RISKS

- À qualifier.
