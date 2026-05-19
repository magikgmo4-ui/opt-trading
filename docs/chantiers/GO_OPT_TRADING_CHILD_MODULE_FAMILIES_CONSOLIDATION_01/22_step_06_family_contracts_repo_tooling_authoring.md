---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_06_REPO_TOOLING_AUTHORING
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
  - step-06
  - repo-tooling
  - authoring
  - contracts
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/workflow_post_change_canonique.md
  - modules/audit/README.md
  - modules/dev_validation_hub/README.md
  - modules/git_fleet_guard/README.md
  - modules/install_module/README.md
  - modules/module_contextuals_shell/README.md
  - modules/naming_normalizer/README.md
  - modules/repo_hygiene/README.md
  - modules/repo_local_artifacts/README.md
  - modules/repo_ownership_guard/README.md
  - modules/trae_module_validator/README.md
  - modules/validated_prompt_factory/README.md
  - modules/workflow_post_change_v2/README.md
  - modules/install_module/scripts/cmd.sh
  - modules/workflow_post_change_v2/scripts/post_change.sh
---

# Step 06 - family contracts `Repo / tooling / authoring`

## Statut
Complete.

## Objet
Durcir la famille `Repo / tooling / authoring` par sous-roles explicites, conventions de wrappers, ownership d'artefacts et limites d'action.

## Verifications utilisees
- lecture de `docs/status/workflow_post_change_canonique.md`
- lecture des README de :
  - `modules/audit`
  - `modules/dev_validation_hub`
  - `modules/git_fleet_guard`
  - `modules/install_module`
  - `modules/module_contextuals_shell`
  - `modules/naming_normalizer`
  - `modules/repo_hygiene`
  - `modules/repo_local_artifacts`
  - `modules/repo_ownership_guard`
  - `modules/trae_module_validator`
  - `modules/validated_prompt_factory`
  - `modules/workflow_post_change_v2`
- lecture de `modules/install_module/scripts/cmd.sh`
- lecture de `modules/workflow_post_change_v2/scripts/post_change.sh`

## Carte de famille
| Sous-role | Surfaces retenues |
|---|---|
| methode / audit | `audit`, `naming_normalizer` |
| validation / garde-fous | `dev_validation_hub`, `trae_module_validator`, `git_fleet_guard` |
| hygiene repo locale | `repo_hygiene`, `repo_local_artifacts`, `repo_ownership_guard` |
| install / sync operatoire | `install_module` |
| authoring / generation | `validated_prompt_factory`, `module_contextuals_shell` |
| workflow post-change | `workflow_post_change_v2` |

## Contrats a durcir
### 1. Contrat de lecture seule par defaut
Les modules de garde-fous et d'audit doivent rester safe-by-default :
- `audit`
- `naming_normalizer`
- `dev_validation_hub`
- `git_fleet_guard`
- `trae_module_validator`

Leur mode par defaut doit privilegier :
- scan
- report
- validate
- explain

### 2. Contrat d'action explicite
Les modules qui modifient repo, shortcuts, ownership ou sync doivent exiger une intention explicite :
- `install_module`
- `repo_hygiene`
- `repo_local_artifacts`
- `repo_ownership_guard`
- `workflow_post_change_v2`

Ils ne doivent pas cacher des effets de bord importants derriere une simple commande `status`.

### 3. Contrat d'artefacts
- rapports et sorties doivent rester dans des repertoires modules dedies ou dans les surfaces runtime explicites
- aucun module de cette famille ne doit recreer un pseudo-journal local
- `workflow_post_change_v2` reste aligne sur la doctrine post-journal actuelle

### 4. Contrat d'authoring
- `validated_prompt_factory` et `module_contextuals_shell` restent des surfaces d'authoring / scaffolding
- ils ne doivent pas etre promus comme hubs runtime ni comme doctrine souveraine

### 5. Contrat de wrappers
Converger sur :
- `status`
- `scan` / `audit` / `validate`
- `apply` / `fix` / `sync` seulement quand l'action modifie reellement l'etat
- `sanity` pour les preconditions techniques

## Frontieres retenues
- `audit` module et dossier racine `audit/` restent distincts
- `install_module` reste un outil operatoire de distribution / sync, pas un orchestrateur produit general
- `workflow_post_change_v2` reste un hook operateur, pas un systeme de journal ni un moteur de workflow global
- `validated_prompt_factory` reste une brique d'authoring
- `module_contextuals_shell` reste un socle shell declaratif

## Ce qui doit rester separe
- hygiene repo locale et validation dev
- authoring et installation
- audit methode et preuves runtime
- workflow post-change et continuite documentaire canonique

## Risques a eviter
- multiplier les outils qui ecrivent dans les memes surfaces sans ownership clair
- laisser des modules de hygiene ou de sync agir de facon implicite ou destructive
- transformer `workflow_post_change_v2` en faux remplaçant de continuite doc ou de journal
- fusionner `validated_prompt_factory` avec d'autres modules de repo tooling alors que son role est d'authoring

## Decision retenue
- oui au durcissement par conventions et limites d'action
- non a une fusion physique globale
- prochaine execution utile si besoin :
  - matrice commune des verbes de wrappers
  - matrice des write scopes par module
  - inventaire des actions destructives ou sudo-gated

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Contrats `Repo / tooling / authoring` cadres. Basculer ensuite vers le gate `Step 07` ou directement vers `Step 08` si aucun move faible risque n'est justifie.
