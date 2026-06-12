# Results And Gaps — GO_LOCAL_LLM_WORKER_STUDENT_TEST_01

## 13_ESTABLISHED

- Chantier ouvert pour tester un worker LLM local read-only sur `student`.
- Scope initial : `docs/`.
- Sorties attendues : JSON par fichier + rapport agrégé.

## 14_HYPOTHESIS

- Un petit modèle local peut couvrir les tâches répétitives de lecture, tri, extraction et proposition.
- Le modèle doit rester borné à des analyses locales pour éviter les hallucinations globales.

## 15_REMAINING_GAP

- Runtime local non encore validé.
- Modèle exact non encore confirmé.
- Qualité JSON non encore mesurée.
- Taux d'hallucination non encore mesuré.
- Performance sur `student` non encore mesurée.

## 16_TODO

1. Appliquer le patch du chantier.
2. Installer ou valider Ollama.
3. Sélectionner un modèle local.
4. Exécuter `model_smoke_test.py`.
5. Exécuter l'audit limité à 5 fichiers.
6. Agréger le rapport.
7. Reporter résultats et gaps dans ce fichier.

## 17_RESUME_POINT

Reprendre ici après application du patch :

```text
runtime local
→ smoke test
→ audit 5 fichiers
→ rapport
→ revue résultats/gaps
```

## RISKS

- À qualifier.
