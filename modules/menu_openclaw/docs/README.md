# menu_openclaw

Hub operateur compact pour relier les modules OpenClaw deja presents dans `opt-trading` sans melanger documentation et runtime.

## But

- donner un point d entree unique ;
- lister les menus OpenClaw declares dans la registry ;
- ouvrir rapidement un module par `module_id` ;
- servir de point d appui pour la sequence standard `GO_OPENCLAW_CHAIN_03`.

## Rappels de perimetre

- `opt-trading` reste le repo canonique de continuite ;
- `openclaw` reste doc/gouvernance-only ;
- `menu_openclaw` ne remplace pas les modules ; il sert de hub de navigation et de reprise.

## Chaine standard visee

1. `install_module_openclaw`
2. `openclaw_config_modulaire`
3. `gateway_openclaw`
4. `configure_openclaw`
5. `doctor_openclaw`
6. `evidence_openclaw`

## Commandes rapides

```bash
bash modules/menu_openclaw/scripts/sanity.sh
bash modules/menu_openclaw/scripts/cmd.sh status
bash modules/menu_openclaw/scripts/cmd.sh list-menus
bash modules/menu_openclaw/scripts/cmd.sh open-menu gateway_openclaw
bash modules/menu_openclaw/scripts/cmd.sh open-menu doctor_openclaw
bash modules/menu_openclaw/scripts/cmd.sh open-menu evidence_openclaw
```

## Point de reprise

Pour la chaine OpenClaw durable, voir `GO_OPENCLAW_CHAIN_03.md` dans ce dossier.
