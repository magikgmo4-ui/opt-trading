---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_SAFE_TEST_BOUNDARY
doc_type: safe_test_boundary
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 30_SAFE_TEST_BOUNDARY - Safe Test Boundary

## Ce qui peut etre teste sans side effect

- lecture des fichiers repo et des documents API
- `systemctl status` en read-only
- `ss -ltnp` pour verifier les ports en ecoute
- inspection locale des routes declarees dans `webhook_server.py`
- futurs `GET` strictement locaux et read-only sur `/dash`, `/api/state`, `/api/events`, `/api/metrics`, `/perf/open`, `/perf/summary`, sous GO dedie ou extension explicite si necessaire

## Ce qui est interdit dans ce GO

- tout `POST /tv`
- tout `POST /api/reset_lock`
- tout `POST /perf/event`
- tout appel vers l'URL publique ngrok
- tout declenchement TradingView externe
- tout envoi Telegram ou verification par message reel
- toute lecture de secret, cle HMAC, token ou `.env`
- tout restart, reload ou manipulation systemd

## Conditions necessaires avant tout futur test reel

- GO dedie explicitement autorise
- perimetre exact du test ecrit avant execution
- separation entre payload de test et flux reel
- verification de la frontiere HMAC sans exposer `TV_WEBHOOK_KEY`
- confirmation que toute telemetrie aval est acceptable: perf, lock, event log, Telegram
- borne claire entre test local, tunnel ngrok et source TradingView externe

## Separation des surfaces

| Surface | Autorisation dans ce GO | Note |
| --- | --- | --- |
| localhost `127.0.0.1` | lecture seule | observation systemd, ports, code, docs |
| tunnel ngrok `127.0.0.1:4040` | non appele | service observe seulement |
| TradingView externe | interdit | aucune alerte reelle, aucun POST, aucun replay |

## Conclusion de securite

Le perimetre de cette reprise reste strictement documentaire et read-only. La frontiere sure s'arrete avant toute emission HTTP ou reset d'etat applicatif.
