# Wrappers Registry Reader

**Module**: `wrappers_registry_reader`  
**Role**: Reader for `registry/wrappers_registry.yaml`  
**Target**: `admin-trading`, `msi_db_layer`

## Description
Ce module fournit un accès en lecture seule à la définition des wrappers système (familles standard : menu, cmd, sanity ; famille exceptionnelle admise : entrypoint pour certaines surfaces opérateur top-level).
Il consomme le fichier central `registry/wrappers_registry.yaml` et offre une CLI pour l'interroger.

## Usage

### CLI
```bash
./scripts/cmd.sh status
./scripts/cmd.sh list
./scripts/cmd.sh show-families
./scripts/cmd.sh show menu-ui_registry_msi
./scripts/cmd.sh export-json
```

### Menu Interactif
```bash
./scripts/menu.sh
```

## Dépendances
- Python 3
- PyYAML (optionnel, parser interne inclus)
