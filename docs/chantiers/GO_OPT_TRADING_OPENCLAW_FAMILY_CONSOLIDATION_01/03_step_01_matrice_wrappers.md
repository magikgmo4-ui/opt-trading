---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_STEP_01_WRAPPERS
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - openclaw
  - wrappers
  - verbs
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md
  - modules/install_module_openclaw/scripts/cmd.sh
  - modules/model_provider_openclaw/scripts/cmd.sh
  - modules/openclaw_config_modulaire/scripts/cmd.sh
  - modules/configure_openclaw/scripts/cmd.sh
  - modules/gateway_openclaw/scripts/cmd.sh
  - modules/doctor_openclaw/scripts/cmd.sh
  - modules/evidence_openclaw/scripts/cmd.sh
  - modules/menu_openclaw/scripts/cmd.sh
---

# Step 01 - matrice des wrappers `OpenClaw`

## Statut
Complete.

## Objet
Cartographier les wrappers reels de la suite `OpenClaw` :
- verbes exposes
- couplages inter-modules
- ecarts de nomenclature
- ecarts de write-scope

## Verifications utilisees
- lecture de `scripts/cmd.sh` sur les `8` modules
- lecture de `scripts/install_shortcuts.sh` sur les modules representatifs
- lecture de la cartographie existante et des README de suite
- `git grep` cible sur les callers `cmd-*` et `menu-*`

## Invariants observes
- les `8` modules exposent `scripts/cmd.sh`, `scripts/menu.sh`, `scripts/sanity.sh`
- les `8` modules exposent `scripts/install_shortcuts.sh`
- `sanity` est present partout
- `status` est present partout sauf pas sous la meme densite de sortie
- les write-scopes sont heterogenes :
  - lecture seule pour `model_provider_openclaw`
  - ecriture locale forte pour `install_module_openclaw`, `openclaw_config_modulaire`, `gateway_openclaw`
  - ecriture documentaire pour `evidence_openclaw`

## Matrice des verbes observes
| Module | Verbes `cmd.sh` observes | Notes |
| --- | --- | --- |
| `install_module_openclaw` | `sanity`, `list`, `status`, `install`, `paths` | `install` copie des modules vers `/opt/trading` |
| `model_provider_openclaw` | `status`, `sanity`, `show-agent`, `export-json` | seul module avec `sanity-model_provider_openclaw` |
| `openclaw_config_modulaire` | `sanity`, `status`, `backup`, `apply`, `validate`, `health`, `probe`, `rollback`, `paths` | coeur structurel et rollback |
| `configure_openclaw` | `sanity`, `status`, `validate`, `config-file`, `wizard`, `dashboard`, `agents-list`, `agents-add`, `set-identity-from-workspace`, `get`, `set`, `unset` | facade live operateur |
| `gateway_openclaw` | `sanity`, `status`, `start`, `stop`, `logs`, `attach`, `health`, `probe`, `paths` | runtime local `tmux` |
| `doctor_openclaw` | `sanity`, `quick`, `deep`, `repair-safe`, `generate-token`, `validate`, `health`, `probe`, `logs`, `status`, `dashboard` | diagnostic + action controlee |
| `evidence_openclaw` | `sanity`, `detect-workspace`, `status`, `export-docs`, `print-doc-prompt`, `evidence-dir`, `show-files` | export de preuves |
| `menu_openclaw` | `sanity`, `status`, `list-menus`, `list-menus-numbered`, `open-menu`, `useful`, `paths` | hub de navigation |

## Couplages inter-modules observes
- `evidence_openclaw` appelle :
  - `cmd-doctor_openclaw status`
  - `cmd-doctor_openclaw quick`
  - `cmd-configure_openclaw status`
- `menu_openclaw` depend de la registry de `install_module_openclaw`
- le reste des references `cmd-*` / `menu-*` est surtout local aux scripts `install_shortcuts.sh` et aux docs de chaque module

## Ecarts de conventions observes
- shortcut hub ambigue :
  - `menu-menu_openclaw`
  - `cmd-menu_openclaw`
  - `menu-openclaw`
  - `cmd-openclaw`
- installation des shortcuts non uniforme :
  - `sudo tee /usr/local/bin/...` sur la plupart des modules
  - `ln -sf` vers `BIN_DIR` sur `model_provider_openclaw`
- `paths` n'est pas expose partout
- `status` existe partout, mais sa charge informative varie fortement
- certains verbes write-scope eleve ne sont pas encore formellement distingues dans une convention commune :
  - `install`
  - `apply`
  - `set`
  - `unset`
  - `start`
  - `stop`
  - `repair-safe`
  - `generate-token`

## Decision Step 01
- oui a une convention de famille, mais pas a une uniformisation aveugle
- base de convergence proposee pour Step 03 :
  - `sanity` obligatoire
  - `status` obligatoire
  - `paths` recommande pour les modules qui pilotent des chemins ou etats locaux
  - verbes `show-*` / `export-*` / `list-*` reserves aux modules de lecture, policy, evidence et hub
  - verbes write-scope eleve gardes explicites et non masques
- anomalie a arbitrer plus tard :
  - double naming du hub `menu_openclaw`

## Risques a eviter
- normaliser les verbes sans distinguer lecture et action
- aligner les shortcuts en cassant les usages locaux existants sans audit
- absorber `doctor` dans `gateway`
- absorber `configure` dans `openclaw_config_modulaire`

## Point de reprise
Step suivant :
- produire le runbook unique de suite
- puis seulement proposer les conventions de wrappers de famille

## RISKS

- À qualifier.
