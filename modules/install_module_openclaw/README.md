# install_module_openclaw

Installeur standard des modules OpenClaw a partir d'un registre local de bundles disponibles.

## Role
- lister les modules OpenClaw installables
- copier le module choisi vers la racine cible
- fournir une experience `cmd/menu/sanity` comme les autres modules du projet

## Contenu
- `app/modules_registry.json` : registre local des modules OpenClaw installables
- `scripts/cmd.sh`, `menu.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`

## Registre local observe
Le registre inclut au moins :
- `openclaw_config_modulaire`
- `install_module_openclaw`
- `model_provider_openclaw`
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `gateway_openclaw`

## Statut
- actif
- point d'entree d'installation de la suite OpenClaw

## Notes de consolidation
- ne pas confondre ce module avec `install_module`
- `install_module_openclaw` est specialise pour la suite OpenClaw et son registre local
