---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
lifecycle_stage: prompt_finalization
base_branch: sot/mainline
branch: go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01/90_CLOSEOUT.md
  - bundles/claude-artifacts/README.md
---

# 00_GO_OPEN

## Objectif

Produire le prompt final executable pour `OPT_TRADING_ATTENTION_CENTER_01`, un Live Artifact Claude Cowork en mode read-only strict servant de cockpit dynamique pour `opt-trading`.

## Finalite

Le prompt doit permettre a Claude Cowork de repondre a une question unique :

```text
Qu'est-ce qui necessite mon attention maintenant, pourquoi, avec quelle preuve, et quelle est la prochaine action prioritaire ?
```

## Perimetre

Inclus :
- spec operateur Attention Center
- sources autorisees en lecture seule
- scoring `P0 / P1 / P2`
- regles de preuve machine `ETAT_DECLARE / ETAT_VERIFIE / HYPOTHESE`
- format d'export journalise
- prompt final directement collable

Exclus :
- runtime
- `modules/`
- `admin-trading`
- TradingView MCP
- `DOC_OPS BLOCKED`
- toute ecriture externe par Claude Cowork
- modification des index globaux

## Invariants

- doc-only
- aucun runtime
- aucun `modules/`
- aucun `admin-trading`
- aucun TradingView MCP
- aucun `DOC_OPS BLOCKED`
- aucune ecriture externe par Claude Cowork
- repo/docs/Git restent la verite canonique
- le Live Artifact reste read-only

## Resultat attendu

- `70_FINAL_PROMPT.md` est directement utilisable
- les sources autorisees sont explicites
- le mode read-only strict est integre
- le scoring `P0 / P1 / P2` est fige
- les regles de preuve machine sont non ambigues
- le format `reports/YYYY-MM-DD_ATTENTION_CENTER_SUMMARY.md` est documente

## RISKS

- À qualifier.
