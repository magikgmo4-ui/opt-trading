---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_30_ARTIFACTS_INDEX
doc_type: chantier/artifacts_index
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
---

# 30_ARTIFACTS_INDEX

## Artefacts bundle actifs

| Artefact | Role operateur |
| --- | --- |
| `bundles/claude-artifacts/README.md` | Point d'entree du pack |
| `bundles/claude-artifacts/PROMPT_TEMPLATES.md` | 5 templates de prompts |
| `bundles/claude-artifacts/REPRISE_TEMPLATE.md` | Template de fiche de reprise |
| `bundles/claude-artifacts/NO_COMMIT_RULES.md` | Regles no-secret / no-sensitive |
| `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` | Checklist avant commit, push, PR, post-merge |
| `bundles/claude-artifacts/bundle_meta/manifest.json` | Manifest technique et invariants |

## Sources documentaires deja mergees

| Source | Apport reutilise |
| --- | --- |
| `docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/` | Handoff IDE et invariants Claude |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/` | Philosophie live artifacts / cowork |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/` | Sequence et priorite `cursor-ai` |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01/` | Definition de Bundles comme workflow actif |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01/` | Validation reelle du pack |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/` | Packet de reprise operateur |

## Traces legacy conservees dans ce GO

| Fichier legacy | Statut apres regularisation |
| --- | --- |
| `00_START.md` | Conserve comme point d'entree historique |
| `10_SOURCE_BUNDLES_INVENTORY.md` | Conserve comme inventaire initial |
| `20_OPERATOR_USAGE.md` | Conserve comme guide initial |
| `30_PROMPT_TEMPLATES.md` | Conserve comme reference initiale |
| `40_BUNDLE_INTEGRATION.md` | Conserve comme integration initiale |
| `50_NO_COMMIT_RULES.md` | Conserve comme trace initiale des interdictions |

## Mapping legacy -> structure canonique

| Besoin canonique | Source principale |
| --- | --- |
| Ouverture du GO | `00_GO_OPEN.md` |
| Etat source | `10_SOURCE_STATE.md` + `10_SOURCE_BUNDLES_INVENTORY.md` |
| Spec operateur | `20_OPERATOR_PACK_SPEC.md` |
| Index des artefacts | `30_ARTIFACTS_INDEX.md` |
| Workflow d'usage | `40_USAGE_WORKFLOW.md` + `20_OPERATOR_USAGE.md` |
| Closeout | `90_CLOSEOUT.md` |
