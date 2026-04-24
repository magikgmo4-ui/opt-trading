---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_02_BATCH2_OPENCLAW
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
  - openclaw
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - modules/configure_openclaw/README.md
  - modules/doctor_openclaw/README.md
  - modules/evidence_openclaw/README.md
  - modules/gateway_openclaw/README.md
  - modules/install_module_openclaw/README.md
  - modules/menu_openclaw/README.md
  - modules/openclaw_config_modulaire/README.md
---

# Step 02 - hygiene documentaire minimale - batch 2 OpenClaw

## Statut
In progress.

## Objet
Documenter la famille `openclaw*` avant tout arbitrage de consolidation, sans toucher aux scripts, wrappers ou callers.

## Scope du batch
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `gateway_openclaw`
- `install_module_openclaw`
- `menu_openclaw`
- `openclaw_config_modulaire`

## Verifications utilisees
- lecture des docs module existantes :
  - `modules/configure_openclaw/docs/README.md`
  - `modules/doctor_openclaw/docs/README.md`
  - `modules/evidence_openclaw/docs/README.md`
  - `modules/gateway_openclaw/docs/README.md`
  - `modules/install_module_openclaw/docs/README.md`
- lecture des entrypoints et artefacts centraux :
  - `modules/gateway_openclaw/app/gateway_env.sh`
  - `modules/install_module_openclaw/app/modules_registry.json`
  - `modules/menu_openclaw/scripts/cmd.sh`
  - `modules/openclaw_config_modulaire/scripts/cmd.sh`
- lecture des runbooks utiles :
  - `modules/configure_openclaw/runbook/README.md`
  - `modules/doctor_openclaw/runbook/README.md`
  - `modules/evidence_openclaw/runbook/README.md`
- reference de famille :
  - `modules/model_provider_openclaw/README.md`

## Fichiers ajoutes
- `modules/configure_openclaw/README.md`
- `modules/doctor_openclaw/README.md`
- `modules/evidence_openclaw/README.md`
- `modules/gateway_openclaw/README.md`
- `modules/install_module_openclaw/README.md`
- `modules/menu_openclaw/README.md`
- `modules/openclaw_config_modulaire/README.md`

## Decisions appliquees

### 1. Famille OpenClaw explicitee comme suite
- `menu_openclaw` est documente comme hub operateur de la suite
- `install_module_openclaw` est documente comme installateur alimente par un registre local de modules
- `gateway_openclaw` est documente comme facade de runtime et de pilotage `tmux`

### 2. Configuration et diagnostic separes
- `configure_openclaw` reste la facade de configuration et de post-install
- `openclaw_config_modulaire` reste la brique modulaire de backup/apply/rollback
- `doctor_openclaw` reste la facade de diagnostic et de reparation prudente

### 3. Evidence et preuve conservees comme fonction distincte
- `evidence_openclaw` est documente comme surface d'export de preuves et de generation de prompts
- la famille n'est pas fusionnee a ce stade ; le plan retient une suite coordonnee, pas un move physique

## Effet mesure
- baseline initiale : `58` modules avec `README`, `27` sans `README`
- apres batch 1 : `69` modules avec `README`, `16` sans `README`
- apres batch 2 OpenClaw : `76` modules avec `README`, `9` sans `README`

## Modules encore sans README
- `audit`
- `bot_vision`
- `dev_validation_hub`
- `engines`
- `hf_free_platform`
- `marketdata`
- `scripts`
- `trading_lab_v1`
- `trading_realtime_v1`

## Rollback
- revert doc-only des `README` ajoutes dans ce batch
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annule

## Point de reprise
Poursuivre `Step 02` avec les `9` modules restants sans `README`, en priorisant `engines`, `marketdata`, `scripts`, `audit` puis les verticales `bot_vision`, `hf_free_platform`, `trading_lab_v1`, `trading_realtime_v1`, `dev_validation_hub`.
