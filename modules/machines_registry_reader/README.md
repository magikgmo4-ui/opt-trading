# Machines Registry Reader

**Module**: `machines_registry_reader`  
**Role**: Reader for `registry/machines_registry.yaml`  
**Target**: `admin-trading`, `msi_db_layer`

## Description
Ce module fournit un accès en lecture seule à la définition des machines du système Desk Pro.
Il consomme le fichier central `registry/machines_registry.yaml` et offre une CLI pour l'interroger.

## Usage

### CLI
```bash
./scripts/cmd.sh status
./scripts/cmd.sh list
./scripts/cmd.sh show-roles
./scripts/cmd.sh show admin_trading
./scripts/cmd.sh export-json
```

### Menu Interactif
```bash
./scripts/menu.sh
```

## Dépendances
- Python 3
- PyYAML (optionnel, parser interne inclus)
