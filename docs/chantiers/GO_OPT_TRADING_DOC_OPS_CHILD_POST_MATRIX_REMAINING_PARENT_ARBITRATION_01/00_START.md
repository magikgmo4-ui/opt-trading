---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01_START
doc_type: start
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01
status: open
lifecycle_stage: start
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/BRANCH_STATE.md
---

# 00_START

## Contexte

- Reprise post-PR `#197`, merge commit `ed754a6`.
- Base canonique retenue : `sot/mainline`.
- Branche de travail corrigee au depart :
  `go/GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01`
  suit maintenant
  `origin/go/GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01`.
- Les familles gouvernance, matrice et naming sont fermees et ne doivent pas etre rouvertes ici.

## Objectif

Arbitrer les parents restants apres le closeout matrice, sans reinventer les chantiers deja ouverts et sans creer de nouveau parent si un parent ouvert couvre deja le besoin.

## Contrainte directrice

- Maintenir idealement `1` chantier principal ouvert par machine.
- Ne pas empiler plusieurs chantiers principaux sur une meme machine.
- Ne pas absorber les parents projet ou runtime dans un parent machine.

## Invariants retenus

- `GO_INDEX.md` reste la verite des GO non clos.
- `GO_CLOSED_INDEX.md` garde les clos.
- `GO_PARENT_THREAD_MAP.md` reste derive.
- `BRANCH_STATE.md` reste borne a la surface branches.
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` reste un parent projet.
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` reste un parent runtime.
- `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` reste le fil principal `cursor-ai`.
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` doit etre consolide sous `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`.
- `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` doit etre rattache a `student` et reste differe.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste a considerer plus tard, apres clarification ou closeout des GO OpenClaw deja actifs.

## Ajouts utilisateur integres dans l'arbitrage

- `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
- `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`
- `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

## Cible de sortie

Produire un arbitrage doc-only minimal couvrant :

- classification des parents et GO restants ;
- carte machine -> chantier principal recommande ;
- ordre final de reprise ;
- verdict explicite `PASS` ou `FAIL`.
