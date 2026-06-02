# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour fantome (Activé)
python3 scripts/env/validate_credentials.py --machine fantome --job repo_ops

# Pour cursor-ai (Activé)
python3 scripts/env/validate_credentials.py --machine cursor-ai --job repo_ops
```

## Résolution
Le resolver chargera les variables d'identité Git et le token GitHub uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
