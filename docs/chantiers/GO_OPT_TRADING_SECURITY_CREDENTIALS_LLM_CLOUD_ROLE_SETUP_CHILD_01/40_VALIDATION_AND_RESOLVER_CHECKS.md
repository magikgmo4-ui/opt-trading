# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour cursor-ai (Activé)
python3 scripts/env/validate_credentials.py --machine cursor-ai --job llm_cloud_inference

# Pour fantome (Éligible mais désactivé)
python3 scripts/env/validate_credentials.py --machine fantome --job llm_cloud_inference
```

## Résolution
Le resolver chargera les clés d'API uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
