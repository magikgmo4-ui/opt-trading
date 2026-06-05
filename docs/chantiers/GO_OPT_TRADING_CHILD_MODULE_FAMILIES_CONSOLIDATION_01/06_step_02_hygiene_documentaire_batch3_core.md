---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_02_BATCH3_CORE
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
  - core
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - modules/engines/README.md
  - modules/marketdata/README.md
  - modules/scripts/README.md
  - modules/audit/README.md
---

# Step 02 - hygiene documentaire minimale - batch 3 core wrappers

## Statut
In progress.

## Objet
Documenter le bloc core restant le plus transversal avant de passer aux verticales specialisees encore sans `README`.

## Scope du batch
- `engines`
- `marketdata`
- `scripts`
- `audit`

## Verifications utilisees
- lecture des entrypoints Python :
  - `modules/engines/__init__.py`
  - `modules/engines/registry.py`
  - `modules/engines/router.py`
- lecture des wrappers shell :
  - `modules/engines/scripts/engines_cmd.sh`
  - `modules/engines/scripts/menu.sh`
  - `modules/marketdata/scripts/cmd.sh`
  - `modules/marketdata/scripts/menu.sh`
  - `modules/scripts/scripts/cmd.sh`
  - `modules/scripts/scripts/menu.sh`
  - `modules/audit/scripts/cmd.sh`
- lecture des docs embarquees :
  - `modules/audit/docs/AUDIT_STRICT_CHECKLIST.md`
  - `modules/audit/docs/AUDIT_THINKING_GUIDE.md`

## Fichiers ajoutes
- `modules/engines/README.md`
- `modules/marketdata/README.md`
- `modules/scripts/README.md`
- `modules/audit/README.md`

## Decisions appliquees

### 1. Engines reste une couche de coordination
- `engines` est documente comme registre et routeur minimal
- il ne devient pas le survivant des modules `*_engine`
- son traitement releve plutot de `Step 06` sur les contracts que d'une fusion

### 2. Marketdata reste une facade legere
- `marketdata` est documente comme surface de wrappers et de navigation
- la logique metier effective reste diffusee dans les collectors et modules de marche adjacents

### 3. Scripts reste distinct de la racine
- `modules/scripts` est documente comme module wrapper
- il ne doit pas etre confondu avec la racine `scripts/`

### 4. Audit methode distincte de audit preuves
- `modules/audit` est documente comme methode et outillage
- la distinction avec la racine `audit/` est maintenant explicite

## Effet mesure
- baseline initiale : `58` modules avec `README`, `27` sans `README`
- apres batch 1 : `69` modules avec `README`, `16` sans `README`
- apres batch 2 OpenClaw : `76` modules avec `README`, `9` sans `README`
- apres batch 3 core wrappers : `80` modules avec `README`, `5` sans `README`

## Modules encore sans README
- `bot_vision`
- `dev_validation_hub`
- `hf_free_platform`
- `trading_lab_v1`
- `trading_realtime_v1`

## Rollback
- revert doc-only des `README` ajoutes dans ce batch
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annule

## Point de reprise
Poursuivre `Step 02` avec les `5` verticales restantes sans `README`, en priorisant `bot_vision`, `dev_validation_hub`, `hf_free_platform`, `trading_lab_v1`, `trading_realtime_v1`.

## RISKS

- À qualifier.
