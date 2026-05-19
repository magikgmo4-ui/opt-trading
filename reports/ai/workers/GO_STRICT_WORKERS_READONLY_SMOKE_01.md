13_ESTABLISHED: Read-only smoke READ_INVENTORY initiated on branch go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01. Priority model: qwen3.5-plus. Allowed inputs: docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md, docs/agents/strict_workers/MODELS_MATRIX_01.md, docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md, scripts/ai/workers/tasks.index.json, scripts/ai/workers/models.registry.json. Job packet: GO_STRICT_WORKERS_READONLY_SMOKE_01.json.

14_HYPOTHESIS: We will inventory the allowed inputs using the READ_INVENTORY path with a non-writing, read-only footprint. Model pool prioritized: qwen3.5-plus. If unavailable, fallback to big-pickle. No runtime writes, no git operations, and no exposure of secrets.

15_REMAINING_GAP: Aucune lacune majeure détectée dans les inputs autorisés. Si l’inventaire révèle des inputs manquants ou non lisibles, ces éléments seront notés ici et les étapes suivantes ajustées.

16_TODO:
- Lire les inputs autorisés et consigner les résultats dans le rapport.
- Vérifier l’absence de secrets dans les contenus lus.
- Générer le rapport et le déposer sous reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01.md (DRAFT_ONLY).
- Documenter la progression dans docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/02_READONLY_SMOKE_EXEC_REPORT.md.

FICHIERS_LUS:
- scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
- docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
- docs/agents/strict_workers/MODELS_MATRIX_01.md
- docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md
- scripts/ai/workers/models.registry.json
- scripts/ai/workers/tasks.index.json
- (lecture du fichier README/placeholder selon disponibilité)

RISQUES:
- Risque mineur d’interprétation si les inputs contiennent des informations ambiguës dans les docs; on s’appuiera sur la matrice et les validations existantes pour trianguler.
- Aucun secret ne sera exposé ni lu dans ce smoke; toute donnée sensible est exclue par design.

VERDICT_DRAFT_ONLY: DRAFT_ONLY
