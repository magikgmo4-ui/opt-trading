# Registry Router

**Module**: `registry_router`  
**Role**: Landing Menu / Router pour les registres centraux.  
**Target**: `admin-trading`, `operator`

## Description
Ce module sert de point d'entrée unique pour naviguer vers les différents lecteurs de registres (Meta, Machines, Modules, UI, Wrappers).
Il ne contient pas de logique de lecture directe, mais route les commandes vers les modules spécialisés.

## Usage

### CLI
```bash
./scripts/cmd.sh status
./scripts/cmd.sh show-entries
./scripts/cmd.sh open-meta
./scripts/cmd.sh open-machines
./scripts/cmd.sh open-modules
./scripts/cmd.sh open-ui
./scripts/cmd.sh open-wrappers
```

### Menu Interactif
```bash
./scripts/menu.sh
```

## Dépendances
- Modules lecteurs existants (`modules/*_reader`)
