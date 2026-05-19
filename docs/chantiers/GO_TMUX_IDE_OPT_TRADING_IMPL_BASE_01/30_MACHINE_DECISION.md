---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_30_MACHINE_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
---

# 30_MACHINE_DECISION

## Decision posee

### 1. `cursor-ai`

Role retenu:

- poste operateur
- IDE
- Git / PR
- point de depart de l'implementation

Ce lot ne cherche pas a transformer `cursor-ai` en runtime `tmux-ide` principal.

### 2. `db-layer`

Role retenu:

- runtime OpenClaw
- gateway tmux deja PASS
- zone a ne pas modifier par defaut dans `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`

Consequence:

- aucune installation ni validation `tmux-ide` sur `db-layer` dans la premiere passe
- aucune intervention sur `openclaw-gateway`

### 3. `admin-trading`

Role retenu:

- premiere machine cible a verifier pour l'implementation `tmux-ide`

Justification:

- cible par defaut deja documentee dans le cadrage `tmux-ide`
- machine prouvee et isolee dans son parent machine
- permet de separer le poste operateur du runtime OpenClaw `db-layer`

## Formulation canonique de reprise

`GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` doit s'ouvrir comme un lot de validation
`cursor-ai -> SSH -> admin-trading`, avec `db-layer` borne en zone runtime protegee.

## Ce qui n'est pas decide ici

- prerequis reels `tmux`, `node`, `npm`, `tmux-ide`
- chemin repo reel sur `admin-trading`
- contenu final de `ide.yml`
- panes definitifs

Ces points relèvent de l'implementation reelle suivante.
