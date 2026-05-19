---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_RUNNER_MAPPING
doc_type: runner_mapping
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
status: draft_canonical
lifecycle_stage: mapping
topic_keys:
  - opt-trading
  - strict_workers
  - openclaw
  - opencode
  - runner
  - mapping
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/tasks.index.json
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
---

# 30_OPENCLAW_OPENCODE_RUNNER_MAPPING

## Architecture d'Appel

```
Trigger → OpenCode/OpenClaw → task.index.json → run_task.sh → worker IA → rapport DRAFT_ONLY → consolidation externe
```

## Triggers

### Manuel (OpenCode)

```text
openCode run-task <task_id> --input <path> [--model <model_id>]
```

Le modèle est sélectionné depuis la liste preferred_workers de la tâche dans tasks.index.json.
Si non spécifié, le premier worker VERIFIED de la liste est utilisé.

### Semi-automatique (OpenClaw Gateway)

```text
POST /api/v1/execute
{
  "intent": "<task_id>",
  "context": {
    "worker_id": "<model_id>",
    "source": "batch|webhook|manual"
  },
  "payload": {
    "input_paths": [...],
    "options": {}
  }
}
```

## Runner Attendu

| Propriété | Valeur |
| --- | --- |
| Runner | scripts/ai/workers/run_task.sh |
| Arguments | <task_id> <worker_model> <input_path> |
| Exemple | `./run_task.sh READ_INVENTORY opencode/qwen3.5-plus ./docs/` |
| Sortie | reports/ai/workers/<task_id>_<timestamp>.md |
| Code sortie | 0 = succès, 1 = stop condition, 2 = input refusé, 3 = erreur runner |

## Mapping Tâche → Runner

| Task | Runner | Arguments | Output path |
| --- | --- | --- | --- |
| READ_INVENTORY | run_task.sh | task_id, model, path(s) | reports/ai/workers/read_inventory_<ts>.md |
| PATCH_DRAFT | run_task.sh | task_id, model, files + objectif | reports/ai/workers/patch_draft_<ts>.md |
| DOC_DRAFT | run_task.sh | task_id, model, contexte | reports/ai/workers/doc_draft_<ts>.md |
| TESTPLAN | run_task.sh | task_id, model, module cible | reports/ai/workers/testplan_<ts>.md |
| CHERRY_PICK_INVENTORY | run_task.sh | task_id, model, commits+target | reports/ai/workers/cherry_pick_inventory_<ts>.md |
| FAST_TRIAGE | run_task.sh | task_id, model, items+categories | reports/ai/workers/fast_triage_<ts>.md |
| ENDPOINT_AUDIT | run_task.sh | task_id, model, endpoint+registry | reports/ai/workers/endpoint_audit_<ts>.md |
| WRITE_GATED | run_task.sh | task_id, model, write_plan | reports/ai/workers/write_gated_<ts>.md |

## Dry-Run Obligatoire (tâches A2 et plus)

Toute tâche A2+ doit d'abord être exécutée en dry-run :

```text
DRY_RUN_MODE=true ./run_task.sh <task_id> <model> <input>
```

Le rapport dry-run est stocké dans `reports/ai/workers/dry_run_<task_id>_<ts>.md`.
Le passage en mode write (WRITE_GATED) nécessite approbation explicite.

## Preuve de Non-Écriture

Chaque rapport worker doit inclure une section attestant :

```text
FICHIERS_LUS: [...]
FICHIERS_MODIFIES: []  (doit être vide pour READ_INVENTORY, PATCH_DRAFT, etc.)
WRITE_EFFECTUE: false
COMMANDES_EXECUTEES: ["read", "list", "cat", "grep"]  (uniquement read-only)
```

Pour WRITE_GATED, cette section devient :

```text
FICHIERS_LUS: [...]
FICHIERS_MODIFIES: [...]  (liste des fichiers write plan)
WRITE_EFFECTUE: true (dry-run: false)
COMMANDES_EXECUTEES: ["read", "write", ...]
DRY_RUN_MODE: true|false
APPROBATION: "humaine|refusee|en_attente"
```

## Healthcheck Minimum

| Check | Commande | Fréquence | Seuil |
| --- | --- | --- | --- |
| Runner disponible | `test -x scripts/ai/workers/run_task.sh` | Chaque appel | PASS=exécutable |
| Task index accessible | `test -f scripts/ai/workers/tasks.index.json` | Chaque appel | PASS=fichier présent |
| Registry accessible | `test -f scripts/ai/workers/models.registry.json` | Chaque appel | PASS=fichier présent |
| Worker modèle répond | `openCode run-task READ_INVENTORY opencode/<model> --dry-run` | Hebdomadaire | PASS=rapport généré |
| Output path accessible | `test -w reports/ai/workers/` | Chaque appel | PASS=accessible en écriture |
| Endpoint IA répond | `curl -s -o /dev/null -w "%{http_code}" <endpoint>` | Hebdomadaire | PASS=200/201 |

## Consolidation Externe

Toute sortie worker doit passer par la pipeline de consolidation avant d'être considérée valide :

```text
Sortie DRAFT_ONLY
  → revue modèle fort (GPT-5, Claude, Codex)
    → tests réels si applicable (commande de test listée)
      → git diff / état repo réel vérifié
        → validation humaine si A3/A4
          → sortie PROMOTED ou REJECTED
```

La sortie consolidée est stockée dans `reports/ai/workers/consolidated/<task_id>_<ts>.md`.
Le statut final est soit `PROMOTED` (validé), soit `REJECTED` (avec raison).
