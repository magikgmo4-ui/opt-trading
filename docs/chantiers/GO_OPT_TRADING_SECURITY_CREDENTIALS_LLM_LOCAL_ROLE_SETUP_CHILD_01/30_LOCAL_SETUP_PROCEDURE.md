# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/llm_local.env
```

Contenu attendu :
```env
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_MODEL_NAME=mistral
```

## 3. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/llm_local.env
```
