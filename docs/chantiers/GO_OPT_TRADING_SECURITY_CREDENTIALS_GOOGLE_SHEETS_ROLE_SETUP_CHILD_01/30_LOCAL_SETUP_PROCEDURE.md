# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
sudo install -d -m 700 /etc/opt-trading/secrets/google
```

## 2. Déploiement du Service Account JSON
Placer le fichier JSON généré via la Google Cloud Console dans le répertoire sécurisé :
```bash
# Exemple (depuis une source sûre)
sudo cp service-account-key.json /etc/opt-trading/secrets/google/writer-service-account.json
sudo chmod 600 /etc/opt-trading/secrets/google/writer-service-account.json
```

## 3. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/google_sheets_writer.env
```

Contenu attendu :
```env
GOOGLE_SERVICE_ACCOUNT_JSON_PATH=/etc/opt-trading/secrets/google/writer-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=XXXXX_VOTRE_ID_ICI_XXXXX
```

## 4. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/google_sheets_writer.env
```
