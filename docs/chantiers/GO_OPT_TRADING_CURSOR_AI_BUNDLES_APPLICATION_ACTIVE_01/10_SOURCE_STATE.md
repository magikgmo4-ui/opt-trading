---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - bundles/claude-artifacts/README.md
---

# 10_SOURCE_STATE — Etat des sources avant activation

## PR mergees

| PR | Contenu | Statut |
| --- | --- | --- |
| #205 | Parent operational plan cursor-ai | MERGE |
| #206 | Claude artifacts operator pack | MERGE |
| #202 | Bundles application operateur | MERGE (application documentee) |
| #201 | Claude cowork / live artifacts / IDE bundle | MERGE |
| #203 | alert_webhook application | MERGE (active) |

## Bundles avant ce GO

| Element | Statut |
| --- | --- |
| `bundles/README.md` | Present — index des bundles |
| `bundles/CURSOR_AI_BUNDLES_REPRISE.md` | Present — reprise operateur |
| `bundles/claude-artifacts/` | Present — pack operateur |
| Bundles workflow | APPLICATION_DOCUMENTED |
| Bundles produit | NON FERME |

## Objectif de ce GO

Passer Bundles de `APPLICATION_DOCUMENTED` a `ACTIF`.

Concretement :
- Ajouter `bundles/ACTIVE_WORKFLOW.md` (definition workflow)
- Ajouter `bundles/BUNDLE_TYPES.md` (types de bundles)
- Ajouter `bundles/OPERATOR_FLOW.md` (flux operateur)
- Ajouter `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md` (limites)
- Documenter le changement dans `docs/chantiers/`

## Admin-trading

- Gate fermee.
- Aucune modification prevue.
- Le bundle admin-trading gate reste FERME / FUTUR.
