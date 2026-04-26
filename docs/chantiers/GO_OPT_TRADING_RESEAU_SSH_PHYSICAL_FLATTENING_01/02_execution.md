---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01_EXECUTION
doc_type: chantier_execution
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01
status: closed
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - reseau_ssh
  - execution
surface: modules
source_kind: canonical
updated_at: 2026-04-26
---

# Execution

- ancien chemin interne `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2` remplacé par `modules/reseau_ssh/wireguard/`
- nouvelle logique WireGuard top-level : `modules/reseau_ssh/scripts/_reseau_ssh_wireguard.sh`
- façade top-level recâblée : `cmd.sh`, `menu.sh`, `sanity_check.sh`, `_reseau_ssh_common.sh`
- payload baseline complété : `modules/reseau_ssh/baseline/README.md`, `PLAN.md`, `inventory.yaml`, `ssh_config.windows`, `windows/*`
- scripts internes `wireguard/scripts/*` retirés

## Validation repo-side

- `bash -n` : `modules/reseau_ssh/scripts/_reseau_ssh_wireguard.sh`, `_reseau_ssh_common.sh`, `_reseau_ssh_baseline.sh`, `cmd.sh`, `menu.sh`, `sanity_check.sh` -> `SYNTAX_OK`
- `cmd-reseau_ssh info` : expose `wireguard_dir=.../modules/reseau_ssh/wireguard` et `baseline_dir=.../modules/reseau_ssh/baseline`
- `cmd-reseau_ssh baseline-show-hosts` : retourne le bloc hosts canonique
- `cmd-reseau_ssh help` : expose uniquement la façade canonique top-level

## Validation machine-side

- `db-layer` : `module=yes`, `wireguard=yes`, `baseline=yes`, `nested_modules=no`, `wireguard_scripts=no`, `sanity_result=PASS`
- `admin-trading` : `module=yes`, `wireguard=yes`, `baseline=yes`, `nested_modules=no`, `wireguard_scripts=no`, `sanity_result=PASS`
- `student` : `module=yes`, `wireguard=yes`, `baseline=yes`, `nested_modules=no`, `wireguard_scripts=no`, `sanity_result=PASS`
- `fantome` : `module=yes`, `wireguard=yes`, `baseline=yes`, `nested_modules=no`, `wireguard_scripts=no`, `sanity_result=PASS`

## Target
1 module canonique par famille.
