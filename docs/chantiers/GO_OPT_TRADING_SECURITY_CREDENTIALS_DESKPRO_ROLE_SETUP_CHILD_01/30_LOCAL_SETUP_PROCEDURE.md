# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/deskpro_user.env
```

Contenu attendu :
```env
DESKPRO_API_URL=http://localhost:8000
DESKPRO_API_KEY=XXXXX_VOTRE_CLE_DESKPRO_ICI_XXXXX
DESKPRO_SNAPSHOT_DIR=/home/fantome/opt-trading-clean/data/snapshots
DESKPRO_GUI_ENABLED=1
```

## 3. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/deskpro_user.env
```
