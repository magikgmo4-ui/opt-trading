---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01_RUNNER_MAPPING
doc_type: runner_mapping
repo: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01
status: draft
---

# 20_RUNNER_MAPPING — ClickUp Task Tracker Worker

## Mapping tache -> worker -> runner

| Tache | Job Packet | Modele | Runner | Output |
| --- | --- | --- | --- | --- |
| READ_INVENTORY ClickUp | `GO_STRICT_WORKERS_CLICKUP_READ_INVENTORY_01` | qwen3.5-plus | `run_task.sh` + API ClickUp | `reports/ai/workers/clickup_inventory_<ts>.md` |
| PATCH_DRAFT ClickUp | `GO_STRICT_WORKERS_CLICKUP_PATCH_DRAFT_01` | glm-5.1 | `run_task.sh` + API ClickUp | `reports/ai/workers/clickup_patch_draft_<ts>.md` |

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
```

## API ClickUp

Le runner peut utiliser le script existant `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/execute_clickup.py` comme reference pour les appels API :

```text
Base: https://api.clickup.com/api/v2
Auth: Bearer token (depuis /tmp/clickup_token ou env CLICKUP_TOKEN)
Team: 90141225112

GET    /list/{list_id}/task         → lecture des taches
PUT    /task/{task_id}              → mise a jour (reserve WRITE_GATED)
GET    /list/{list_id}              → infos liste
```

Le runner **ne doit jamais** :
- Lire/modifier `/tmp/clickup_token`
- Court-circuiter le script execute_clickup.py
- Faire des appels PUT/POST/DELETE sans approbation explicite

## Garde-fous

- Token ClickUp jamais transmis dans le job packet
- READ_INVENTORY uniquement GET
- PATCH_DRAFT : dry-run obligatoire, patch NON applique
- Toute erreur API est loggee et documentee dans le rapport
