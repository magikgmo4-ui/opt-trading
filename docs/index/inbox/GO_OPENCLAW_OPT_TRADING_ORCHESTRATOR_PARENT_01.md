---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: inbox
surface: index
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/index/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01

## Objet

Transport court de reprise pour le parent OpenClaw `db-layer` hors continuite canonique.

## Etabli

 - parent reel prouve sur branche dediee : `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
 - machine cible : `db-layer`
 - prochain GO metier attendu : `GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01`

## Regle

- ne pas reprendre la branche parent brute comme base active
- ne pas toucher au runtime dans cette passe
- realigner d'abord la documentation canonique

## Point De Reprise

 - lire `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md`
 - ouvrir ensuite le child `GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01`

## RISKS

- À qualifier.
