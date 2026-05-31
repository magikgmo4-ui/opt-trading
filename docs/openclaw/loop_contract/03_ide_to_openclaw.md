---
doc_id: OPENCLAW_LOOP_FORMAT_03
doc_type: loop_contract_format
segment: ide_to_openclaw
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# FORMAT 3 — IDE/agent → OpenClaw : Résultat structuré

## Rôle

L'IDE ou l'agent retourne à OpenClaw un résultat structuré après exécution
de l'instruction (FORMAT 2). Ce résultat est la seule source de vérité
qu'OpenClaw utilise pour construire la synthèse (FORMAT 4).

## Schéma (YAML)

```yaml
result:
  # Obligatoires
  job_id: string              # repris du FORMAT 1
  instruction_id: string      # repris du FORMAT 2
  status: enum                # PASS | FAIL | PARTIAL | SKIPPED
  agent_target: string        # agent qui a exécuté
  executed_at: string         # ISO 8601

  # Obligatoires si status != SKIPPED
  summary: string             # résumé 1-3 phrases de ce qui a été fait
  files_modified: list[str]   # [] si read-only, sinon liste exacte
  files_read: list[str]       # fichiers consultés

  # Erreur (obligatoire si status = FAIL ou PARTIAL)
  error: string | null        # message d'erreur ou null

  # Optionnels
  diff_summary: string        # résumé du diff si write
  artifacts: list[str]        # chemins d'artefacts produits
  evidence: list[str]         # chemins de fichiers de preuve
  notes: string
```

## Statuts

| Statut | Signification |
| --- | --- |
| `PASS` | Exécution complète, résultat conforme au FORMAT 2 |
| `FAIL` | Exécution échouée — stoppe la boucle |
| `PARTIAL` | Exécution partielle — stoppe la boucle, nécessite gate humain |
| `SKIPPED` | Instruction non exécutée (scope vide, condition non remplie) |

## Template

```yaml
result:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  status: "PASS"
  agent_target: "claude-code"
  executed_at: "2026-05-30T00:00:00Z"
  summary: "<résumé de ce qui a été fait>"
  files_modified: []
  files_read: []
  error: null
  diff_summary: ""
  artifacts: []
  evidence: []
  notes: ""
```

## Règles de validation

```
status doit être l'un des 4 valeurs définies.
FAIL ou PARTIAL exige un champ error non null.
files_modified non vide implique que write était dans allowed_ops (FORMAT 2).
executed_at doit être ISO 8601 — pas de date relative.
```

## Modes d'échec segment 3

| Erreur | Cause | Résolution |
| --- | --- | --- |
| `MISSING_STATUS` | status absent | Ajouter status explicite |
| `FAIL_NO_ERROR` | FAIL sans error | Fournir le message d'erreur |
| `UNAUTHORIZED_WRITE` | files_modified sans write dans scope | Signaler la violation de scope |
| `INVALID_DATE` | executed_at non ISO 8601 | Corriger le format |

## Règle de propagation

```
FAIL  → OpenClaw stoppe la boucle, construit FORMAT 4 avec verdict FAIL
PARTIAL → OpenClaw stoppe la boucle, construit FORMAT 4 avec verdict PARTIAL + gate obligatoire
PASS  → OpenClaw construit FORMAT 4, peut proposer relance si next step défini
```
