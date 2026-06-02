# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour admin-trading (Activé)
python3 scripts/env/validate_credentials.py --machine admin-trading --job sheets_append_rows

# Pour fantome (Éligible mais désactivé)
python3 scripts/env/validate_credentials.py --machine fantome --job sheets_append_rows
```

## Résolution
Le resolver chargera `GOOGLE_SERVICE_ACCOUNT_JSON_PATH` uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
