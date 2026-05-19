# Registry Meta Reader

**Module**: `registry_meta_reader`  
**Role**: Reader for `registry/meta_index.yaml`  
**Target**: `system-wide`

## Description
Ce module fournit un accès en lecture seule à l'index des registres centraux.
Il consomme le fichier central `registry/meta_index.yaml` et offre une CLI pour l'interroger.

## Usage

### CLI
```bash
./scripts/cmd.sh status
./scripts/cmd.sh list
./scripts/cmd.sh show machines_registry
./scripts/cmd.sh export-json
```

### Menu Interactif
```bash
./scripts/menu.sh
```

## Dépendances
- Python 3
- PyYAML (optionnel, parser interne inclus)
