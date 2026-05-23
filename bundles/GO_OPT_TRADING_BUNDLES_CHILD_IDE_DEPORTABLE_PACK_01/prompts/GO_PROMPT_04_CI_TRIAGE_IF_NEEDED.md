# GO_PROMPT_04_CI_TRIAGE_IF_NEEDED

## OBJECTIF

Si une PR est ouverte et que la CI échoue, produire un triage minimal sans patch runtime.

## FORMAT DE TRIAGE

```text
CI_FAILURE_TRIAGE

PR:
JOB_FAILED:
STEP_FAILED:
ERROR_EXCERPT:
LIKELY_CAUSE:
DOC_ONLY_RELEVANCE:
FIX_CANDIDATE:
REQUIRES_IDE_PATCH: yes/no
REQUIRES_RUNTIME_CHANGE: no unless proven
STOP_IF:
```

## RÈGLES

- Ne pas corriger runtime dans ce GO.
- Ne pas modifier le scope.
- Si l'échec vient d'une règle globale indépendante, déclarer `BLOCKED_EXTERNAL_TO_SCOPE`.
- Si l'échec vient du patch doc-only, corriger uniquement les fichiers du bundle, de gouvernance méthode ou des scripts session_transport.
