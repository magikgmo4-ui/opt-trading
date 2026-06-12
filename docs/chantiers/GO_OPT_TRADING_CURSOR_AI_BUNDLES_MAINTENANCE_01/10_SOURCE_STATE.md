---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/README.md
---

# 10_SOURCE_STATE

## Pack Claude artifacts avant maintenance

| Fichier | Present | Role |
| --- | --- | --- |
| `README.md` | OUI | Survol et index |
| `PROMPT_TEMPLATES.md` | OUI | 5 templates de prompts |
| `REPRISE_TEMPLATE.md` | OUI | Template de fiche de reprise |
| `NO_COMMIT_RULES.md` | OUI | Regles de securite |
| `CHECKLIST_EXECUTION.md` | NON | A creer |
| `bundle_meta/manifest.json` | NON | A creer |

## Conventions Bundles

`bundles/README.md` specifie :
- Un bundle contient au minimum : `README_BUNDLE.md`, `bundle_meta/manifest.json`

Le pack Claude artifacts n'a pas encore de `manifest.json`.

## bundles/README.md avant maintenance

Reference 2 bundles (student Ollama + IDE bundle). Ne reference pas :
- `claude-artifacts/`
- `CURSOR_AI_OPERATOR_REPRISE_PACKET.md`
- `ACTIVE_WORKFLOW.md`, `BUNDLE_TYPES.md`, `OPERATOR_FLOW.md`, `NO_RUNTIME_NO_SENSITIVE_RULES.md`

## Objectif

Completer le pack et mettre a jour l'index pour refleter l'etat reel.

## RISKS

- À qualifier.
