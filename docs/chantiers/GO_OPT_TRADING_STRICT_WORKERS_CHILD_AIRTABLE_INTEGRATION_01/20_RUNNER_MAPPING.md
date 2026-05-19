---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01_RUNNER_MAPPING
doc_type: runner_mapping
repo: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
status: draft
---

# 20_RUNNER_MAPPING — Airtable Integration Worker

## Mapping tache -> worker -> runner

| Tache | Job Packet | Modele | Runner | Output |
| --- | --- | --- | --- | --- |
| READ_INVENTORY Airtable | `GO_STRICT_WORKERS_AIRTABLE_READ_INVENTORY_01` | qwen3.5-plus | `run_task.sh` + `airtable_bridge` | `reports/ai/workers/airtable_inventory_<ts>.md` |
| PATCH_DRAFT Airtable | `GO_STRICT_WORKERS_AIRTABLE_PATCH_DRAFT_01` | glm-5.1 | `run_task.sh` + `airtable_bridge` | `reports/ai/workers/airtable_patch_draft_<ts>.md` |
| WRITE_GATED Airtable | `GO_STRICT_WORKERS_AIRTABLE_WRITE_GATED_01` | glm-5.1 / qwen3.6-plus | `run_task.sh` + `airtable_bridge` | `reports/ai/workers/airtable_write_gated_<ts>.md` |

## Invocation

```bash
# READ_INVENTORY — lecture seule
bash scripts/ai/workers/run_task.sh \
  --job-packet docs/chantiers/.../<packet>.json \
  --dry-run

# PATCH_DRAFT — proposition sans ecriture
bash scripts/ai/workers/run_task.sh \
  --job-packet docs/chantiers/.../<packet>.json \
  --dry-run

# WRITE_GATED — ecriture apres approbation
bash scripts/ai/workers/run_task.sh \
  --job-packet docs/chantiers/.../<packet>.json
```

## Dependance bridge

Le runner strict_workers utilise `modules/airtable_bridge/app/client.py` comme seul point d'acces API :

```python
# Integration dans le runner
from modules.airtable_bridge.app.client import send_go_status

result = send_go_status({
    "go_id": "GO_...",
    "status": "PASS",
    "machine": "fantome"
})
```

Le runner **ne doit jamais** :
- Appeler l'API Airtable directement
- Lire/modifier `.env` du bridge
- Court-circuiter le fail-open du bridge

## Garde-fous

- L'appel au bridge est encapsule dans le runner ; jamais d'appel direct depuis le job packet
- Toute erreur bridge est loggue et documentee dans le rapport
- Le bridge est fail-open ; une erreur API ne bloque pas le runner
- Les credentials Airtable ne sont jamais transmis dans le job packet
