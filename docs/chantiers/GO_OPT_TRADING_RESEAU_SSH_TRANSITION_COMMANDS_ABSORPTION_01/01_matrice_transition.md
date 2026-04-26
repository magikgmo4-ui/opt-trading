---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01_MATRIX
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TRANSITION_COMMANDS_ABSORPTION_01
status: open
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - transition
  - bootstrap
  - ssh
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/lib/common.sh
---

# Matrice transition restante

| Commande | Backend actuel | Nature | Constat | Classe proposee |
| --- | --- | --- | --- | --- |
| `bootstrap` | `scripts/reseau_ssh/reseau_ssh_cmd.sh` | bootstrap systeme + paquets + UFW + Fail2Ban | utile, destructive moderee, appelle des helpers shell simples | `absorb_dans_canonique` |
| `ssh-hardening-safe` | `scripts/reseau_ssh/reseau_ssh_cmd.sh` | hardening SSH safe | utile, bornable, depend de `backup_file` et `need_root` | `absorb_dans_canonique` |
| `ssh-lockdown` | `scripts/reseau_ssh/reseau_ssh_cmd.sh` | hardening SSH fort | utile mais plus risquee, precondition `authorized_keys` | `absorb_dans_canonique` |

## Constat technique

Les trois commandes :
- n'existent pas dans l'implementation nested `step2`
- n'existent pas dans la facade canonique autrement qu'en delegation
- s'appuient sur `scripts/reseau_ssh/lib/common.sh`

Le menu canonique `modules/reseau_ssh/scripts/menu.sh` expose encore un menu compat entier :
- `Operator compat menu (scripts/reseau_ssh)`

## Lecture actuelle

La famille `reseau_ssh` ne peut pas etre consideree pleinement consolidee tant que ces commandes restent :
- utiles
- publiees via le canonique
- mais implementees hors du canonique

## Target
1 module canonique par famille.
