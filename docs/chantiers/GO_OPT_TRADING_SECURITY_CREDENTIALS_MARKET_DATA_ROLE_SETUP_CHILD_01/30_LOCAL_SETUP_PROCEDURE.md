# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée.

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/market_data_readonly.env
```

Contenu attendu :
```env
BINANCE_API_KEY=XXXXX_VOTRE_CLE_BINANCE_ICI_XXXXX
BINANCE_SECRET_KEY=YYYYY_VOTRE_SECRET_BINANCE_ICI_YYYYY
COINGLASS_API_KEY=ZZZZZ_VOTRE_CLE_COINGLASS_ICI_ZZZZZ
```

## 3. Sécurisation finale
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/market_data_readonly.env
```
