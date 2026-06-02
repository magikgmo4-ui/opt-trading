# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour student (Activé)
python3 scripts/env/validate_credentials.py --machine student --job deskpro_analysis

# Pour fantome (Activé)
python3 scripts/env/validate_credentials.py --machine fantome --job deskpro_analysis
```

## Résolution
Le resolver chargera les variables DeskPro uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
