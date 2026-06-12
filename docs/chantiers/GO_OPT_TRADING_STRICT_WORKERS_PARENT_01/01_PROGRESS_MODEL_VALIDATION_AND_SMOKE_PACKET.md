---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01_PROGRESS_MODEL_VALIDATION_AND_SMOKE_PACKET
doc_type: progress_note
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: validation
topic_keys:
  - strict_workers
  - model_validation
  - readonly_smoke
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/01_PROGRESS_MODEL_VALIDATION_AND_SMOKE_PACKET.md
point_de_reprise: "Exécuter le premier READ_INVENTORY via OpenCode local"
updated_at: 2026-04-26
links:
  - docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
---

# Progress — Model validation + readonly smoke packet

## 13_ESTABLISHED

La validation d'IDs OpenCode Zen existe déjà dans :

```text
docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md
```

Le registry modèle existe déjà dans :

```text
scripts/ai/workers/models.registry.json
```

Le task index existe déjà en version :

```text
schema_version: 0.2-draft
only_verified_models: true
```

Un job packet READ_INVENTORY a été ajouté :

```text
scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

## 14_HYPOTHESIS

À valider localement dans OpenCode :

```text
- le modèle qwen3.5-plus est disponible dans l'environnement connecté
- le runner local pourra charger tasks.index.json + models.registry.json + job packet
- les chemins allowed_inputs sont lisibles sans exposition de secrets
```

## 15_REMAINING_GAP

Reste à faire :

```text
- créer ou brancher un runner local
- créer les commandes .opencode/commands si absent
- exécuter un premier READ_INVENTORY réellement
- produire reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01.md
- consolider le rapport par modèle fort / humain
```

## 16_TODO

Prochain GO :

```text
GO_STRICT_WORKERS_READONLY_SMOKE_EXEC_01
```

Actions :

```text
1. Vérifier OpenCode local.
2. Charger le job packet.
3. Router vers qwen3.5-plus ou fallback big-pickle.
4. Exiger sortie DRAFT_ONLY.
5. Vérifier qu'aucun fichier source n'a été modifié.
```

## 17_RESUME_POINT

```text
Reprendre sur go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01.
Le chantier est prêt pour un premier smoke READ_INVENTORY local.
Ne pas passer à PATCH_DRAFT avant validation du smoke read-only.
```

## RISKS

- À qualifier.
