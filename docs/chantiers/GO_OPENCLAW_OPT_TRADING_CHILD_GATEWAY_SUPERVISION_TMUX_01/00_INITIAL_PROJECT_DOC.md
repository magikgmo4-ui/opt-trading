---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-05
topic_keys:
  - openclaw
  - tmux
  - gateway
  - db-layer
  - supervision
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01

## Classification

- type : child runtime doc-first
- statut : open
- machine cible : `db-layer`
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

## But

Stabiliser le Gateway OpenClaw sur `db-layer` via une supervision `tmux` bornee, sous utilisateur `openclaw`, en loopback only.

## ETABLI

- ce child n'existait pas dans le repo au moment du realignement documentaire
- son ouverture vient du plan `11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md` du parent OpenClaw
- aucun changement runtime n'est inclus dans ce squelette

## Perimetre du futur lot

- cadrage tmux session `openclaw-gateway`
- scripts `start/status/stop` documentes
- verification loopback `127.0.0.1:18789`
- aucun bridge V1 tant que la supervision tmux n'est pas validee

## Hors Perimetre

- bridge OpenClaw
- policy runtime large
- exposition WAN
- admin-trading
- systemd durable dans cette passe d'ouverture

## NEXT_GO

Point de reprise suivant : completer le cadrage et les preuves doc-first de supervision tmux avant toute action runtime.
