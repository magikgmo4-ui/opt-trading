---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01_JOB_PACKETS_SPEC
doc_type: job_packets_spec
repo: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
status: draft
---

# 10_JOB_PACKETS_SPEC — Airtable Integration Worker

## Job Packet 1: READ_INVENTORY — Airtable

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_AIRTABLE_READ_INVENTORY_01` |
| `task_type` | `READ_INVENTORY` |
| `autonomy_max` | A1 |
| `surface` | `airtable` |
| `dependance` | `modules/airtable_bridge/` |
| `modele_prefere` | `qwen3.5-plus` (VERIFIED, A1, READ_INVENTORY) |
| `dry_run` | true |
| `requires_explicit_write_approval` | false |

**inputs autorisés :**
```json
{
  "table": "GO_Status",
  "filter": "",
  "max_records": 100
}
```

**denied_commands :** `write`, `delete`, `update`, `patch`, `airtable:post`
**denied_inputs :** `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `.env`

**output :** `reports/ai/workers/airtable_inventory_<timestamp>.md`
**required_sections :** `ETAT_AIRTABLE`, `MODELE_SYNC`, `VERDICT_INVENTORY`

**validation :** Vérifier que le rapport contient les données Airtable sans les modifier
**stop_conditions :** Si le bridge retourne une erreur → documenter et arreter

---

## Job Packet 2: PATCH_DRAFT — Airtable

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_AIRTABLE_PATCH_DRAFT_01` |
| `task_type` | `PATCH_DRAFT` |
| `autonomy_max` | A2 |
| `surface` | `airtable` |
| `dependance` | `modules/airtable_bridge/` |
| `modele_prefere` | `glm-5.1` (VERIFIED, A2, PATCH_DRAFT) |
| `dry_run` | true |
| `requires_explicit_write_approval` | false |

**inputs autorisés :**
```json
{
  "modele_id": "string",
  "nouveau_statut": "VERIFIED|VERIFIED_FREE|ABSENT_CURRENT_ENDPOINT",
  "justification": "string (max 500 chars)"
}
```

**denied_commands :** `write`, `delete`, `patch:apply`
**denied_inputs :** `AIRTABLE_API_KEY`, `scripts/ai/workers/models.registry.json`

**output :** `reports/ai/workers/airtable_patch_draft_<timestamp>.md`
**required_sections :** `MODELE_CIBLE`, `PATCH_PROPOSE`, `DIFF_ATTENDU`, `VALIDATION_EXTERNE`

**validation :** Patch proposé mais NON appliqué. Validation externe obligatoire avant tout merge.
**stop_conditions :** Si le patch modifie le registry local → REFUSE

---

## Job Packet 3: WRITE_GATED — Airtable

| Champ | Valeur |
| --- | --- |
| `job_packet_id` | `GO_STRICT_WORKERS_AIRTABLE_WRITE_GATED_01` |
| `task_type` | `WRITE_GATED` |
| `autonomy_max` | A4 |
| `surface` | `airtable` |
| `dependance` | `modules/airtable_bridge/` |
| `modele_prefere` | `glm-5.1` / `qwen3.6-plus` (VERIFIED, A4) |
| `dry_run` | true |
| `requires_explicit_write_approval` | true |

**inputs autorisés :**
```json
{
  "go_id": "string",
  "status": "PASS|BLOCKED|IN_PROGRESS|CLOSED",
  "next_go": "string",
  "machine": "fantome",
  "updated_at": "ISO8601 timestamp"
}
```

**denied_commands :** `delete`, `bulk:write`, `airtable:delete`
**denied_inputs :** `AIRTABLE_API_KEY`, `scripts/ai/workers/tasks.index.json`, `scripts/ai/workers/models.registry.json`

**write_allowlist :** `modules/airtable_bridge/app/client.py` (lecture seule, via bridge)
**forbidden_targets :** `modules/airtable_bridge/.env`, `modules/airtable_bridge/scripts/*`

**output :** `reports/ai/workers/airtable_write_gated_<timestamp>.md`
**required_sections :** `APPROBATION_EXPLICITE`, `DRY_RUN`, `WRITE_EFFECTIF`, `VERDICT_WRITE`

**validation :** Dry-run obligatoire avant write. Rollback possible si écriture erronée.
**stop_conditions :** Si approbation explicite absente → REFUSE
