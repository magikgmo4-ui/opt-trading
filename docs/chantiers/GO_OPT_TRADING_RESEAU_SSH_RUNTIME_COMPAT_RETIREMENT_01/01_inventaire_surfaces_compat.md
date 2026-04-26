---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_INVENTAIRE
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - inventory
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - scripts/reseau_ssh/README.md
  - registry/wrappers_registry.yaml
---

# Inventaire des surfaces de compat

## Surfaces restantes

| Surface | Classe actuelle | Role | Decision de cette passe |
| --- | --- | --- | --- |
| `scripts/reseau_ssh/install_reseau_ssh.sh` | `compat_active_backend_guarded` | reinstalleur legacy des alias courts | patch immediat applique pour delegation au canonique si disponible |
| `scripts/reseau_ssh/reseau_ssh_cmd.sh` | `compat_active_backend` | backend des commandes de compat encore deleguees par la facade canonique | conserver tant que l'absorption ou la depreciation n'est pas faite |
| `scripts/reseau_ssh/reseau_ssh_menu.sh` | `compat_active_backend` | menu compat encore delegue par la facade canonique | conserver tant que l'absorption ou la depreciation n'est pas faite |
| `scripts/reseau_ssh/sanity_reseau_ssh.sh` | `compat_active_backend` | deep sanity backend encore delegue par la facade canonique | conserver tant que le deep sanity n'est pas absorbe ou retire |
| `scripts/reseau_ssh/lib/*` et `templates/*` | `compat_active_backend` | payload backend encore requis par les scripts de compat | conserver tant que les anciens scripts restent appeles |
| `scripts/reseau_ssh_cmd.sh` | `archive_backup` | wrapper racine historique | deplace vers `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/` |
| `scripts/reseau_ssh_menu.sh` | `archive_backup` | wrapper racine historique | deplace vers `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/` |

## Dependances repo-side observees

Etat observe :
- le registre canonique publie deja `cmd/menu/sanity-reseau_ssh` vers `modules/reseau_ssh/scripts/*`
- le registre publie encore les alias suffixes `*_reseau_ssh_step2` comme compat transitoire
- aucune dependance repo-side critique explicite n'a ete relevee vers `scripts/reseau_ssh/install_reseau_ssh.sh`
- les references restantes observees sont principalement :
  - docs de chantier
  - readmes
  - fichiers de la famille `reseau_ssh` elle-meme

## Conclusion d'inventaire

Le premier retrait defensable n'est pas l'archive immediate du dossier.

Le premier retrait defensable est :
- la capacite de republier les alias courts depuis `scripts/reseau_ssh`

Le dossier `scripts/reseau_ssh` reste donc classe :
- `compat_active_backend`

Les wrappers racine sont maintenant classes :
- `archive_backup`

## Target
1 module canonique par famille.
