# STRICT WORKER REPORT — READ_INVENTORY

## 13_ESTABLISHED

### Project: opt-trading

| Aspect | Valeur |
|---|---|
| Root | opt-trading (git, sot/mainline) |
| Top-level dirs | 37 entries (docs/, scripts/, modules/, config/, tests/, .github/, etc.) |
| docs/chantiers/ | ~400+ GO directories (GO_OPT_TRADING_*, GO_STRATEGY_*, etc.) |
| docs/agents/ | strict_workers/ (autonomie etroite, models matrix, model id validation) |
| modules/ | ~200+ modules (bot_vision, desk_pro, airtable_bridge, strategy, etc.) |
| scripts/ | ~100+ scripts (ai/, admin_trading, db_layer, git_ops, etc.) |
| config/ | machine_runtime_map.yml |
| tests/ | ~15 test files/dirs (e2e, runtime_health, openclaw, fixtures) |
| Lignes totales (12 fichiers) | 681 insertions (PR #606) |

### Strict Workers Infrastructure

| Fichier | Description |
|---|---|
| scripts/ai/workers/tasks.index.json | Index des 8 task types (schema_version 0.3-draft) |
| scripts/ai/workers/models.registry.json | Registry des modeles (24 entrees, 10 VERIFIED + 5 VERIFIED_FREE) |
| scripts/ai/workers/run_task.sh | Runner lock (validation + prompt generation) |
| scripts/ai/workers/_validate_job.py | Validateur de job packets (4 env vars) |
| scripts/ai/workers/job_packets/ | 22 job packets JSON (8 promus + 14 existants) |
| reports/ai/workers/ | 15 rapports existants de runs anterieurs |

### Job Packets (22 total)

| Type | Nombre | Statut |
|---|---|---|
| MATRIX (promus PR #606) | 8 | DRAFT_ONLY |
| A4 NEGATIVE tests (N1-N5) | 5 | TEST |
| A4 POSITIVE test (P6) | 1 | TEST |
| A4 WRITE REEL test | 1 | TEST |
| E2E tests (A, B) | 2 | TEST |
| POOL SMOKE (3 modeles) | 3 | SMOKE |
| READONLY SMOKE | 1 | SMOKE |
| PATCH_DRAFT_IMPL | 1 | TEST |

### Workers VERIFIED (10)

glm-5.1, glm-5, kimi-k2.5, kimi-k2.6, minimax-m2.7, minimax-m2.5, qwen3.6-plus, qwen3.5-plus, big-pickle, gpt-5-nano

### Workers VERIFIED_FREE (5)

minimax-m2.5-free, nemotron-3-super-free, deepseek-v4-flash-free, ring-2.6-1t-free, trinity-large-preview-free

### CI/CD Workflows

| Workflow | Status |
|---|---|
| .github/workflows/strict-workers-validate.yml | Merged (PR #601, #602) |
| .github/workflows/strict-workers-smoke.yml | Merged (PR #601, #602) |
| .github/workflows/strict-workers-schedule.yml | Merged (PR #601) |

### 8 Promoted Job Packets (PR #606, merged 87f9d1c1)

| Packet | Default Worker | Autonomy | Writes |
|---|---|---|---|
| READ_INVENTORY_MATRIX_01 | qwen3.5-plus | A1 | false |
| PATCH_DRAFT_MATRIX_01 | glm-5.1 | A2 | false |
| DOC_DRAFT_MATRIX_01 | qwen3.5-plus | A2 | false |
| TESTPLAN_MATRIX_01 | glm-5.1 | A2 | false |
| CHERRY_PICK_INVENTORY_MATRIX_01 | kimi-k2.5 | A2 | false |
| FAST_TRIAGE_MATRIX_01 | qwen3.5-plus | A1 | false |
| ENDPOINT_AUDIT_MATRIX_01 | qwen3.5-plus | A1 | false |
| WRITE_GATED_DRYRUN_MATRIX_01 | glm-5.1 | A4 (dry) | true (dry) |

## 14_HYPOTHESIS

1. Les 8 job packets MATRIX sont validables par la CI/CD car ils suivent le schema exact de GO_STRICT_WORKERS_READONLY_SMOKE_01.json (valide en production)
2. Le runner lock (run_task.sh) bloque correctement les ecritures non autorisees, les secrets, et le dirty working tree
3. Les task types dans tasks.index.json couvrent tous les besoins de la chaine strict workers (read-only, patch, doc, test, cherry-pick, triage, audit, write-gated)
4. Les modeles VERIFIED du registry sont suffisants pour executer chaque type de tache avec au moins un worker candidat

## 15_REMAINING_GAP

1. Le run_task.sh genere un PROMPT mais n appelle pas le worker model automatiquement — l etape d inference (feed prompt → get output) est manuelle
2. Aucun job packet n a encore ete execute en run reel depuis la promotion PR #606 — ce rapport est le premier
3. Pas de mecanisme de circuit-breaker si le worker model produit un output invalide (sections manquantes, verdict absent)
4. Les CI/CD workflows validate.yml et smoke.yml filtrent les job packets par glob (job_packets/*.json) — ils valideront aussi les 8 nouveaux packets au prochain push

## 16_TODO

1. Executer les runs reels des 8 job packets promus dans l ordre de risque croissant: READ_INVENTORY → FAST_TRIAGE → ENDPOINT_AUDIT → DOC_DRAFT → TESTPLAN → CHERRY_PICK_INVENTORY → PATCH_DRAFT → WRITE_GATED_DRYRUN
2. Ajouter un validateur post-output qui verifie que le rapport genere contient toutes les required_output_sections
3. Decider si run_task.sh doit integrer l appel au worker model ou rester un generateur de prompt manuel
4. Mettre a jour models.registry.json avec validation_at le 2026-05-19

## FICHIERS_LUS

- scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01.json
- scripts/ai/workers/tasks.index.json
- scripts/ai/workers/models.registry.json
- scripts/ai/workers/run_task.sh
- scripts/ai/workers/_validate_job.py
- scripts/ai/workers/job_packets/ (22 fichiers listes)
- reports/ai/workers/ (fichiers listes)
- docs/ (structure)
- docs/agents/strict_workers/ (dossier)
- docs/chantiers/ (liste des dossiers GO)
- scripts/ (structure)
- modules/ (structure)
- config/machine_runtime_map.yml
- tests/ (structure)
- .github/workflows/strict-workers-validate.yml
- .github/workflows/strict-workers-smoke.yml
- reports/ai/workers/GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01_PROMPT.txt

## RISQUES

- R1: Les globs larges (docs/**, scripts/**, modules/**) en allowed_inputs donnent acces a beaucoup de fichiers — tout modele worker doit etre fiable pour ne pas lire les zones denied (**.env, **secret*, etc.)
- R2: run_task.sh bloque sur working tree dirty — les fichiers generes dans reports/ai/workers/ ne sont pas trackes par .gitignore (s ils etaient trackes, le deuxieme run echouerait)
- R3: Les modeles VERIFIED_FREE sont dans les worker_candidates mais ignores par _validate_job.py (verifie seulement status == 'VERIFIED') — si un jour on veut un default_worker VERIFIED_FREE, le validateur echouera

## VERDICT_DRAFT_ONLY
