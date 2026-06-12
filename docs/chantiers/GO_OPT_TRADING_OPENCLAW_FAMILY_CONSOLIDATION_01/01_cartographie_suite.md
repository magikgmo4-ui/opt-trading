---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_CARTOGRAPHIE
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - openclaw
  - inventory
  - entrypoints
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/00_cadrage.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
  - modules/install_module_openclaw/README.md
  - modules/model_provider_openclaw/README.md
  - modules/openclaw_config_modulaire/README.md
  - modules/configure_openclaw/README.md
  - modules/gateway_openclaw/README.md
  - modules/doctor_openclaw/README.md
  - modules/evidence_openclaw/README.md
  - modules/menu_openclaw/README.md
---

# Cartographie de suite `OpenClaw`

## Carte retenue
| Couche | Module | Role | Verbes/entree principale | Ecriture potentielle |
| --- | --- | --- | --- | --- |
| hub | `menu_openclaw` | federation, listing, navigation | `status`, `list-menus`, `open-menu`, `useful`, `paths` | faible, sauf installation des shortcuts |
| installation | `install_module_openclaw` | copie locale de modules declares | `list`, `status`, `install`, `paths` | forte, copie vers `/opt/trading` |
| policy provider/model | `model_provider_openclaw` | lecture policy et export machine-readable | `status`, `show-agent`, `export-json` | lecture seule |
| config structurelle | `openclaw_config_modulaire` | backup/apply/rollback de la config | `status`, `backup`, `apply`, `rollback`, `paths` | forte, ecrit `~/.openclaw/*` |
| config live | `configure_openclaw` | facade operateur sur la config active | `status`, `validate`, `wizard`, `agents-*`, `get/set/unset` | moyenne a forte |
| runtime local | `gateway_openclaw` | pilotage runtime local | `status`, `start`, `stop`, `logs`, `attach`, `health`, `probe`, `paths` | forte, agit sur session runtime |
| diagnostic | `doctor_openclaw` | diagnostic, verification, repair-safe | `quick`, `deep`, `repair-safe`, `generate-token`, `health`, `probe`, `logs` | moyenne a forte |
| preuves | `evidence_openclaw` | export de preuves et prompt documentaire | `status`, `export-docs`, `print-doc-prompt`, `show-files` | ecrit sous `docs_evidence/` |

## Graphe de dependances observe
- `menu_openclaw` lit la registry de `install_module_openclaw` pour decouvrir les modules autorises
- `install_module_openclaw` lit `app/modules_registry.json`
- `gateway_openclaw` depend de `app/gateway_env.sh`
- `evidence_openclaw` depend explicitement de `doctor_openclaw` et `configure_openclaw` si les shortcuts `cmd-*` sont installes

## Invariants de lecture
- la suite reste locale a `db-layer`
- `model_provider_openclaw` ne doit pas etre absorbe dans la config machine
- `openclaw_config_modulaire` reste distinct de `configure_openclaw`
- `doctor_openclaw` reste distinct de `gateway_openclaw`
- `evidence_openclaw` reste hors runtime
- `menu_openclaw` reste un hub, pas un megamodule

## Ecarts de structure observes
- la suite est homogene sur les fichiers de base `cmd/menu/sanity`, mais pas sur les verbes
- la suite n'est pas homogene sur les shortcuts :
  - la plupart utilisent `sudo tee /usr/local/bin/...`
  - `model_provider_openclaw` utilise `ln -sf` vers un `BIN_DIR`
- le hub expose une double nomenclature :
  - `menu-menu_openclaw` / `cmd-menu_openclaw`
  - `menu-openclaw` / `cmd-openclaw`
- `paths` n'est pas expose partout
- `sanity` et `status` sont les seuls quasi-invariants verifiables a ce stade

## Decision de baseline
- oui a une cartographie unique de suite
- oui a une harmonisation par conventions de wrappers
- non a une fusion physique des modules dans ce lot
- non a une normalisation aveugle des verbes sans regarder le write-scope de chaque module

## Point de reprise
Basculer sur `03_step_01_matrice_wrappers.md` pour la matrice exacte des verbes et des ecarts de conventions.

## RISKS

- À qualifier.
