---
doc_id: BUNDLE_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
doc_type: bundle/operator_pack
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_pack
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/
---

# Claude Artifacts Operator Pack

## Objectif

Ce pack transforme les artefacts Claude / IDE Bundle / Claude cowork live artifacts deja integres dans le repo en pack operateur cursor-ai stable et reproductible.

## Sources utilisees

| Source | Contenu | Statut |
| --- | --- | --- |
| `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | Bundle manifest, IDE handoff | MERGE (PR #201) |
| `GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | Initial project doc, response capture, remaining gaps | MERGE (PR #201) |
| `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01` | Plan parent cursor-ai | MERGE (PR #205) |

## Contenu du pack

| Fichier | Role |
| --- | --- |
| `README.md` | Ce fichier — survol et index |
| `PROMPT_TEMPLATES.md` | Templates de prompts operateur (reprise, review, merge, safety, handoff) |
| `REPRISE_TEMPLATE.md` | Template de fiche de reprise standard |
| `NO_COMMIT_RULES.md` | Regles de ce qui ne doit jamais etre committe |
| `CHECKLIST_EXECUTION.md` | Checklist pre-commit, pre-push, pre-PR et post-merge |
| `bundle_meta/manifest.json` | Manifest technique du pack, dependances et invariants |

## Invariants

- Machine cible : cursor-ai uniquement.
- Admin-trading : non ouvert sans demande explicite.
- Runtime : non modifie.
- Secrets / .env / tokens : jamais committes.
- alert_webhook : ACTIVE_CONTINUITY, ne pas marquer comme ferme.
- Bundles produit : APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED, ne pas marquer comme ferme.

## Usage

1. Lire `PROMPT_TEMPLATES.md` pour les prompts standard.
2. Utiliser `REPRISE_TEMPLATE.md` pour creer une fiche de reprise.
3. Verifier `NO_COMMIT_RULES.md` avant tout commit.
4. Executer `CHECKLIST_EXECUTION.md` avant push et PR.
