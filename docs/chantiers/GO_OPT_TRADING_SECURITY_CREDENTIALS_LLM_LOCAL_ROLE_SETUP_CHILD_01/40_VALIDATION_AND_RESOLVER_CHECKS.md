# Validation and Resolver Checks

## Validation de l'Authorization
```bash
# Pour student (Activé)
python3 scripts/env/validate_credentials.py --machine student --job llm_local_inference

# Pour fantome (Activé)
python3 scripts/env/validate_credentials.py --machine fantome --job llm_local_inference
```

## Résolution
Le resolver chargera l'URL Ollama uniquement sur les machines où le rôle est `AUTHORIZED_ACTIVE`.
