---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_02_BATCH4_VERTICALES
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-02
  - readme
  - verticales
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/bot_vision_canonique.md
  - modules/bot_vision/README.md
  - modules/dev_validation_hub/README.md
  - modules/hf_free_platform/README.md
  - modules/trading_lab_v1/README.md
  - modules/trading_realtime_v1/README.md
---

# Step 02 - hygiene documentaire minimale - batch 4 verticales specialisees

## Statut
Complete.

## Objet
Terminer la couverture `README` des modules restants en documentant les verticales specialisees et en explicitant les frontieres qui restent sous arbitrage.

## Scope du batch
- `bot_vision`
- `dev_validation_hub`
- `hf_free_platform`
- `trading_lab_v1`
- `trading_realtime_v1`

## Verifications utilisees
- lecture des docs et cadrages embarques :
  - `docs/status/bot_vision_canonique.md`
  - `modules/bot_vision/bot_vision_step1/INSTALL_STEP1.md`
  - `modules/dev_validation_hub/docs/README.md`
  - `modules/hf_free_platform/spec/00_hf_free_platform_spec_v1.md`
  - `modules/hf_free_platform/spec/01_hf_free_platform_scope_v1.md`
  - `modules/hf_free_platform/handoff/00_hf_free_platform_recovery_pack.md`
  - `modules/trading_lab_v1/docs/README.md`
  - `modules/trading_realtime_v1/docs/README.md`
- lecture des entrypoints et wrappers :
  - `modules/bot_vision/bot_vision_step1/desk_pro_vision/vision/vision_generate.py`
  - `modules/bot_vision/scripts/cmd.sh`
  - `modules/dev_validation_hub/scripts/cmd.sh`
  - `modules/hf_free_platform/scripts/hf_free_platform_cmd.sh`
  - `modules/trading_lab_v1/app/trading_lab_v1.py`
  - `modules/trading_lab_v1/scripts/cmd.sh`
  - `modules/trading_realtime_v1/app/trading_realtime_v1.py`
  - `modules/trading_realtime_v1/scripts/cmd.sh`

## Fichiers ajoutes
- `modules/bot_vision/README.md`
- `modules/dev_validation_hub/README.md`
- `modules/hf_free_platform/README.md`
- `modules/trading_lab_v1/README.md`
- `modules/trading_realtime_v1/README.md`

## Decisions appliquees

### 1. Bot Vision reste explicitement ambigu au niveau famille
- `bot_vision` est documente comme verticale historique `step1`
- il n'est pas promu survivant par defaut
- la famille reste a arbitrer avec `bot_vision_step2` et `vision_bot`

### 2. Dev validation est isole comme surface dev-only
- `dev_validation_hub` est documente comme hub local de validation et pre-PR
- il reste hors runtime et hors prod

### 3. HF Free Platform reste une verticale de publication
- `hf_free_platform` est documente comme cible Hugging Face free-first
- la separation canon Git / publication HF est maintenant explicite au niveau racine du module

### 4. LAB et REALTIME restent deux branches distinctes
- `trading_lab_v1` est documente comme verticale analytique, batch et comparaison
- `trading_realtime_v1` est documente comme verticale runtime d'observation
- aucune fusion rapide n'est retenue

## Effet mesure
- baseline initiale : `58` modules avec `README`, `27` sans `README`
- apres batch 1 : `69` modules avec `README`, `16` sans `README`
- apres batch 2 OpenClaw : `76` modules avec `README`, `9` sans `README`
- apres batch 3 core wrappers : `80` modules avec `README`, `5` sans `README`
- apres batch 4 verticales specialisees : `85` modules avec `README`, `0` sans `README`

## Rollback
- revert doc-only des `README` ajoutes dans ce batch
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annule

## Point de reprise
`Step 02` est termine. Reprise sur `Step 03` pour figer survivants, transitions et compatibilites des familles `deepseek*`, `reseau_ssh*`, `bot_vision*` et `desk_*`.
