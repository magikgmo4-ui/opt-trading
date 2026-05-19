---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_EXECUTION_SUBLOTS
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - modules
  - execution
  - sublots
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/91_synthese_resultats.md
---

# Plans d'execution par sous-lot

## Regle
Chaque sous-lot doit rester borne :
- un objectif net
- un scope court
- un rollback simple
- pas de move physique sans preuve caller-level

## Sous-lots prioritaires d'execution

### 1. `GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01`
- priorite : `P1`
- nature : structuration + conventions + eventuelles mutualisations legeres
- etat courant :
  - lance et clos doc-only le `2026-04-24`
  - voir `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md`
- objectif :
  - consolider la suite OpenClaw comme cockpit local borne
  - harmoniser wrappers, docs et chainage install -> policy -> config -> gateway -> doctor -> evidence
- scope initial :
  - `install_module_openclaw`
  - `model_provider_openclaw`
  - `openclaw_config_modulaire`
  - `configure_openclaw`
  - `gateway_openclaw`
  - `doctor_openclaw`
  - `evidence_openclaw`
  - `menu_openclaw`
- premiers steps :
  1. cartographier les verbes de wrappers
  2. fixer un runbook de suite unique
  3. mutualiser uniquement les helpers shell/documentaires repetes
  4. verifier qu'aucune fusion runtime n'est necessaire
  5. fermer en conventions si la structure suffit
- risque :
  - faible a modere
- move physique probable :
  - non par defaut

### 2. `GO_OPT_TRADING_RESEAU_SHARE_TRANSFER_CONSOLIDATION_01`
- priorite : `P1`
- nature : conventions + wrappers + ownership machine
- objectif :
  - rendre coherente la suite `reseau / partage / transfert`
  - sans melanger baseline SSH, surface `shared`, exposition serveur, montage client et workflow Windows
- scope initial :
  - `reseau_ssh_step2`
  - `shared`
  - `shared_files_sftp`
  - `shared_sshfs_permanent`
  - `winscp_transfer`
- premiers steps :
  1. fixer matrice machine -> ownership -> wrapper
  2. normaliser `status/path/sanity/show-*`
  3. produire une carte unique de la suite
  4. auditer les callers avant toute mutualisation
  5. decider s'il n'y a qu'un lot de conventions ou un petit patch wrapper
- risque :
  - modere
- move physique probable :
  - non

### 3. `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01`
- priorite : `P1`
- nature : clarification runtime / transition / compat
- objectif :
  - arbitrer proprement `scripts/student/` vs `deepseek_hub`
  - reduire l'ambiguite entre runtime reel, facade candidate et couches de compatibilite
- scope initial :
  - `scripts/student/`
  - `deepseek_hub`
  - `deepseek_response`
  - `deepseek_thinking`
  - `deepseek_student`
- premiers steps :
  1. auditer les callers et wrappers reels
  2. figer la matrice de verbes entre `deepseek-student` et `deepseek_hub`
  3. verifier ce qui reste vraiment necessaire dans `deepseek_response` / `deepseek_thinking`
  4. decider si `deepseek_student` reste transition seule
  5. seulement ensuite, evaluer un lot de consolidation
- risque :
  - modere a eleve
- move physique probable :
  - possible plus tard, pas au debut

### 4. `GO_OPT_TRADING_VISION_FAMILY_SURVIVOR_DECISION_01`
- priorite : `P1`
- nature : decision produit / runtime, pas fusion immediate
- objectif :
  - fixer la cible finale de la famille `Vision`
  - decider si le couple transitoire doit rester stable, ou si un survivant unique est materialisable
- scope initial :
  - `bot_vision`
  - `vision_bot`
  - `bot_vision_step2`
- premiers steps :
  1. formaliser la cible cross-platform headless
  2. verifier le contrat input/output reel entre `vision_bot` et `bot_vision_step2`
  3. qualifier la dette `step1` de `bot_vision`
  4. decider survivant / binome durable / simple layering
  5. seulement ensuite, envisager un lot d'alignement wrappers
- risque :
  - eleve
- move physique probable :
  - non au depart

### 5. `GO_OPT_TRADING_DESK_PRO_STACK_CONSOLIDATION_01`
- priorite : `P2`
- nature : gros lot de frontieres de stack
- objectif :
  - consolider la stack Desk Pro sans casser la hierarchie `ops hub -> admin wrapper -> runner -> orchestrator/dashboard`
- scope initial :
  - `desk_pro`
  - `desk_common`
  - `desk_pro_runner`
  - `desk_pro_orchestrator`
  - `desk_pro_dashboard`
  - satellites `desk_*`
- premiers steps :
  1. figer les contrats d'artefacts run-level et dashboard
  2. auditer les callers admin et multi-machine
  3. verifier le role exact de chaque satellite
  4. documenter les scopes d'ownership
  5. ne proposer des moves qu'en dernier
- risque :
  - eleve
- move physique probable :
  - eventuel plus tard seulement

## Sous-lots de contrat / alignement

### 6. `GO_OPT_TRADING_REGISTRY_UI_LOCALCMS_CONTRACTS_01`
- priorite : `P2`
- objectif :
  - produire la matrice producer / consumer et les contrats d'exposition UI vers `localcms`
- nature :
  - doc + contrats, pas migration de repo

### 7. `GO_OPT_TRADING_COLLECTORS_FAMILY_ALIGNMENT_01`
- priorite : `P2`
- objectif :
  - derouler la migration map collectors :
    - inventory
    - vocabulary
    - artifacts
    - config
    - operator surface
- nature :
  - contrat et convergence selective

### 8. `GO_OPT_TRADING_ENGINE_PIPELINE_CONTRACT_ALIGNMENT_01`
- priorite : `P3`
- objectif :
  - normaliser envelopes d'output, `run_id`, `summary`, `sample/explain/export`
- nature :
  - contrats seulement

### 9. `GO_OPT_TRADING_RUNTIME_EDGE_PLATFORM_BOUNDARIES_01`
- priorite : `P3`
- objectif :
  - documenter ownership des fichiers `state/`, `tmp/`, `data/`, `perf/perf.db`
  - aligner les verbes `status/info/path`
- nature :
  - contrats et entrypoints

### 10. `GO_OPT_TRADING_REPO_TOOLING_WRAPPER_CONVENTIONS_01`
- priorite : `P3`
- objectif :
  - matrice commune des verbes de wrappers
  - write scopes
  - actions safe-by-default vs action explicite
- nature :
  - conventions repo/tooling

## Ordre recommande
1. `GO_OPT_TRADING_RESEAU_SHARE_TRANSFER_CONSOLIDATION_01`
2. `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01`
3. `GO_OPT_TRADING_VISION_FAMILY_SURVIVOR_DECISION_01`
4. `GO_OPT_TRADING_DESK_PRO_STACK_CONSOLIDATION_01`
5. lots de contrats transverses selon besoin

## Gate de lancement
Avant d'ouvrir un sous-lot d'execution, verifier :
- le besoin produit ou operatoire est reel
- le scope tient dans un seul lot
- les callers critiques sont identifiables
- le rollback est simple
- aucune autre famille n'est implicitement rouverte par bord
