# Modules Registry Reader

**Module**: `modules_registry_reader`  
**Role**: Reader for `registry/modules_registry.yaml`  
**Target**: `admin-trading`, `msi_db_layer`

## Description
Ce module fournit un accès en lecture seule à la définition des modules fonctionnels du système Desk Pro.
Il consomme le fichier central `registry/modules_registry.yaml` et offre une CLI pour l'interroger.

## Usage

### CLI
```bash
./scripts/cmd.sh status
./scripts/cmd.sh list
./scripts/cmd.sh show-domains
./scripts/cmd.sh show desk_pro_runner
./scripts/cmd.sh export-json
```

### Menu Interactif
```bash
./scripts/menu.sh
```

## Dépendances
- Python 3
- PyYAML (optionnel, parser interne inclus)
