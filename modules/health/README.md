# health

Checks locaux en lecture seule autour du flux webhook, de l'etat router et de la configuration risque.

## Role
- verifier rapidement l'etat minimal des fichiers de runtime
- controler la coherence `router_state` / registry engines / `risk_config`

## Contenu
- `checker.py` : checks Python locaux, sans appel reseau

## Checks observes
- presence et validite JSON de `state/router_state.json`
- presence d'un `active_engine`
- presence du moteur dans `modules.engines.registry`
- presence et lecture de `state/risk_config.json`

## Statut
- actif
- surface de diagnostic locale mince

## Notes de consolidation
- garder cette surface separee du monitoring applicatif
- `health` n'est pas un dashboard ni une couche perf; c'est un check local basique
