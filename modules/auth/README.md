# auth

Briques d'authentification et d'acces aux secrets pour les surfaces runtime du repo.

## Role
- lire les secrets depuis l'environnement ou les fichiers locaux supportes
- valider la cle webhook TradingView
- charger les credentials Bitget profiles

## Contenu
- `secrets.py` : acces minimal aux variables sensibles
- `webhook_key.py` : extraction et validation constante de `TV_WEBHOOK_KEY`
- `bitget_credentials.py` : chargement des profils Bitget depuis `.secrets/bitget.env` et l'environnement
- `scripts/` : wrappers `cmd`, `menu`, `sanity`

## Integration
- `webhook_server.py` importe `modules.auth.webhook_key`
- les integrations Bitget peuvent lire les profils via `bitget_credentials.py`

## Statut
- actif
- module support runtime, pas surface produit autonome

## Notes de consolidation
- ne pas dupliquer la lecture de secrets ailleurs si `auth` couvre deja le besoin
- la frontiere `auth` / `env` doit rester simple :
  - `env` charge l'environnement
  - `auth` consomme les secrets et valide les acces
