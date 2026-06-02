# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/llm_cloud.env
```

Contenu attendu :
```env
OPENAI_API_KEY=XXXXX_VOTRE_CLE_OPENAI_ICI_XXXXX
ANTHROPIC_API_KEY=YYYYY_VOTRE_CLE_ANTHROPIC_ICI_YYYYY
GEMINI_API_KEY=ZZZZZ_VOTRE_CLE_GEMINI_ICI_ZZZZZ
```

## 3. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/llm_cloud.env
```
