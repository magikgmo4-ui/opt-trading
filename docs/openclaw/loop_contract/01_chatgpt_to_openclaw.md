---
doc_id: OPENCLAW_LOOP_FORMAT_01
doc_type: loop_contract_format
segment: chatgpt_to_openclaw
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# FORMAT 1 — ChatGPT → OpenClaw : Job Spec

## Rôle

ChatGPT formule l'intention opérateur en un job spec structuré qu'OpenClaw
peut interpréter sans ambiguïté pour déclencher un job.

## Schéma (YAML)

```yaml
job_spec:
  # Obligatoires
  job_id: string          # identifiant unique ex: JOB_20260530_001
  intent: string          # description courte de l'objectif (1 phrase)
  scope:
    repo: string          # ex: opt-trading
    files: list[string]   # fichiers ou globs autorisés ([] = read-only global)
    branch: string        # branche cible
  allowed_ops: list[str]  # ex: [read, write, commit] — jamais push sans gate
  output_expected: string # ce que ChatGPT attend en retour (FORMAT 4)

  # Optionnels
  constraints: list[str]  # règles supplémentaires ex: ["no runtime change"]
  timeout_min: int         # délai max avant FAIL automatique (défaut: 30)
  context: string          # contexte additionnel pour OpenClaw
  go_id: string            # GO parent si applicable
```

## Template

```yaml
job_spec:
  job_id: "JOB_YYYYMMDD_NNN"
  intent: "<une phrase — ce que le job doit accomplir>"
  scope:
    repo: "opt-trading"
    files: []
    branch: "sot/mainline"
  allowed_ops: ["read"]
  output_expected: "synthèse FORMAT 4 avec verdict PASS/FAIL et next step"
  constraints:
    - "no runtime change"
    - "PR gated — no direct push"
  timeout_min: 30
  context: ""
  go_id: ""
```

## Champs obligatoires

```
job_id, intent, scope.repo, scope.branch, allowed_ops, output_expected
```

## Règles de validation

```
allowed_ops ne peut pas contenir "push" sans que "commit" soit aussi présent.
allowed_ops ne peut pas contenir "merge" — le merge est toujours un gate humain (FORMAT 5).
scope.files = [] signifie read-only global — autorisé uniquement si allowed_ops = [read].
intent doit tenir en une phrase — pas de bullet list.
```

## Modes d'échec segment 1

| Erreur | Cause | Résolution |
| --- | --- | --- |
| `INVALID_JOB_ID` | Format job_id non respecté | Reformuler JOB_YYYYMMDD_NNN |
| `MISSING_FIELD` | Champ obligatoire absent | Compléter le template |
| `FORBIDDEN_OP` | push ou merge dans allowed_ops | Retirer l'opération interdite |
| `INTENT_TOO_LONG` | intent > 1 phrase | Condensar en une phrase |
