# Test Protocol — GO_LOCAL_LLM_WORKER_STUDENT_TEST_01

## 1. Préconditions

```bash
git status -sb
ollama list
python tools/local_llm_worker/scripts/model_smoke_test.py --model <model>
```

Le repo doit être dans un état contrôlé avant exécution.

## 2. Test limité 5 fichiers

Commande :

```bash
python tools/local_llm_worker/scripts/audit_files.py \
  --config tools/local_llm_worker/config.yaml \
  --model <model> \
  --root docs \
  --max-files 5
```

Résultat attendu :

```text
tools/local_llm_worker/outputs/file_analysis/*.json
```

## 3. Agrégation

Commande :

```bash
python tools/local_llm_worker/scripts/aggregate_reports.py \
  --input tools/local_llm_worker/outputs/file_analysis \
  --output tools/local_llm_worker/outputs/reports/student_docs_audit_report.md
```

Résultat attendu :

```text
tools/local_llm_worker/outputs/reports/student_docs_audit_report.md
```

## 4. Contrôles qualité

Vérifier :

- JSON valide ;
- pas d'invention manifeste ;
- distinction entre `established` et `hypothesis` ;
- TODO courts et actionnables ;
- propositions locales ;
- pas de modification du repo hors outputs.

## 5. Test docs complet

À exécuter seulement après validation du test 5 fichiers :

```bash
python tools/local_llm_worker/scripts/audit_files.py \
  --config tools/local_llm_worker/config.yaml \
  --model <model> \
  --root docs
```

## 6. Close gate local

Le GO peut passer en revue si :

- smoke test OK ;
- audit 5 fichiers OK ;
- rapport agrégé produit ;
- limites documentées ;
- aucune modification automatique ;
- prochaine extension clairement définie ou chantier stoppé.
