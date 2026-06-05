---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01
status: active
scope: doc-only
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01/00_GO_OPEN.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01/90_CLOSEOUT.md
---

# 10_SOURCE_STATE

## Etat prouve sur `sot/mainline`

| Element | Etat prouve |
| --- | --- |
| PR closeout produit | `#264` mergee |
| Pack cible | `bundles/claude-artifacts/` |
| Statut pack | `product_closed` |
| Version manifest | `1.0.1` |
| Machine cible | `cursor-ai` |
| Scope bundle | `claude-artifacts-pack-only` |

## Surfaces lues pour le test

| Surface | Role dans le test |
| --- | --- |
| `bundles/claude-artifacts/README.md` | Point d'entree operateur |
| `bundles/claude-artifacts/PROMPT_TEMPLATES.md` | Templates de prompts |
| `bundles/claude-artifacts/REPRISE_TEMPLATE.md` | Template de reprise |
| `bundles/claude-artifacts/NO_COMMIT_RULES.md` | Gate no-secret / no-sensitive |
| `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` | Checklist pre-commit a post-merge |
| `bundles/claude-artifacts/bundle_meta/manifest.json` | Identite, statut, version, invariants |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01/` | Closeout produit de reference |

## Hypothese de test retenue

Le test se place dans un cas reel simple :

1. un operateur `cursor-ai` doit reprendre un nouveau GO doc-only ;
2. il ne veut pas chercher de doctrine ailleurs que dans le pack ;
3. il utilise le pack pour preparer sa reprise, ses garde-fous et sa verification avant PR.

## Etat attendu

Le pack doit suffire sans patch bundle si :
- le README oriente correctement ;
- les templates sont instanciables sans recherche externe ;
- le template de reprise est executable ;
- les garde-fous de commit et de PR sont compréhensibles ;
- le manifest confirme le statut `product_closed` et la version `1.0.1`.

## RISKS

- À qualifier.
