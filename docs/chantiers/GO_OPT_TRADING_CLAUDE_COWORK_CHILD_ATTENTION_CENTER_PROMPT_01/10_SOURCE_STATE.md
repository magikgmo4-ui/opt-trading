---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01/90_CLOSEOUT.md
  - bundles/claude-artifacts/README.md
---

# 10_SOURCE_STATE

## Etat prouve sur `sot/mainline`

| Element | Etat |
| --- | --- |
| Parent Claude Cowork / Live Artifacts | documente |
| `OPT_TRADING_ATTENTION_CENTER_01` | cible prioritaire etablie |
| Pack `bundles/claude-artifacts/` | `product_closed` |
| Test d'usage reel du pack | PASS |
| Runtime | hors scope |
| `admin-trading` | hors scope |
| TradingView MCP | ferme, hors scope |
| `DOC_OPS BLOCKED` | hors scope |

## Sources utilisees

| Source | Apport |
| --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | cible, invariants, architecture |
| `01_FULL_RESPONSE_CAPTURE.md` | structure recommandee du cockpit et prompt initial |
| `02_REMAINING_GAP.md` | sources autorisees, read-only strict, scoring, etats machine, export |
| `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01/` | preuve que le pack operateur est exploitable |
| `bundles/claude-artifacts/*` | garde-fous et style operateur |

## Synthese source

Le parent Claude Cowork a deja fixe cinq points qui deviennent obligatoires dans ce GO :

1. `OPT_TRADING_ATTENTION_CENTER_01` est le premier Live Artifact a produire.
2. Le Live Artifact est un cockpit dynamique, pas une source canonique.
3. Le mode read-only strict est requis.
4. Le scoring `P0 / P1 / P2` est necessaire pour hierarchiser l'attention.
5. Les etats machine doivent distinguer `ETAT_DECLARE`, `ETAT_VERIFIE` et `HYPOTHESE`.

## Decision locale

Ce GO ne rouvre aucun gap produit du pack Claude Artifacts. Il exploite le pack `product_closed` comme couche operateur pour produire un prompt final stable et executable.

## RISKS

- À qualifier.
