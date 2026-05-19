# dev_validation_hub

Module durable de validation développeur pour `opt-trading`.

## Objectif

Donner à une machine de dev-only comme `fantome` une surface bornée et réutilisable pour :
- lire l'état Git courant
- créer et réutiliser un venv local de validation
- installer les dépendances minimales de tests HTTP
- exécuter les tests HTTP isolés `memory_bricks`
- afficher un état pré-PR simple

## Commandes principales

- `bash modules/dev_validation_hub/scripts/sanity.sh`
- `bash modules/dev_validation_hub/scripts/cmd.sh status`
- `bash modules/dev_validation_hub/scripts/cmd.sh pre-pr`
- `bash modules/dev_validation_hub/scripts/cmd.sh ensure-venv`
- `bash modules/dev_validation_hub/scripts/cmd.sh install-http-test-deps`
- `bash modules/dev_validation_hub/scripts/cmd.sh run-memory-bricks-http-tests`
- `bash modules/dev_validation_hub/scripts/cmd.sh trading-lab-status`

## Venv par défaut

Le venv par défaut est :
- `.venv-dev-validation`

Il peut être remplacé en second argument des commandes concernées.

## Exemple de cycle utile sur `fantome`

```bash
bash modules/dev_validation_hub/scripts/sanity.sh
bash modules/dev_validation_hub/scripts/cmd.sh ensure-venv
bash modules/dev_validation_hub/scripts/cmd.sh install-http-test-deps
bash modules/dev_validation_hub/scripts/cmd.sh run-memory-bricks-http-tests
bash modules/dev_validation_hub/scripts/cmd.sh pre-pr
```

## Périmètre volontairement exclu

- aucun service runtime
- aucun rôle réseau ou prod
- aucune mutation de config globale machine
- aucun refactor de modules métier
