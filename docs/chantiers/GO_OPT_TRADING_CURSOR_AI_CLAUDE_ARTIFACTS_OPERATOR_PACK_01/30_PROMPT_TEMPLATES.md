---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_30_PROMPT_TEMPLATES
doc_type: chantier/prompt_templates
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
---

# 30_PROMPT_TEMPLATES

Reference des templates de prompts standard pour operateur cursor-ai.

Les templates complets sont dans `bundles/claude-artifacts/PROMPT_TEMPLATES.md`.

## Liste des templates

| Template | Usage | Quand l'utiliser |
| --- | --- | --- |
| Template 1 — Reprise | Prompt de reprise standardise | Demarrage d'un nouveau GO ou reprise d'un GO existant |
| Template 2 — Review | Prompt de review avant merge | Verification d'un GO cree avant ouverture de PR |
| Template 3 — Merge doc-only | Prompt de merge dans sot/mainline | Merge d'un GO doc-only via PR |
| Template 4 — Safety check | Prompt de verification no-runtime | Verification qu'un GO ne contient pas de runtime |
| Template 5 — Handoff IDE | Prompt de handoff pour operateur | Fin d'un GO, transmission a l'operateur suivant |

## Philosophie des prompts

Issue de `01_FULL_RESPONSE_CAPTURE.md` (Claude cowork parent) :

```text
Repo / docs / commits / closeouts = verite canonique
Live Artifact Claude = vue dynamique de pilotage
Claude Cowork = operateur / assistant d'execution
```

Les prompts de ce pack sont concus pour :
- Standardiser le format des GO.
- Reduire les erreurs de procedure.
- Assurer la conformite aux invariants (no runtime, no admin-trading, no secrets).
- Permettre la reprise par un autre operateur.

## Scoring d'attention (P0/P1/P2)

| Niveau | Definition | Exemple |
| --- | --- | --- |
| P0 | Action bloquante ou risque de divergence canonique | PR ouverte qui bloque merge, branche dediee sans indexation |
| P1 | Verification requise avant travail suivant | GO actif sans `SESSION_REPRISE.txt` |
| P2 | Surveillance non bloquante | Doc recent modifie, branch stale reference |

## Mode read-only strict

Extrait de `02_REMAINING_GAP.md` :

```text
MODE READ-ONLY STRICT
Tu peux lire et synthetiser.
Tu ne modifies aucun fichier, aucune branche, aucune PR, aucun document Drive, aucun calendrier, aucune tache.
Toute action d'ecriture doit etre proposee comme TODO et attendre un GO explicite.
```
