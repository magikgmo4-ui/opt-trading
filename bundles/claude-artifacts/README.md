---
doc_id: BUNDLE_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
doc_type: bundle/operator_pack
repo: opt-trading
machine: cursor-ai
status: product_closed
lifecycle_stage: product_closed
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01/
---

# Claude Artifacts Operator Pack

## Statut produit

`PRODUCT_CLOSED` pour l'usage operateur `cursor-ai`.

Le closeout produit est borne au pack `bundles/claude-artifacts/`. Il ne ferme pas `alert_webhook`, ne ferme pas le workflow Bundles global, et n'ouvre aucune surface `admin-trading`.

## Objectif

Ce pack transforme les artefacts Claude / IDE Bundle / Claude cowork live artifacts deja integres dans le repo en pack operateur cursor-ai stable et reproductible.

## Sources utilisees

| Source | Contenu | Statut |
| --- | --- | --- |
| `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | Bundle manifest, IDE handoff | MERGE (PR #201) |
| `GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | Initial project doc, response capture, remaining gaps | MERGE (PR #201) |
| `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01` | Plan parent cursor-ai | MERGE (PR #205) |
| `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01` | Fermeture produit du pack | PRODUCT_CLOSED |

## Contenu du pack

| Fichier | Role |
| --- | --- |
| `README.md` | Ce fichier — survol, index et statut produit |
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
- alert_webhook : ACTIVE_CONTINUITY, ne pas marquer comme ferme depuis ce pack.
- Bundles global : ne pas marquer comme ferme depuis ce pack.
- Claude Artifacts Operator Pack : PRODUCT_CLOSED.

## Usage

1. Lire `PROMPT_TEMPLATES.md` pour les prompts standard.
2. Utiliser `REPRISE_TEMPLATE.md` pour creer une fiche de reprise.
3. Verifier `NO_COMMIT_RULES.md` avant tout commit.
4. Executer `CHECKLIST_EXECUTION.md` avant push et PR.
5. Consulter `bundle_meta/manifest.json` pour l'identifiant, la version et les invariants.
