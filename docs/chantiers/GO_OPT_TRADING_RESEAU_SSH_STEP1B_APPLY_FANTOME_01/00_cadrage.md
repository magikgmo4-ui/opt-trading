---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_APPLY_FANTOME_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_APPLY_FANTOME_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - fantome
  - db-layer
  - runtime
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/apply_linux.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/templates/hosts.block
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/templates/ssh_config.linux
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/06_step_05_runbook_fantome.md
---

# GO_OPT_TRADING_RESEAU_SSH_STEP1B_APPLY_FANTOME_01

## Objet

Appliquer `reseau_ssh_step1b` sur `db-layer` et `fantome` après le merge PR #625 qui :
- corrige les IPs `192.168.16.x` → `192.168.0.x` (LAN actif)
- ajoute `fantome` dans l'inventaire, `hosts.block` et `ssh_config.linux`

## Cible

Sur chaque machine :
- `/etc/hosts` contient le bloc `reseau_ssh` avec les IPs actives (`192.168.0.x`) et `fantome`
- `~/.ssh/config` contient les alias canoniques avec les IPs actives et `Host fantome`

## Portée

- `db-layer` — refresh (IPs stales + ajout alias fantome)
- `fantome` — première application step1b

## Hors-scope

- WireGuard step2 (phase séparée)
- SSHFS `/shared` mount (dépend de ce GO)
- `admin-trading`, `student` (non ciblés dans ce lot)

## Prérequis

- PR #625 mergée dans `sot/mainline` ✓
- Accès SSH opérateur vers `db-layer` et `fantome`
- `git pull` effectué sur les deux machines avant exécution

## IPs de référence

| Machine     | LAN actif      | WireGuard     |
|-------------|---------------|---------------|
| admin-trading | 192.168.0.111 | 10.66.66.1   |
| db-layer    | 192.168.0.100  | 10.66.66.2   |
| student     | 192.168.0.142  | 10.66.66.3   |
| cursor-ai   | 192.168.0.177  | 10.66.66.4   |
| fantome     | 192.168.0.191  | 10.66.66.5   |

## Target

Baseline SSH cohérente sur toutes les machines Linux de la flotte.
