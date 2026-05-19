# UI Registry MSI

**Module**: `ui_registry_msi`  
**Type**: Registry / Indexation  
**Status**: V1 (Local/JSON)  
**Target**: `msi_db_layer` (Principal), `admin_trading` (Secondaire)

## Description
Ce module est la **source de vérité (Registry)** pour toutes les surfaces UI/UX du système Desk Pro, avec une priorité "MSI-first".
Il ne s'agit pas du dashboard final, mais de l'index structuré qui permet de savoir :
- Quelle UI est disponible ?
- Sur quelle machine (`msi_db_layer`, `admin_trading`, `student`) ?
- Dans quelle catégorie (`dev`, `probabilites_trades`, `screenshots`) ?
- Quel module la fournit ?

## Objectifs
1. **Centraliser** la connaissance des points d'entrée UI.
2. **Exposer** clairement les outils disponibles pour l'opérateur MSI.
3. **Préparer** le terrain pour un dashboard unifié futur.

## Structure
Le module est autonome et fonctionne en priorité avec le registre central (`registry/ui_surfaces_registry.yaml`), ou en fallback sur sa base locale (`config/ui_registry_seed.json`).

```
modules/ui_registry_msi/
├── app/
│   └── ui_registry_msi.py       # Logique de lecture/filtrage/export
├── config/
│   └── ui_registry_seed.json    # Base locale (Fallback)
├── scripts/
│   ├── cmd.sh                   # Wrapper CLI
│   ├── menu.sh                  # Interface opérateur interactive
│   └── sanity_check.sh          # Tests de santé
└── README.md
```

## Catégories UI
- `ui/index/modules`: Navigation générale, hubs, menus racines.
- `ui/dev`: Outils de développement, logs, debug, performance.
- `ui/probabilites_trades`: Moteurs de décision, scoring, analyse de marché.
- `ui/screenshots_analyses_passees`: Historique, retention, vision.

## Machines Cibles
- `msi_db_layer`: Interface opérateur principale (Monitoring, Dashboard).
- `admin_trading`: Backend d'exécution et orchestration.
- `student`: IA complémentaire et analyse LLM.
- `dell_cursor_ai`: Environnement de développement.

## Commandes Principales

### Via Wrapper (Linux/Git Bash)
```bash
# Statut du registre
./scripts/cmd.sh status

# Liste simple des surfaces
./scripts/cmd.sh list

# Vue groupée par machine
./scripts/cmd.sh show-machines

# Vue groupée par catégorie
./scripts/cmd.sh show-categories

# Vue filtrée MSI (db-layer)
./scripts/cmd.sh show-msi

# Exports
./scripts/cmd.sh export-json
./scripts/cmd.sh export-md

# Menu Interactif
./scripts/menu.sh
```

### Via Python (Windows Powershell)
```powershell
python -m modules.ui_registry_msi.app.ui_registry_msi status
python -m modules.ui_registry_msi.app.ui_registry_msi show-msi
```
