---
doc_id: GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01_GAPS_P3_P6
doc_type: audit
repo: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01
status: CLOSED
created_at: 2026-06-03
---

# 70_GAPS_AUDIT — P3 Bitget + P6 secrets.py

## P3 — Bitget scope audit : PASS

**Verdict : READ-ONLY confirmé par le code.**

Tous les appels Bitget dans le repo sont en lecture uniquement :

| Fichier | Opération | Méthode HTTP |
|---|---|---|
| `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` | `bitget_candles()` | GET |
| `modules/derivatives_collector/app/bitget_adapter.py` | collecte market data | GET |
| `modules/derivatives_collector/app/derivatives_collector.py` | OI/Funding/Liq/LSR | GET |
| `modules/auth/bitget_credentials.py` | chargement credentials | — |

Aucun `place_order`, aucun `POST` vers l'exchange, aucun `withdraw`. Le profil `readonly_main`
dans `.secrets/bitget.env` est cohérent avec l'usage réel.

**Action restante** : vérifier côté console Bitget que le scope API est bien `Read Only`
(pas de Order, pas de Trade, pas de Withdraw). Action manuelle, hors repo.

---

## P6 — secrets.py non systématique : INVENTAIRE

### Périmètre

`modules/auth/secrets.py` expose `get_secret(name)` et `require_secret(name)`.
Ces fonctions ne sont pas systématiquement utilisées — la plupart des modules
lisent `os.environ.get()` directement.

### Occurrences directes sur variables sensibles

| Fichier | Variable | Risque |
|---|---|---|
| `webhook_server.py` | `TV_WEBHOOK_KEY`, `OPS_ADMIN_KEY`, `TELEGRAM_BOT_TOKEN` | MEDIUM — module d'entrée |
| `perf/perf_app.py` | `TELEGRAM_BOT_TOKEN` | LOW — fallback vide accepté |
| `shared/telegram_notify.py` | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | LOW — fallback vide |
| `shared/telegram_channels.py` | `TELEGRAM_BOT_TOKEN`, CHAT_ID_* | LOW — fallback vide |
| `modules/desk_analyze/analyze_latest.py` | `OPENAI_API_KEY` | LOW — usage facultatif |
| `modules/collector_telegram/src/.../config.py` | `TELEGRAM_API_HASH` | LOW — collecteur standalone |
| `modules/bot_vision/headless_capture/scripts/` | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | LOW — scripts Node headless |
| `modules/openclaw_github_actions_bridge/app/bridge.py` | `GITHUB_TOKEN` | LOW — injecté par CI |

### Analyse

**102 occurrences totales** de `os.environ.get` dans les modules — mais la grande majorité
sont des variables de config opérationnelle non sensibles (URLs, timeouts, flags, seuils).

Les appels sur variables sensibles (TOKEN, KEY, SECRET) sont concentrés dans les entry points
(`webhook_server.py`, `perf_app.py`) et les modules shared (`telegram_notify`, `telegram_channels`).

Ces modules ne bénéficieraient pas d'un refactor vers `require_secret()` car :
- Ils acceptent légitimement des valeurs vides (Telegram optionnel, fallback gracieux)
- `require_secret()` lève une exception → inadapté pour des features optionnelles

### Verdict

**Non bloquant. Refactor non justifié en l'état.**

`require_secret()` est utile pour les modules qui doivent échouer fort si un secret manque
(ex : `bitget_credentials` pour le trading). Pour les modules à dégradation gracieuse
(Telegram désactivé si token absent), `os.environ.get(key, "")` est le pattern correct.

**Recommandation** : appliquer `require_secret()` uniquement lors de la création de nouveaux
modules où l'absence du secret est une erreur fatale, non comme refactor systématique.
