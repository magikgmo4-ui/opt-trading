---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01_20_REAL_USAGE_SCENARIO
doc_type: chantier/real_usage_scenario
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_REAL_USAGE_01
status: active
scope: doc-only
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
---

# 20_REAL_USAGE_SCENARIO

## Scenario teste

Un operateur `cursor-ai` ouvre un nouveau GO doc-only et veut piloter tout le flux localement :

1. identifier rapidement le bon pack ;
2. verifier son statut produit ;
3. generer une reprise operateur ;
4. verifier les regles no-commit ;
5. verifier la checklist avant PR ;
6. confirmer le statut et les invariants dans le manifest.

## Parcours reel execute

### Etape 1 — Point d'entree

Le README suffit pour :
- identifier le pack ;
- confirmer qu'il est `PRODUCT_CLOSED` ;
- connaitre ses 6 artefacts ;
- comprendre qu'il ne ferme ni `alert_webhook` ni le workflow Bundles global.

### Etape 2 — Generation d'une reprise

`PROMPT_TEMPLATES.md` fournit un template de reprise complet avec :
- role ;
- repo ;
- branche canonique ;
- contraintes ;
- etapes Git ;
- criteres de PASS.

Le template est instanciable en remplaçant simplement `<GO_ID>`, l'etat valide, l'objectif et les etapes specifiques.

### Etape 3 — Fiche de reprise test

`REPRISE_TEMPLATE.md` permet de produire une fiche de reprise standard contenant :
- `7_CANONICAL_STATE`
- `13_ESTABLISHED`
- `14_HYPOTHESIS`
- `15_REMAINING_GAP`
- `16_TODO`
- `17_RESUME_POINT`

### Etape 4 — Gate de securite

`NO_COMMIT_RULES.md` couvre les risques principaux :
- secrets
- `.env`
- tokens
- outputs live
- payloads reels
- chemins prives non anonymises

### Etape 5 — Checklist avant PR

`CHECKLIST_EXECUTION.md` couvre :
- pre-commit
- pre-push
- pre-PR
- post-merge

### Etape 6 — Confirmation technique

`bundle_meta/manifest.json` suffit pour confirmer :
- `bundle_id`
- `bundle_type`
- `machine`
- `status`
- `lifecycle_stage`
- `version`
- liste des fichiers
- invariants de securite

## RISKS

- À qualifier.
