# CURSOR_AI_BUNDLES_REPRISE — Operateur cursor-ai

## Point de reprise Bundles

Cette fiche est le point d'entree operateur pour les bundles cote cursor-ai.

## Bundles cursor-ai actifs

| Bundle | Statut | Action |
|---|---|---|
| `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | ACTIVE | Bundle IDE live artifacts — appliquer le handoff |

## Methode de creation d'un bundle cursor-ai

1. Creer `bundles/<BUNDLE_NAME>/` ou `docs/chantiers/<BUNDLE_NAME>/`
2. `README_BUNDLE.md` : objectif, invariants, machine owner
3. `bundle_meta/manifest.json` : schema, type, version
4. `checklists/CHECKLIST_EXECUTION.md` : steps
5. `prompts/GO_PROMPT_*.md` : prompts IDE
6. Commiter sans secret, .env, output live

## Methode de recuperation

1. Consulter `bundles/README.md` pour l'index
2. Lire le `README_BUNDLE.md` du bundle
3. Suivre `CHECKLIST_EXECUTION.md`
4. Utiliser les `prompts/` dans l'IDE

## Conventions cursor-ai

- Machine owner = cursor-ai (sauf exception documentee)
- Tous les bundles cursor-ai passent par `bundles/` ou `docs/chantiers/`
- Aucun runtime admin-trading dans un bundle cursor-ai
- Aucun secret
