# Implementation Plan — GO_LOCAL_LLM_WORKER_STUDENT_TEST_01

## Kanban

| Colonne | Étape | Objectif | Livrable | Statut |
|---|---|---|---|---|
| BACKLOG | Cadrage chantier | Définir cible, limites, garde-fous | `00_INITIAL_PROJECT_DOC.md` | À faire |
| BACKLOG | Structure repo | Créer dossiers worker + docs chantier | `tools/local_llm_worker/` | À faire |
| À FAIRE | Installation student | Installer Ollama ou llama.cpp | runtime local fonctionnel | À faire |
| À FAIRE | Modèle local | Tester Gemma/Gemma-like | smoke test OK | À faire |
| À FAIRE | Prompt canonique | Grille d'analyse fichier | `file_audit_prompt.md` | À faire |
| À FAIRE | Schéma sortie | Forcer JSON stable | `file_audit.schema.json` | À faire |
| EN COURS | Worker lecture | Scanner `docs/`, lire fichiers | `audit_files.py` | À faire |
| EN COURS | Sorties par fichier | Générer une fiche par fichier | `outputs/file_analysis/*.json` | À faire |
| EN COURS | Agrégateur | Regrouper gaps/TODO/risques | `aggregate_reports.py` | À faire |
| TEST | Test 5 fichiers | Vérifier qualité/silence/stabilité | rapport court | À faire |
| TEST | Test `docs/` complet | Laisser tourner sans suivi manuel | rapport global | À faire |
| REVIEW | Revue humaine | Évaluer hallucinations/propositions | `40_RESULTS_AND_GAPS.md` | À faire |
| DONE | Décision suite | Étendre ou stopper | prochain GO ou close gate | À faire |

## Phases

### Phase 1 — Structure

- Créer l'arborescence `tools/local_llm_worker/`.
- Créer les prompts, schémas et scripts.
- Créer la documentation du chantier.
- Créer l'inbox atomique.

### Phase 2 — Runtime local

- Installer ou valider Ollama/lama.cpp.
- Télécharger un modèle local compatible.
- Lancer le smoke test.

### Phase 3 — Audit limité

- Scanner un petit lot de 5 fichiers `docs/`.
- Produire un JSON par fichier.
- Valider la conformité du JSON.
- Corriger prompt/script si la sortie est instable.

### Phase 4 — Agrégation

- Lire les fiches JSON.
- Regrouper les gaps, risques, TODO et propositions.
- Générer un rapport Markdown.

### Phase 5 — Revue

- Vérifier hallucinations.
- Vérifier utilité des propositions.
- Documenter les gaps.
- Décider extension vers `src/`, `tests/` ou arrêt.

## Critères de réussite

- Le worker ne modifie aucun fichier source.
- Les sorties JSON sont valides.
- Le rapport agrégé est lisible.
- Les propositions sont séparées des faits établis.
- Le worker peut tourner sans supervision sur un scope borné.

## Critères d'arrêt

- JSON instable malgré correction prompt.
- Hallucinations fréquentes.
- Sorties non exploitables.
- Temps d'analyse disproportionné.
- Incapacité à respecter le mode read-only.

## RISKS

- À qualifier.
