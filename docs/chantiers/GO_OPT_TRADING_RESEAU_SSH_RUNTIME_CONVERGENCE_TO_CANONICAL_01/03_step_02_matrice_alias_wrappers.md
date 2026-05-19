---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_STEP_02_ALIAS_WRAPPERS
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - aliases
  - wrappers
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - scripts/reseau_ssh/install_reseau_ssh.sh
  - modules/reseau_ssh/scripts/install_shortcuts.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/install_shortcuts_linux.sh
  - modules/reseau_ssh_step1b/scripts/install_shortcuts.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/install_shortcuts_linux.sh
  - registry/wrappers_registry.yaml
---

# Step 02 - matrice alias et wrappers

## Publication observee

| Surface | Installeur | Alias publies | Cible publiee |
| --- | --- | --- | --- |
| `scripts/reseau_ssh` | `scripts/reseau_ssh/install_reseau_ssh.sh` | `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | `/opt/trading/scripts/reseau_ssh/reseau_ssh_menu.sh`, `/opt/trading/scripts/reseau_ssh/reseau_ssh_cmd.sh`, `/opt/trading/scripts/reseau_ssh/sanity_reseau_ssh.sh` |
| `modules/reseau_ssh` top-level | `modules/reseau_ssh/scripts/install_shortcuts.sh` | `menu-reseau_ssh_step2`, `cmd-reseau_ssh_step2`, `sanity-reseau_ssh_step2` | `/opt/trading/modules/reseau_ssh/scripts/menu.sh`, `/opt/trading/modules/reseau_ssh/scripts/cmd.sh`, `/opt/trading/modules/reseau_ssh/scripts/sanity_check.sh` |
| `modules/reseau_ssh` nested | `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/install_shortcuts_linux.sh` | `menu-reseau_ssh_step2`, `cmd-reseau_ssh_step2`, `sanity-reseau_ssh_step2` | `/opt/trading/modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_menu.sh`, `/opt/trading/modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh`, `/opt/trading/modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/sanity_check.sh` |
| `modules/reseau_ssh_step1b` top-level | `modules/reseau_ssh_step1b/scripts/install_shortcuts.sh` | `menu-reseau_ssh_step1b`, `cmd-reseau_ssh_step1b`, `sanity-reseau_ssh_step1b` | `/opt/trading/modules/reseau_ssh_step1b/scripts/menu.sh`, `/opt/trading/modules/reseau_ssh_step1b/scripts/cmd.sh`, `/opt/trading/modules/reseau_ssh_step1b/scripts/sanity_check.sh` |
| `modules/reseau_ssh_step1b` nested legacy | `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/install_shortcuts_linux.sh` | `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | copie `step1b` vers `/opt/trading/scripts/reseau_ssh_*.sh`, puis publication des alias courts |

## Ecarts critiques

### 1. Les alias courts restent encore publies hors du canonique
Le registre cible maintenant `reseau_ssh`.

Mais la publication machine-side observee des alias courts reste encore sur `scripts/reseau_ssh`.

### 2. Le suffixe `step2` a encore deux installateurs
Le compat `reseau_ssh_step2` existe :
- depuis la facade top-level `modules/reseau_ssh/scripts/*`
- depuis l'implementation nested `reseau_ssh_step2`

Cette dualite doit rester transitoire.

### 3. `step1b` garde un ancien publicateur des alias courts
L'installeur nested legacy de `step1b` ne doit plus servir de trajectoire cible.

### 4. Le registre est pret
`registry/wrappers_registry.yaml` porte maintenant :
- `cmd/menu/sanity-reseau_ssh`
- `cmd/menu/sanity-reseau_ssh_step2`

Le manque n'est donc plus declaratif.

Le manque est machine-side.

## Target
1 module canonique par famille.
