---
doc_id: GO_OPT_TRADING_LOCALCMS_CREDENTIALS_PANEL_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_LOCALCMS_CREDENTIALS_PANEL_01
parent_go: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01
status: impl
created_at: 2026-06-03
---

# GO_OPT_TRADING_LOCALCMS_CREDENTIALS_PANEL_01

## Objectif

Ajouter un panneau credentials à LocalCMS (lecture seule) et un formulaire CLI
interactif pour faciliter la rotation des credentials.

## Contraintes

- LocalCMS reste **read-only** — aucun endpoint POST/PUT.
- Aucune valeur n'est jamais affichée, loggée ou transmise.
- Statut uniquement : SET / ABSENT / UNKNOWN / FUTURE.

## Livraisons

### modules/localcms/app/main.py

Nouveau endpoint `GET /credentials` — page HTML avec :
- 5 cartes de résumé (SET / ABSENT / UNKNOWN / FUTURE / Total actifs)
- Tableau par provider : ID, Env Var, Statut (badge couleur), Storage, File, Update Command
- Lien vers `python3 scripts/credentials_form.py` pour la mise à jour
- Lien sidebar ajouté dans la section "Security"
- Endpoint JSON : `GET /credentials/json`

Helpers ajoutés :
- `_cred_check_env()` — lecture directe du fichier .env
- `_cred_check_role()` — sudo -n grep sur les role files
- `_cred_check_system()` — test -f avec sudo -n fallback
- `_resolve_cred_status()` — dispatch selon storage type
- `_build_credentials_status()` — liste complète avec statuts
- `_credentials_html()` — HTML builder groupé par provider

### scripts/credentials_form.py

CLI interactif (Python3, sans dépendances externes) :
- `--status` : affichage lecture seule avec couleurs ANSI
- `--provider NAME` : mise à jour d'un seul provider
- Mode interactif : menu numéroté, getpass masqué, écriture vers le bon fichier
- `_write_env_key()` : update/append dans .env
- `_write_role_key()` : sudo tee + chmod 600 pour role files
- OpenClaw/system : redirige vers les procédures manuelles

## Registry couvert

35 credentials, 13 providers :
Telegram (10), TradingView (2), Internal (4), Google (3), GitHub (1),
Binance (1), Coinglass (1), Ollama (1), OpenAI (1), Anthropic (1),
Database (3), Airtable (2), DeskPro (2), ClickUp (1), Figma (2 future)

## Storage types

| Type | Mécanisme | Exemple |
|------|-----------|---------|
| env | read/write direct Python | /opt/trading/.env |
| role | sudo -n grep / sudo tee | /etc/opt-trading/env.d/roles/*.env |
| openclaw | check existence + redirect | ~/.openclaw/openclaw.json |
| system | test -f / sudo -n | /etc/wireguard/, ~/.ssh/ |
