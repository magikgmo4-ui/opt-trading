# GO_LOCAL_LLM_WORKER_STUDENT_TEST_01 — Initial Project Doc

## 1_MASTER_TARGET

Tester sur `student` un worker LLM local capable d'analyser le dépôt en mode read-only, fichier par fichier, puis de produire des sorties structurées vérifiables.

## 3_INITIAL_NEED

Mettre en place un petit modèle local de type Gemma/Gemma-like pour réduire les appels cloud sur les tâches répétitives :

- lecture de fichiers ;
- classification ;
- extraction de TODO/GAP/risques ;
- propositions locales ;
- rapport final.

## 4_MASTER_PROJECT_PLAN

Le chantier vise un pipeline local minimal :

```text
scan docs/
→ lire fichier
→ appeler modèle local
→ produire JSON
→ valider schéma
→ sauvegarder output
→ agréger outputs
→ produire rapport final
```

## 6_FINAL_TARGET

Livrable attendu :

- runtime local validé sur `student` ;
- worker read-only fonctionnel ;
- audit limité initialement à `docs/` ;
- sortie JSON par fichier ;
- rapport agrégé Markdown ;
- aucun commit, push ou patch appliqué automatiquement par le worker.

## GO_STRUCTURAL_ROLE

```text
GO_CHILD_ATTACHED_TO_PARENT
```

## 10_SELECTED_SETUP

Surface principale :

```text
tools/local_llm_worker/
```

Documentation chantier :

```text
docs/chantiers/GO_LOCAL_LLM_WORKER_STUDENT_TEST_01/
```

Index atomique :

```text
docs/index/inbox/GO_LOCAL_LLM_WORKER_STUDENT_TEST_01.md
```

## 12_INVARIANTS

- Worker read-only sur le repo.
- Aucun `git commit` automatique.
- Aucun `git push` automatique.
- Aucun patch appliqué automatiquement.
- Les sorties doivent rester dans `tools/local_llm_worker/outputs/`.
- Le premier test est limité à 5 fichiers.
- Le premier scope complet est limité à `docs/`.
- Toute modification proposée doit rester une proposition.

## 15_REMAINING_GAP

À valider sur `student` :

- runtime disponible : Ollama ou llama.cpp ;
- modèle exact utilisable ;
- performance CPU/GPU ;
- stabilité JSON ;
- taux d'hallucination ;
- qualité des propositions ;
- coût réel en temps local.

## 17_RESUME_POINT

Reprise :

```text
appliquer patch
→ installer runtime local
→ exécuter smoke test
→ lancer audit limité 5 fichiers
→ agréger rapport
→ documenter résultats
```
