---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_LISTE
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: active
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - modules
  - inventory
  - families
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - registry/modules_registry.yaml
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/00_cadrage.md
---

# Liste des modules

## Baseline
- total observe : `85` modules
- modules avec `README.md` : `58`
- modules sans `README.md` : `27`

## Familles retenues pour lecture

### 1. Desk / Desk Pro
- `desk_analyze`
- `desk_capture_inputs`
- `desk_common`
- `desk_pro`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `desk_retention`
- `desk_snapshot_ingest`
- `desk_state`

### 2. Engines / trading pipeline
- `decision_engine`
- `execution_engine`
- `engines`
- `journal_engine`
- `perf_engine`
- `portfolio_engine`
- `position_engine`
- `probability_engine`
- `risk_engine`

### 3. Collectors / market / derivatives
- `collector_binance_spot`
- `collector_coingecko`
- `derivatives_analyzer`
- `derivatives_collector`
- `liquidation_analyzer`
- `market_scanner`
- `marketdata`
- `opportunity_ranker`

### 4. Registry / UI / navigation operateur
- `machines_registry_reader`
- `modules_registry_reader`
- `ops_menu_hub`
- `ops_super_menu`
- `ops_wrappers`
- `registry_meta_reader`
- `registry_router`
- `ui_registry_msi`
- `wrappers_registry_reader`

### 5. Openclaw
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `gateway_openclaw`
- `install_module_openclaw`
- `menu_openclaw`
- `model_provider_openclaw`
- `openclaw_config_modulaire`

### 6. Reseau / partage / transfert
- `reseau_ssh`
- `reseau_ssh_step1b`
- `reseau_ssh_step2`
- `shared_files_sftp`
- `shared_sshfs_permanent`
- `winscp_transfer`

### 7. DeepSeek / student / memoire locale
- `deepseek_hub`
- `deepseek_response`
- `deepseek_student`
- `deepseek_thinking`
- `memory_bricks`
- `perm_fix_student`

### 8. Repo / tooling / authoring
- `audit`
- `dev_validation_hub`
- `git_fleet_guard`
- `install_module`
- `module_contextuals_shell`
- `naming_normalizer`
- `repo_hygiene`
- `repo_local_artifacts`
- `repo_ownership_guard`
- `trae_module_validator`
- `validated_prompt_factory`
- `workflow_post_change_v2`

### 9. Runtime edge / platform
- `auth`
- `env`
- `health`
- `perf`
- `router`
- `scripts`
- `shared`
- `webhook`

### 10. Vision / verticales speciales / experimentaux
- `bot_vision`
- `bot_vision_step2`
- `hf_free_platform`
- `kil_v1`
- `mimo_open_observer`
- `simex_bitget_bridge`
- `trading_lab_v1`
- `trading_realtime_v1`
- `vision_bot`

## Modules sans README
- `audit`
- `auth`
- `bot_vision`
- `configure_openclaw`
- `deepseek_response`
- `deepseek_thinking`
- `desk_common`
- `desk_pro`
- `dev_validation_hub`
- `doctor_openclaw`
- `engines`
- `env`
- `evidence_openclaw`
- `gateway_openclaw`
- `health`
- `hf_free_platform`
- `install_module_openclaw`
- `marketdata`
- `menu_openclaw`
- `openclaw_config_modulaire`
- `perf`
- `router`
- `scripts`
- `trading_lab_v1`
- `trading_realtime_v1`
- `webhook`
- `workflow_post_change_v2`

## Observations utiles
- la simple nomenclature montre deja des familles step-by-step (`reseau_ssh*`, `bot_vision*`)
- plusieurs modules parapluie n'ont pas de `README` alors qu'ils servent de centre de gravite de suite (`desk_pro`, `desk_common`)
- certaines familles ont deja une preuve documentaire de lignee dans `docs/status/*`, sans encore avoir un plan d'execution associe

## Point de reprise
Passer a `02_ensembles_a_consolider.md` pour distinguer ce qui doit etre consolide, coordonne ou laisse separe.
