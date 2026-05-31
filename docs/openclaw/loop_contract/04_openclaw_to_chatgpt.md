---
doc_id: OPENCLAW_LOOP_FORMAT_04
doc_type: loop_contract_format
segment: openclaw_to_chatgpt
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# FORMAT 4 — OpenClaw → ChatGPT : Synthèse + gate humain

## Rôle

OpenClaw agrège le résultat (FORMAT 3) en une synthèse lisible par ChatGPT
(et l'opérateur humain). La synthèse inclut le verdict, un résumé des faits,
la prochaine étape recommandée, et la question de gate humain si applicable.

## Schéma (YAML)

```yaml
synthesis:
  # Obligatoires
  job_id: string              # repris du FORMAT 1
  instruction_id: string      # repris du FORMAT 2
  verdict: enum               # PASS | FAIL | PARTIAL | SKIPPED
  synthesized_at: string      # ISO 8601

  # Résumé (obligatoire)
  what_was_done: string       # 1-3 phrases — ce qui a été exécuté
  key_findings: list[str]     # faits établis par l'exécution (bullet list)
  files_modified: list[str]   # repris du FORMAT 3

  # Erreur (obligatoire si verdict != PASS)
  error_summary: string | null

  # Gate humain (obligatoire si verdict = PASS et write dans allowed_ops)
  gate_required: bool
  gate_question: string | null  # question posée à l'opérateur

  # Next step (optionnel)
  next_step: string | null    # recommandation OpenClaw si PASS
  next_job_spec: object | null  # FORMAT 1 pré-rempli si relance souhaitée

  # Optionnel
  notes: string
```

## Verdicts et comportement gate

| Verdict | gate_required | Comportement |
| --- | --- | --- |
| `PASS` + read-only | false | Pas de gate — ChatGPT peut relancer directement |
| `PASS` + write | true | Gate obligatoire avant tout merge ou push |
| `FAIL` | false | Stoppe — ChatGPT décide de relancer ou d'abandonner |
| `PARTIAL` | true | Gate obligatoire — opérateur doit examiner avant relance |
| `SKIPPED` | false | Signaler — ChatGPT redéfinit le job spec si nécessaire |

## Template (PASS avec write)

```yaml
synthesis:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  verdict: "PASS"
  synthesized_at: "2026-05-30T00:00:00Z"
  what_was_done: "<résumé de l'exécution>"
  key_findings:
    - "<fait 1>"
    - "<fait 2>"
  files_modified:
    - "path/to/file.md"
  error_summary: null
  gate_required: true
  gate_question: "Les modifications ci-dessus sont-elles conformes à l'intent ? APPROVE pour merger, REJECT pour annuler, RESTART pour relancer avec corrections."
  next_step: "<prochaine action recommandée>"
  next_job_spec: null
  notes: ""
```

## Template (FAIL)

```yaml
synthesis:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  verdict: "FAIL"
  synthesized_at: "2026-05-30T00:00:00Z"
  what_was_done: "<ce qui a été tenté>"
  key_findings:
    - "<cause d'échec>"
  files_modified: []
  error_summary: "<message d'erreur>"
  gate_required: false
  gate_question: null
  next_step: null
  next_job_spec: null
  notes: ""
```

## Règles de validation

```
verdict doit correspondre au status du FORMAT 3.
gate_required = true si verdict = PASS + write OU verdict = PARTIAL.
gate_question non null si gate_required = true.
next_job_spec ne peut pas contenir push ou merge dans allowed_ops.
```

## Modes d'échec segment 4

| Erreur | Cause | Résolution |
| --- | --- | --- |
| `VERDICT_MISMATCH` | verdict ≠ FORMAT 3 status | Aligner sur FORMAT 3 |
| `GATE_MISSING` | write PASS sans gate | Ajouter gate_required: true |
| `NO_GATE_QUESTION` | gate_required true sans question | Formuler la gate_question |
