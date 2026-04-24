# menu_openclaw

Hub operateur compact pour relier les modules OpenClaw deja presents dans `opt-trading`.

## Role
- offrir un point d'entree unique vers la suite OpenClaw
- lister les menus declares dans la registry OpenClaw
- ouvrir rapidement le menu d'un module par `module_id`
- servir de point d'appui de reprise pour la chaine OpenClaw

## Contenu
- `scripts/cmd.sh` : `status`, `list-menus`, `list-menus-numbered`, `open-menu`, `useful`, `paths`
- `scripts/menu.sh`, `sanity.sh`, `install_shortcuts.sh`
- `scripts/commandes_utiles.sh`
- `docs/README.md`, `RUNBOOK.txt`, `GO_OPENCLAW_*.md`

## Chaine de reference
1. `install_module_openclaw`
2. `openclaw_config_modulaire`
3. `gateway_openclaw`
4. `configure_openclaw`
5. `doctor_openclaw`
6. `evidence_openclaw`

## Statut
- actif
- hub de navigation et de reprise, pas module runtime autonome

## Notes de consolidation
- garder ce module distinct des sous-modules qu'il route
- son role est de federer la suite, pas de dupliquer leurs commandes
