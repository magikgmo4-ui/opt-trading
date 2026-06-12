---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01
status: active
lifecycle_stage: real_usage
base_branch: sot/mainline
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01
scope: doc-only
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01/90_CLOSEOUT.md
---

# 00_GO_OPEN

## Objectif

Tester le pack `bundles/claude-artifacts/` en usage reel operateur `cursor-ai` apres son passage a `product_closed`, sans rouvrir le closeout produit sauf gap bloqueur prouve.

## Perimetre

Inclus :
- lecture du README comme point d'entree
- utilisation des templates de prompts
- production d'une reprise test via `REPRISE_TEMPLATE.md`
- verification de `NO_COMMIT_RULES.md`
- verification de `CHECKLIST_EXECUTION.md`
- verification de `bundle_meta/manifest.json`
- documentation des gaps reels si presents

Exclus :
- runtime
- `modules/`
- `admin-trading`
- TradingView MCP
- `DOC_OPS BLOCKED`
- modification des index globaux
- reouverture du closeout produit si aucun gap bloqueur n'est prouve

## Invariants

- doc-only
- aucun secret
- aucun runtime
- aucune modification `modules/`
- aucun changement `admin-trading`
- aucun changement TradingView MCP
- aucun changement `DOC_OPS BLOCKED`
- aucun index global modifie

## Criteres de verdict

PASS si :
- le pack permet une reprise operateur sans chercher ailleurs
- les templates sont directement utilisables
- le template de reprise est suffisant
- les regles no-commit couvrent les risques principaux
- la checklist couvre commit, push, PR et post-merge
- le manifest identifie le pack, son statut, sa version et ses invariants
- aucun gap bloqueur n'est detecte

FAIL si :
- un artefact manque
- un template est ambigu ou inutilisable
- la checklist ne couvre pas un risque operateur important
- le manifest n'est pas exploitable
- une source externe non documentee est necessaire

## RISKS

- À qualifier.
