---
doc_id: GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01_STEP_04_DUPLICATIONS
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
  - duplication
  - wrappers
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/05_step_03_conventions_wrappers.md
---

# Step 04 - audit des duplications

## Statut
Complete.

## Objet
Verifier si la suite `OpenClaw` justifie une petite mutualisation shell/doc a faible risque.

## Verifications utilisees
- hash SHA256 des scripts `*.sh` sur les `8` modules `OpenClaw`
- comptage de lignes des scripts `*.sh`
- relecture ciblee des `install_shortcuts.sh`

## Constat principal
Il n'existe pas de duplication litterale evidente a mutualiser immediatement :
- les hashes des `cmd.sh` sont tous differents
- les hashes des `menu.sh` sont tous differents
- les hashes des `sanity.sh` sont tous differents
- les hashes des `install_shortcuts.sh` sont tous differents

Conclusion :
- la duplication est surtout structurelle
- elle n'est pas encore une duplication texte-a-texte qui justifierait un helper commun dans ce lot

## Zones de proximite reelles

### 1. `install_shortcuts.sh`
Pattern commun observe :
- creation de shortcuts `menu-*` / `cmd-*`
- sortie lisible de fin

Ecarts observes :
- la plupart utilisent `sudo tee /usr/local/bin/...`
- `model_provider_openclaw` utilise `BIN_DIR` + `ln -sf`
- `menu_openclaw` installe `4` aliases, dont les aliases famille `menu-openclaw` / `cmd-openclaw`

### 2. `cmd.sh`
Pattern commun observe :
- `set -euo pipefail`
- `case "${1:-help}" in`
- dispatch de verbes shell explicites

Ecarts observes :
- ecarts de role trop forts pour mutualiser sans sur-generalisation
- write-scope heterogene
- certains modules sont surtout lecture/policy, d'autres pilotent du runtime

### 3. `menu.sh` et `sanity.sh`
Pattern commun observe :
- surfaces standard de la famille

Decision :
- aucune preuve de duplication assez stable pour extraire un helper commun maintenant

## Decision Step 04
- non a une mutualisation shell immediate
- oui a un futur petit patch cible si un vrai irritant operatoire est confirme
- le meilleur candidat futur n'est pas un helper generique
- le meilleur candidat futur est un micro-lot sur :
  - la doc des aliases du hub
  - ou l'harmonisation des `install_shortcuts.sh`

## Risques a eviter
- creer un helper commun prematurement et figer une abstraction trop large
- casser la compatibilite locale de `model_provider_openclaw`
- toucher aux write-scopes de `gateway`, `doctor`, `configure` ou `openclaw_config_modulaire` pour gagner seulement de la symetrie

## Point de reprise
Step suivant :
- Step 05
- decider si le sous-lot doit :
  - rester doc-only et se fermer
  - ou ouvrir un mini patch shell tres cible

## RISKS

- À qualifier.
