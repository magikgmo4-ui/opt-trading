---
doc_id: BUNDLES_ACTIVE_WORKFLOW_01
doc_type: bundle/active_workflow
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: workflow_active
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - bundles/claude-artifacts/README.md
---

# ACTIVE_WORKFLOW — Bundles cursor-ai

## Definition

Bundles est maintenant un **workflow actif cursor-ai**. Il n'est pas un produit ferme mais une methode continue de packaging, documentation et reprise cote cursor-ai.

## Quand utiliser Bundles

| Situation | Action Bundles |
| --- | --- |
| Nouveau GO doc-only | Creer un bundle de reprise avec templates |
| Pack operateur a standardiser | Utiliser le template Claude artifacts |
| IDE handoff a produire | Generer un bundle de handoff |
| PR a merger | Suivre le flux operateur Bundles |
| Closeout de GO | Produire un closeout bundle |
| Reprise par un autre operateur | Pointer vers le bundle existant |

## Quand NE PAS utiliser Bundles

- Runtime : les bundles cursor-ai ne touchent jamais le runtime.
- Admin-trading : pas de bundle admin-trading sans demande explicite.
- Secrets : aucun bundle ne contient de secret, .env, token, payload reel.

## Relation avec Claude artifacts

Le pack `bundles/claude-artifacts/` est un cas concret de bundle operateur. Il suit la methode Bundles et fournit les templates standard.

## Etat Bundles

| Element | Statut |
| --- | --- |
| Bundles produit | APPLICATION_DOCUMENTED, non ferme |
| Bundles workflow cursor-ai | ACTIF (ce GO) |
| Bundle Claude artifacts | ACTIF, integre |
| Bundle IDE handoff | REFERENCE |
| Bundle student (Ollama) | REFERENCE, machine student |

## Regles

1. Chaque bundle cursor-ai contient au minimum : README, template/prompts, regles no-secret.
2. Aucun runtime dans un bundle cursor-ai.
3. Aucun secret dans un bundle.
4. Les bundles sont versionnes dans `bundles/` ou `docs/chantiers/`.
5. Un bundle n'est jamais supprime sans GO explicite.
