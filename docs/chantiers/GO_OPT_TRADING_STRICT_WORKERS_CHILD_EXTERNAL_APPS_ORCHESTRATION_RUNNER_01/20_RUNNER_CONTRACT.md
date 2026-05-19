# Runner Contract — OpenClaw / OpenCode

## Contrat générique

### Input

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `job_packet_path` | string | oui | Chemin relatif dans le repo vers le job packet JSON |
| `trigger_source` | string | oui | `github_schedule` / `github_manual` / `human` / `openclaw` |
| `requested_app` | string | non | Cible bridge : `airtable` / `clickup` / `botpress` / `telegram` / `sheets` / `none` |
| `mode` | string | oui | `READ_ONLY` / `DRAFT_ONLY` / `WRITE_GATED` |
| `dry_run` | bool | non (défaut: true) | `true` = ne pas écrire dans l'app externe |
| `operator_context` | string | non | Contexte libre (GO id, session id, etc.) |
| `validation_token` | string | non | Jeton de validation externe pour WRITE_GATED |

### Output

| Champ | Type | Description |
|---|---|---|
| `run_id` | string | Identifiant unique du run (UUID) |
| `job_packet_id` | string | Référence au packet exécuté |
| `app_target` | string | App bridge ciblée (ou `none`) |
| `actions_planned` | array | Actions que le worker prévoit d'exécuter |
| `actions_executed` | array | Actions réellement exécutées |
| `files_touched` | array | Fichiers modifiés dans le repo |
| `app_records_touched` | array | Enregistrements modifiés dans l'app externe |
| `verdict` | string | `PASS` / `FAIL` / `BLOCKED` / `DRAFT_ONLY` |
| `report_path` | string | Chemin vers le rapport DRAFT_ONLY généré |
| `errors` | array | Erreurs éventuelles |
| `warnings` | array | Avertissements |
| `timestamp` | string | Date UTC du run |

### Pipeline d'exécution

```
1. VALIDATE → run_task.sh valide le packet (schema + registry)
2. PLAN    → worker liste les actions prévues (read-only)
3. EXECUTE → worker exécute les actions autorisées par le mode
4. REPORT  → worker génère le rapport DRAFT_ONLY
5. VERIFY  → OpenClaw vérifie le verdict
6. CLOSE   → si WRITE_GATED + validation → write réel ; sinon close
```

## Modes d'exécution

| Mode | Description | Write repo | Write app | Validation requise |
|---|---|---|---|---|
| `READ_ONLY` | Lecture seule | non | non | non |
| `DRAFT_ONLY` | Rapport sans write | oui (rapport .md) | non | non |
| `WRITE_GATED` | Write contrôlé | oui (scope limité) | oui (scope limité) | oui (externe) |
