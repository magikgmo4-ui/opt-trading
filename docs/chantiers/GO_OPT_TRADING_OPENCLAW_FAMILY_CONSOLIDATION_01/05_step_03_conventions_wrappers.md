---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_STEP_03_CONVENTIONS
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
  - conventions
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/04_step_02_runbook_de_suite.md
  - modules/menu_openclaw/scripts/install_shortcuts.sh
  - modules/model_provider_openclaw/scripts/install_shortcuts.sh
---

# Step 03 - conventions de wrappers `OpenClaw`

## Statut
Complete.

## Objet
Figer une convention de wrappers commune a la suite `OpenClaw`, sans patch runtime immediat.

## Decision generale
La famille `OpenClaw` n'a pas besoin d'une uniformisation totale.
Elle a besoin d'une convention lisible, stable et compatible avec les write-scopes differents des modules.

## Conventions retenues

### 1. Noyau obligatoire
Chaque module de la suite doit conserver :
- `scripts/cmd.sh`
- `scripts/menu.sh`
- `scripts/sanity.sh`
- un wrapper `install_shortcuts.sh`

### 2. Verbes de base
Les verbes minimaux attendus par famille sont :
- `sanity`
- `status`

Exception acceptee :
- `status` peut etre plus ou moins riche selon le role du module
- `paths` n'est pas obligatoire si un verbe plus precis existe deja, par exemple :
  - `config-file`
  - `evidence-dir`

### 3. Verbes par role
- hub :
  - `list-*`
  - `open-*`
  - `useful`
  - `paths`
- policy / lecture :
  - `show-*`
  - `export-*`
  - pas de write implicite
- config structurelle :
  - `backup`
  - `apply`
  - `rollback`
  - `validate`
- config live :
  - `get`
  - `set`
  - `unset`
  - `agents-*`
- runtime :
  - `start`
  - `stop`
  - `logs`
  - `attach`
  - `health`
  - `probe`
- diagnostic :
  - `quick`
  - `deep`
  - `repair-safe`
  - `generate-token`
- evidence :
  - `export-docs`
  - `print-doc-prompt`
  - `show-files`

### 4. Verbos a write-scope eleve
Les verbes suivants doivent rester explicites et jamais etre caches derriere un alias ambigu :
- `install`
- `apply`
- `rollback`
- `set`
- `unset`
- `start`
- `stop`
- `repair-safe`
- `generate-token`

### 5. Naming des shortcuts
Convention cible :
- `menu-<module_id>`
- `cmd-<module_id>`

Exception de famille retenue pour le hub :
- alias principal de reprise :
  - `menu-openclaw`
  - `cmd-openclaw`
- alias de compatibilite toleres a ce stade :
  - `menu-menu_openclaw`
  - `cmd-menu_openclaw`

Decision :
- le hub doit etre documente avec `menu-openclaw` / `cmd-openclaw` comme entree principale
- les alias `menu-menu_openclaw` / `cmd-menu_openclaw` ne doivent plus etre la surface de reprise recommandee

### 6. Installation des shortcuts
Convergence cible plus tard :
- un mode d'installation unique
- un `BIN_DIR` configurable
- creation idempotente
- sortie de statut lisible

Decision presente :
- ne pas normaliser le mecanisme maintenant
- auditer d'abord la duplication et la compatibilite locale en Step 04

## Ce qui n'est pas force
- pas d'ajout automatique de `paths` a tous les modules
- pas de suppression immediate des alias existants
- pas de fusion des verbes `doctor` avec ceux du `gateway`
- pas de fusion entre `configure_openclaw` et `openclaw_config_modulaire`

## Resultat Step 03
- la famille a maintenant une convention commune
- le prochain audit peut comparer les scripts a partir d'une cible explicite
- un futur patch shell pourra rester petit et borne s'il devient necessaire

## Point de reprise
Step suivant :
- auditer la duplication `install_shortcuts.sh`, `cmd.sh`, `menu.sh`, `sanity.sh`
- verifier si une petite mutualisation sans risque est reellement possible

## RISKS

- À qualifier.
