---
doc_id: OPENCLAW_LOOP_FORMAT_02
doc_type: loop_contract_format
segment: openclaw_to_ide
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# FORMAT 2 — OpenClaw → IDE/agent : Instruction structurée

## Rôle

OpenClaw traduit le job spec (FORMAT 1) en une instruction exécutable
pour l'IDE ou l'agent. L'instruction est plus précise et technique que
le job spec — elle inclut les commandes, le périmètre fichiers exact,
et les opérations autorisées.

## Schéma (YAML)

```yaml
instruction:
  # Obligatoires
  job_id: string           # repris du FORMAT 1
  instruction_id: string   # ex: INSTR_20260530_001_A
  agent_target: string     # ex: claude-code, cursor, bash-runner
  command: string          # commande principale ou prompt agent
  file_scope: list[str]    # fichiers/globs exacts autorisés en écriture
  read_scope: list[str]    # fichiers/globs autorisés en lecture seule
  allowed_ops: list[str]   # sous-ensemble du FORMAT 1 (jamais plus large)

  # Retour attendu
  return_format: "FORMAT_3"  # toujours FORMAT_3
  return_fields:             # champs minimum attendus dans le résultat
    - status
    - files_modified
    - summary

  # Optionnels
  env_vars: dict[str,str]  # variables d'env à injecter si nécessaire
  timeout_min: int
  notes: string
```

## Template

```yaml
instruction:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  agent_target: "claude-code"
  command: |
    <prompt ou commande exacte à exécuter>
  file_scope: []
  read_scope: ["**/*"]
  allowed_ops: ["read"]
  return_format: "FORMAT_3"
  return_fields:
    - status
    - files_modified
    - summary
  env_vars: {}
  timeout_min: 30
  notes: ""
```

## Règles de validation

```
allowed_ops dans FORMAT 2 ⊆ allowed_ops dans FORMAT 1 (jamais plus large).
file_scope vide + allowed_ops contenant write → ERREUR : périmètre écriture non défini.
agent_target doit être un agent connu (claude-code, cursor, bash-runner, python-runner).
return_format doit toujours être "FORMAT_3".
```

## Modes d'échec segment 2

| Erreur | Cause | Résolution |
| --- | --- | --- |
| `SCOPE_EXPANSION` | allowed_ops > FORMAT 1 | Restreindre au FORMAT 1 |
| `WRITE_NO_SCOPE` | write sans file_scope | Définir file_scope explicitement |
| `UNKNOWN_AGENT` | agent_target inconnu | Utiliser un agent de la liste |
| `MISSING_RETURN_FORMAT` | return_format absent | Ajouter FORMAT_3 |
