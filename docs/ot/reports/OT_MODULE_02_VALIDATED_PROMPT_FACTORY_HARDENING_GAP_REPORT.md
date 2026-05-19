# OT-MODULE-02 — VALIDATED_PROMPT_FACTORY (HARDENING) — GAP REPORT

Date (America/Montreal) : 2026-03-14

## ÉTABLI
- Le module existe, est déclaré dans les registries, et génère des prompts via Python.
- Le workflow impose la continuité (doc canonique + kanban + point de reprise).

## ÉCARTS PROUVÉS (ET STATUT)

### GAP-01 (CRITIQUE) — Synthèse incomplète acceptée
- **Constat** : la validation de sections manquantes n’était pas bloquante.
- **Risque** : prompts “Non spécifié” en production, continuité affaiblie.
- **Statut** : CORRIGÉ (échec explicite si section manquante).

### GAP-02 (UTILE) — En-têtes Markdown non interprétés
- **Constat** : une synthèse écrite avec `## CONTEXTE` n’était pas reconnue comme header.
- **Statut** : CORRIGÉ (tolérance aux préfixes `#`).

### GAP-03 (UTILE) — Output dir non robuste
- **Constat** : `--output-dir` pouvait pointer vers un fichier existant sans message clair.
- **Statut** : CORRIGÉ (erreur explicite si path non-dir).

## RÉSERVE MINEURE
- Exécution réelle des wrappers bash sur poste Windows : non prouvable ici (WSL absent). À confirmer sur Linux cible.

## HORS PÉRIMÈTRE (NON RETENU)
- Refonte UX (nouveaux modes, API, intégration menu hub).
- Ajout de flags/options d’exécution non nécessaires au durcissement minimal.

