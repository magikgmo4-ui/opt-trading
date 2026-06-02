# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour admin-trading (Activé)
python3 scripts/env/validate_credentials.py --machine admin-trading --job tv_webhook_receive

# Pour fantome (Éligible mais désactivé)
python3 scripts/env/validate_credentials.py --machine fantome --job tv_webhook_receive
```

## Résolution
Le resolver chargera `TV_WEBHOOK_SECRET` uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
