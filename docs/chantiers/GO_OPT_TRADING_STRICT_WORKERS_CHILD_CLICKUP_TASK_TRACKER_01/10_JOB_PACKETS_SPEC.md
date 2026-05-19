---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01_JOB_PACKETS_SPEC
doc_type: job_packets_spec
repo: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
status: draft
---

# 10_JOB_PACKETS_SPEC — ClickUp Task Tracker Worker

## Job Packet 1: READ_INVENTORY — ClickUp

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_CLICKUP_READ_INVENTORY_01` |
| `task_type` | `READ_INVENTORY` |
| `autonomy_max` | A1 |
| `surface` | `clickup` |
| `modele_prefere` | `qwen3.5-plus` (VERIFIED, A1, READ_INVENTORY) |
| `dry_run` | true |
| `requires_explicit_write_approval` | false |

**inputs autorises :**
```json
{
  "list_id": "GO_ACTIVE",
  "max_tasks": 50,
  "filtre_status": ""
}
```

**denied_commands :** `write`, `delete`, `update`, `clickup:post`, `clickup:put`
**denied_inputs :** `CLICKUP_TOKEN`, `/tmp/clickup_token`, `.env`

**output :** `reports/ai/workers/clickup_inventory_<timestamp>.md`
**required_sections :** `TACHES_CLICKUP`, `STATUTS`, `VERDICT_INVENTORY`

**validation :** Verifier que le rapport liste les taches sans les modifier
**stop_conditions :** Si l'API ClickUp retourne une erreur → documenter et arreter

---

## Job Packet 2: PATCH_DRAFT — ClickUp

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_CLICKUP_PATCH_DRAFT_01` |
| `task_type` | `PATCH_DRAFT` |
| `autonomy_max` | A2 |
| `surface` | `clickup` |
| `modele_prefere` | `glm-5.1` (VERIFIED, A2, PATCH_DRAFT) |
| `dry_run` | true |
| `requires_explicit_write_approval` | false |

**inputs autorises :**
```json
{
  "task_id": "string",
  "champ": "status|custom_field|description",
  "nouvelle_valeur": "string",
  "justification": "string (max 500 chars)"
}
```

**denied_commands :** `clickup:write`, `clickup:delete`, `clickup:put`
**denied_inputs :** `CLICKUP_TOKEN`, `scripts/ai/workers/tasks.index.json`

**output :** `reports/ai/workers/clickup_patch_draft_<timestamp>.md`
**required_sections :** `TACHE_CIBLE`, `PATCH_PROPOSE`, `DIFF_ATTENDU`, `VALIDATION_EXTERNE`

**validation :** Patch propose mais NON applique. Validation externe obligatoire avant tout merge.
**stop_conditions :** Si le patch modifie le registry local → REFUSE
