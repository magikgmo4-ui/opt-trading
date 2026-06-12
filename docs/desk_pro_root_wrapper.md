# Desk Pro Root Wrapper (Legacy Compat)

Ce document décrit une couche legacy de compatibilité autour des scripts root Desk Pro. Elle ne doit plus être promue comme point d'entrée canonique.

## Statut Canonique
- **Opérateur** : `menu-ops_menu_hub`
- **Admin / debug** : `scripts/admin_trading/desk_pro_cmd.sh` ou `cmd-desk_pro_runner`
- **Scripts root `desk_pro_root_*`** : **LEGACY / COMPAT** uniquement

## Legacy Commands

### Linux / Bash
Located in `scripts/`:

```bash
# Check status
./scripts/desk_pro_root_cmd.sh status

# Run full pipeline
./scripts/desk_pro_root_cmd.sh run

# Run and show dashboard
./scripts/desk_pro_root_cmd.sh run-and-show

# Show latest dashboard
./scripts/desk_pro_root_cmd.sh dashboard-latest

# Exports
./scripts/desk_pro_root_cmd.sh export-json-latest
./scripts/desk_pro_root_cmd.sh export-html-latest

# Interactive Menu
./scripts/desk_pro_root_menu.sh
```

### Windows / PowerShell
Located in `scripts/`:

```powershell
# Check status
.\scripts\desk_pro_root.ps1 status

# Run full pipeline
.\scripts\desk_pro_root.ps1 run

# Run and show dashboard
.\scripts\desk_pro_root.ps1 run-and-show

# Show latest dashboard
.\scripts\desk_pro_root.ps1 dashboard-latest

# Exports
.\scripts\desk_pro_root.ps1 export-json-latest
.\scripts\desk_pro_root.ps1 export-html-latest
```

## Règle d'Usage
Ces scripts peuvent rester utilisés pour compatibilité locale, mais les nouvelles procédures doivent référencer `menu-ops_menu_hub`, `scripts/admin_trading/desk_pro_cmd.sh` ou `cmd-desk_pro_runner` selon le rôle.

## Integration
- **Delegates to**: `modules.desk_pro_runner.app.desk_pro_runner`
- **Orchestrates**: `desk_pro_orchestrator` (via runner)
- **Visualizes**: `desk_pro_dashboard` (via runner)

## RISKS

- À qualifier.
