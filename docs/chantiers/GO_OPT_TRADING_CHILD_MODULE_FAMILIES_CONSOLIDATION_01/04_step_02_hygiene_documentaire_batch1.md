---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_02_BATCH1
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: in_progress
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-02
  - readme
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - modules/desk_pro/README.md
  - modules/desk_common/README.md
  - modules/auth/README.md
  - modules/env/README.md
  - modules/health/README.md
  - modules/router/README.md
  - modules/webhook/README.md
  - modules/perf/README.md
  - modules/workflow_post_change_v2/README.md
  - modules/deepseek_response/README.md
  - modules/deepseek_thinking/README.md
---

# Step 02 — hygiene documentaire minimale — batch 1

## Statut
In progress.

## Objet
Poser les `README` manquants sur le premier bloc de modules actifs et ambigus, sans toucher au runtime ni aux wrappers.

## Scope du batch
- `desk_pro`
- `desk_common`
- `auth`
- `env`
- `health`
- `router`
- `webhook`
- `perf`
- `workflow_post_change_v2`
- `deepseek_response`
- `deepseek_thinking`

## Verifications utilisees
- lecture de l'arborescence de chaque module
- lecture des fichiers centraux :
  - `modules/desk_common/paths.py`
  - `modules/auth/webhook_key.py`
  - `modules/auth/secrets.py`
  - `modules/auth/bitget_credentials.py`
  - `modules/env/env.py`
  - `modules/health/checker.py`
  - `modules/webhook/handlers.py`
  - `modules/webhook/parse.py`
  - `modules/desk_pro/api/routes.py`
  - `modules/workflow_post_change_v2/scripts/post_change.sh`
  - `modules/deepseek_response/scripts/deepseek_response_cmd.sh`
  - `modules/deepseek_thinking/scripts/deepseek_thinking_cmd.sh`

## Fichiers ajoutes
- `modules/desk_pro/README.md`
- `modules/desk_common/README.md`
- `modules/auth/README.md`
- `modules/env/README.md`
- `modules/health/README.md`
- `modules/router/README.md`
- `modules/webhook/README.md`
- `modules/perf/README.md`
- `modules/workflow_post_change_v2/README.md`
- `modules/deepseek_response/README.md`
- `modules/deepseek_thinking/README.md`

## Decisions appliquees

### 1. Desk Pro
- `desk_pro` est documente comme surface partagee API/UI/service, distincte des facades `runner` et `dashboard`
- `desk_common` est documente comme support de chemins et de wrappers, pas comme centre de gravite produit

### 2. Runtime transverse
- `auth`, `env`, `health`, `webhook`, `perf`, `router` sont documentes selon leur role reel de brique ou facade
- `perf` est explicitement documente comme facade module autour de `perf/perf_app.py`

### 3. DeepSeek
- `deepseek_response` et `deepseek_thinking` sont documentes comme modules encore actifs en compatibilite, mais a consolider avec `deepseek_hub`

### 4. Post-change
- `workflow_post_change_v2` est documente selon son comportement reel post-journal local retire

## Effet mesure
- baseline initiale : `58` modules avec `README`, `27` sans `README`
- apres batch 1 : `69` modules avec `README`, `16` sans `README`

## Modules encore sans README
- `audit`
- `bot_vision`
- `configure_openclaw`
- `dev_validation_hub`
- `doctor_openclaw`
- `engines`
- `evidence_openclaw`
- `gateway_openclaw`
- `hf_free_platform`
- `install_module_openclaw`
- `marketdata`
- `menu_openclaw`
- `openclaw_config_modulaire`
- `scripts`
- `trading_lab_v1`
- `trading_realtime_v1`

## Rollback
- revert doc-only des `README` ajoutes dans ce batch
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annule

## Point de reprise
Poursuivre `Step 02` avec la famille `openclaw*`, puis les modules de plateforme restants sans `README`.
