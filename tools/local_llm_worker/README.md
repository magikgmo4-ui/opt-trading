# Local LLM Worker

Worker expérimental read-only pour analyser des fichiers du dépôt avec un modèle local.

## Objectif

```text
scan docs/
→ lire fichier
→ appeler modèle local
→ produire JSON structuré
→ sauvegarder output
→ agréger rapport Markdown
```

## Invariants

- Ne modifie pas les fichiers analysés.
- N'applique aucun patch.
- Ne commit pas.
- Ne push pas.
- Écrit seulement dans `tools/local_llm_worker/outputs/`.

## Structure

```text
tools/local_llm_worker/
  config.yaml
  prompts/
  schemas/
  scripts/
  outputs/
```

## Smoke test

```bash
python tools/local_llm_worker/scripts/model_smoke_test.py --model <model>
```

## Audit limité

```bash
python tools/local_llm_worker/scripts/audit_files.py \
  --config tools/local_llm_worker/config.yaml \
  --model <model> \
  --root docs \
  --max-files 5
```

## Agrégation

```bash
python tools/local_llm_worker/scripts/aggregate_reports.py \
  --input tools/local_llm_worker/outputs/file_analysis \
  --output tools/local_llm_worker/outputs/reports/student_docs_audit_report.md
```

## Sortie JSON attendue

```json
{
  "file": "",
  "file_type": "",
  "purpose": "",
  "established": [],
  "hypothesis": [],
  "remaining_gap": [],
  "todo": [],
  "risk": [],
  "duplicate_candidate": [],
  "patch_proposal": "",
  "confidence": 0
}
```
