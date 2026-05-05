---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_20_ACTIVE_WORKFLOW
doc_type: chantier/active_workflow
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/ACTIVE_WORKFLOW.md
---

# 20_ACTIVE_WORKFLOW — Bundles comme workflow actif cursor-ai

## Definition

Bundles est maintenant un **workflow actif cursor-ai**.

Avant ce GO : `APPLICATION_DOCUMENTED` — la methode Bundles etait documentee mais non activee comme workflow.

Apres ce GO : `ACTIF` — Bundles est le workflow standard de packaging, documentation et reprise cote cursor-ai.

## Quand utiliser Bundles

| Situation | Action Bundles |
| --- | --- |
| Nouveau GO doc-only | Creer un bundle de reprise avec templates |
| Pack operateur a standardiser | Utiliser le template Claude artifacts |
| IDE handoff a produire | Generer un bundle de handoff |
| PR a merger | Suivre le flux operateur Bundles |
| Closeout de GO | Produire un closeout bundle |
| Reprise par un autre operateur | Pointer vers le bundle existant |

## Relation avec Claude artifacts

Le pack `bundles/claude-artifacts/` est une **instance concrete** de bundle operateur cree via le workflow Bundles.

Ce pack fournit :
- Les templates de prompts standard (reprise, review, merge, safety, handoff).
- Le template de reprise standard.
- Les regles no-commit.

Tout futur operateur cursor-ai pourra :
1. Consulter `bundles/ACTIVE_WORKFLOW.md` pour comprendre le role Bundles.
2. Consulter `bundles/BUNDLE_TYPES.md` pour choisir le type de bundle.
3. Suivre `bundles/OPERATOR_FLOW.md` pour le flux de creation.
4. Utiliser `bundles/claude-artifacts/PROMPT_TEMPLATES.md` pour les prompts.
5. Verifier `bundles/NO_RUNTIME_NO_SECRET_RULES.md` avant commit.

## Sorties sures

Chaque bundle cree via ce workflow garantit :
- Doc-only (pas de runtime).
- Pas de secrets.
- Pas d'admin-trading sans demande explicite.
- Pas de fermeture produit intempestive.
