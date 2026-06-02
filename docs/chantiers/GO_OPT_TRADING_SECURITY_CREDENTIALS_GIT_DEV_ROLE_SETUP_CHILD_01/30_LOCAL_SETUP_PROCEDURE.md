# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/git_dev.env
```

Contenu attendu :
```env
GH_TOKEN=XXXXX_VOTRE_TOKEN_GH_ICI_XXXXX
GIT_AUTHOR_NAME="Votre Nom"
GIT_AUTHOR_EMAIL="votre.email@exemple.com"
```

## 3. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/git_dev.env
```
