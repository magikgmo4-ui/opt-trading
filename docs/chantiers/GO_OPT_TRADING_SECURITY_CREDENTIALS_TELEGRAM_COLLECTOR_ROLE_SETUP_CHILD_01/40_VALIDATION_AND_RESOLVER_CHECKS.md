# Validation and Resolver Checks

Les scripts canoniques ont été mis à jour pour supporter le modèle d'autorisation à trois niveaux.

## Validation des Statuts

### Cas 1 : AUTHORIZED_ACTIVE (`fantome`)
```bash
python3 scripts/env/validate_credentials.py --machine fantome --job telegram_collect_channel
```
**Résultat attendu** : `OK` (ou `MISSING` si les secrets ne sont pas en place localement).

### Cas 2 : ELIGIBLE_DISABLED_BY_DEFAULT (`admin-trading`)
```bash
python3 scripts/env/validate_credentials.py --machine admin-trading --job telegram_collect_channel
```
**Résultat attendu** : `Status: ELIGIBLE_DISABLED (Role 'telegram_collector' is eligible but not active on 'admin-trading')`.

### Cas 3 : FORBIDDEN (`student`)
```bash
python3 scripts/env/validate_credentials.py --machine student --job telegram_collect_channel
```
**Résultat attendu** : `Status: DENIED (Machine 'student' is forbidden from role 'telegram_collector')`.

## Résolution
Le resolver refusera de charger les credentials si le rôle n'est pas `AUTHORIZED_ACTIVE`.
