# Admin Trading Desk Pro - Quick Reference

## Commandes clés
| Action | Commande | Description |
|---|---|---|
| **Santé** | `sanity-desk-pro` | Vérifier l'état global du système |
| **Status** | `desk-pro status` | Afficher les composants disponibles |
| **Info Run** | `desk-pro-last-run` | Résumé du dernier run/log |
| **Exécuter** | `desk-pro-run-logged` | Lancer un run complet avec logs |
| **Log** | `desk-pro-tail-log` | Voir les 50 dernières lignes du log |
| **Dashboard** | `desk-pro dashboard-latest` | Afficher le résumé portefeuille |
| **Export HTML** | `desk-pro export-html-latest` | Générer le rapport HTML |
| **Partager** | `desk-pro-copy-latest` | Copier HTML/JSON vers /shared |
| **Menu** | `menu-desk-pro` | Interface interactive complète |

---
**Rappel** : Mode **PAPER** uniquement. Aucune action réelle sur le marché.
**Logs** : `/opt/trading/data/logs/desk_pro/`
**Partage** : `/shared/desk_pro/latest/`

## Service
- `tv-perf.service` : `uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010`

## URLs admin-trading
- `http://127.0.0.1:8010/desk/health`
- `http://127.0.0.1:8010/desk/snapshot`

## URLs LAN
- `http://<IP_ADMIN_TRADING>:8010/desk/health`
- `http://<IP_ADMIN_TRADING>:8010/desk/snapshot`

## Scripts module Desk Pro
- `./scripts/desk_pro_sanity.sh`
- `./scripts/desk_pro_cmd.sh <health|snapshot|form-sample|sanity|tree>`
- `./scripts/desk_pro_menu.sh`
- `./scripts/desk_pro_http_test.sh`

## Variables d'environnement
- `TV_PERF_SCHEME`
- `TV_PERF_HOST`
- `TV_PERF_PORT`

## Procédure minimale
1. Copier `.env.example` vers `.env`.
2. Ajuster les variables si besoin.
3. Lancer `./scripts/desk_pro_requirements_fix.sh` si les deps Python sont à corriger.
4. Vérifier avec `./scripts/desk_pro_sanity.sh`.
5. Tester l'accès HTTP avec `./scripts/desk_pro_http_test.sh`.
