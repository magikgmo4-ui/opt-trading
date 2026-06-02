# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour fantome (Activé)
python3 scripts/env/validate_credentials.py --machine fantome --job market_snapshot_fetch

# Pour admin-trading (Activé)
python3 scripts/env/validate_credentials.py --machine admin-trading --job market_snapshot_fetch
```

## Résolution
Le resolver chargera les variables `BINANCE_API_KEY` et `COINGLASS_API_KEY` uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
