# Collectors convergence scope 01

## Etat de départ
- `modules/derivatives_collector` reste le collector dérivatives canonique.
- `packages/collectors_core` est la fondation partagée des nouveaux collectors.
- `modules/collector_coingecko` et `modules/collector_binance_spot` sont deux providers spot validés.
- La convergence complète n'est pas encore faite.

## Ce qui doit converger
- modèle de config
- modèle lifecycle / status / artifacts
- surface opérateur (cmd / sanity / runbook)
- doctrine collector-family
## Ce qui doit rester séparé
- sémantique métier dérivatives
- logique provider spécifique
- contrats spot vs dérivatives
- toute fausse unification de schéma

## Points non convergés
- `derivatives_collector` n'utilise pas encore `collectors_core`
- config différente (`.env` vs `defaults.toml` + env)
- outputs non harmonisés au niveau famille
- façade opérateur non unifiée

## Ordre recommandé
1. figer doctrine collector-family
2. auditer `derivatives_collector` contre cette doctrine
3. converger d'abord docs / wrappers / artifacts
4. décider plus tard si une migration runtime vaut le coût

## Hors scope
- provider #3
- gros refactor
- intégration LocalCMS
- intégration runtime large opt-trading

## Trigger suivant
GO_COLLECTORS_CONVERGENCE_AUDIT_01
