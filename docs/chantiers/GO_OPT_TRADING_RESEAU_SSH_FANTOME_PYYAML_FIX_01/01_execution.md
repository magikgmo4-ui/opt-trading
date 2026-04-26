---
doc_id: GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01_EXECUTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - fantome
  - pyyaml
  - execution
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/status/reseau_ssh_canonique.md
---

# Execution

## Diagnostic

Le script nested `reseau_ssh_step2/scripts/reseau_ssh_cmd.sh` parse `inventory.yaml` via :
- `python3`
- `yaml.safe_load`

Sur `fantome`, le diagnostic initial etait :
- `/usr/bin/python3`
- `ModuleNotFoundError: No module named 'yaml'`

## Correctif applique

Installation systeme sur `fantome` :

```bash
sudo apt-get update
sudo apt-get install -y python3-yaml
```

Package confirme :
- `python3-yaml 6.0-3+b2`

## Validation

- `python3 -c "import yaml"` : OK
- `sanity-reseau_ssh` : OK sans `RESEAU_SSH_SKIP_DEEP_SANITY`

## Note d'hygiene

`apt` a emis un warning de sources dupliquees dans `/etc/apt/sources.list` sur `fantome`.

Ce warning n'a pas bloque l'installation et reste hors scope `reseau_ssh`.

## Target
1 module canonique par famille.
