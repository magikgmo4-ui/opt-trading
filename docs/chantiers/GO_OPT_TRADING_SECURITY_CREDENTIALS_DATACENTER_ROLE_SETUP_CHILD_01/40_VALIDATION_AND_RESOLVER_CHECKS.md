# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour admin-trading (Activé)
python3 scripts/env/validate_credentials.py --machine admin-trading --job db_maintenance

# Pour fantome (Éligible mais désactivé)
python3 scripts/env/validate_credentials.py --machine fantome --job db_maintenance
```

## Résolution
Le resolver chargera les variables `DB_HOST`, `DB_USER` et `DB_PASSWORD` uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
