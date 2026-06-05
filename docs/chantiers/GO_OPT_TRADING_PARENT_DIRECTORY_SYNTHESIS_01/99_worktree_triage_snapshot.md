---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_WORKTREE_TRIAGE_01
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: repo
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - worktree
  - triage
  - staging
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/90_recap_parent.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
---

# Worktree triage snapshot

## Snapshot
- branch: `codex/repo-directory-synthesis-parent-01`
- date: `2026-04-24`
- etat Git: dirty
- fichiers trackes modifies: `8`
- fichiers non trackes: `54`

## 1. Herite / hors lot courant
Ces surfaces ne doivent pas etre stagees avec le lot courant.

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/00_cadrage.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_decisions.md`

## 2. Produit par le lot courant
Ces surfaces relevent du travail `repo-directory-synthesis` et du child `modules`.

### 2.1 Documentaire repo-level
- `docs/architecture/REPO_SURFACES_MAP.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/*` (`17` fichiers)

### 2.2 Child modules
- `docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/*` (`8` fichiers)
- `27` `README.md` ajoutes sous `modules/` :
  - `audit`, `auth`, `bot_vision`, `configure_openclaw`, `deepseek_response`, `deepseek_thinking`
  - `desk_common`, `desk_pro`, `dev_validation_hub`, `doctor_openclaw`, `engines`, `env`
  - `evidence_openclaw`, `gateway_openclaw`, `health`, `hf_free_platform`, `install_module_openclaw`, `marketdata`
  - `menu_openclaw`, `openclaw_config_modulaire`, `perf`, `router`, `scripts`, `trading_lab_v1`
  - `trading_realtime_v1`, `webhook`, `workflow_post_change_v2`

### 2.3 Fichiers partages / melanges
Ces fichiers ont ete touches par le lot courant, mais ils servent aussi de surfaces de continuite communes.

- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

## 3. Pret a stage / commit maintenant
Sous-ensemble propre recommande pour un commit sans melanger les surfaces heritees ou partagees.

- `docs/architecture/REPO_SURFACES_MAP.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/*`
- `docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/*`
- les `27` `modules/*/README.md` ajoutes dans le child

Total recommande a stage immediatement : `54` fichiers.

## 4. A laisser de cote
Ces surfaces doivent rester hors du prochain commit de ce lot.

- les `4` fichiers herites listes en section 1
- les `4` fichiers `docs/index/*`, a traiter ensuite dans un lot ou un commit separe si on veut garder un historique propre

## 5. Sequence recommandee
1. stage le sous-ensemble propre de `54` fichiers
2. commit le lot `repo-directory-synthesis` + `child modules`
3. traiter `docs/index/*` dans un commit separe, ou apres nettoyage des changements herites
4. laisser le lot `DOC_OPS` hors de cette serie

## RISKS

- À qualifier.
