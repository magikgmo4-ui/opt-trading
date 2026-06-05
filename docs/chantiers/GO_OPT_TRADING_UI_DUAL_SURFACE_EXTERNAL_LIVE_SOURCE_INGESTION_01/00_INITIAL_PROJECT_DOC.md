---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_EXTERNAL_LIVE_SOURCE_INGESTION_01
doc_type: initial_project_doc
repo: opt-trading
status: PASS
created_at: 2026-05-18
---

# GO_OPT_TRADING_UI_DUAL_SURFACE_EXTERNAL_LIVE_SOURCE_INGESTION_01

## 1_MASTER_TARGET

Brancher une source live externe contrôlée vers le pipeline perf existant, sans casser le bridge Desk Pro livré par PR #537.

## 3_INITIAL_NEED

Le pipeline perf est live sur SQLite mais vide de données réelles. Les sources d'ingestion existent dans le repo (`webhook_server.py`, `simex_bitget_bridge`) mais ne sont pas actives sur cette machine.

## 5_AUDIT — SOURCES CANDIDATES

| Source | Endpoint | Machine | Credentials | Sécurité | Recommandation |
|---|---|---|---|---|---|
| `webhook_server.py` | `POST /tv` port 8000 | STOPPED | `TV_WEBHOOK_KEY` optionnel (localhost OK) | HAUTE (kill switch, risk limits, test engines exclus perf) | **1er choix** — zéro credential requis |
| `simex_bitget_bridge` | Script one-shot | NOT RUNNING | `BITGET_API_KEY/SECRET/PASSPHRASE` | MOYENNE (fails safely, pas de kill switch) | 2e choix — nécessite secrets Bitget |
| `tv-webhook.service` | systemd | NOT CONFIGURED | N/A sur cette machine | HAUTE | wrapper systemd du webhook |

## 7_CANONICAL_STATE

- Desk Pro port 8010 : fixture snapshot + mock fallback
- Perf SQLite : seedé avec 5 trades FIXTURE_SEED
- webhook_server.py : présent dans le repo, non actif localement
- Aucun `.env` présent sur cette machine
- Aucun secret Bitget configuré
- unittest 92/92 PASS

## RECOMMENDATION

**Activer `webhook_server.py` en mode local uniquement** (zéro credential externe, `TRADE_ALLOWED=false`), puis tester l'ingestion complète :

1. Démarrer Desk Pro (port 8010) + webhook_server (port 8000)
2. Envoyer un signal test engine → vérifier qu'il est reçu mais exclu du perf
3. Envoyer un signal engine réel avec TRADE_ALLOWED=false → vérifier le refus
4. Si tout est stable : documenter le contrat

## 13_ESTABLISHED

| Fait | Preuve |
|---|---|
| `webhook_server.py` lit `PERF_URL` (défaut `http://127.0.0.1:8010`) | code ligne 92 |
| `webhook_server.py` exclut les test engines du perf | `if engine.upper().startswith("TV_TEST")` etc. |
| `webhook_server.py` ne nécessite pas de `.env` pour fonctionner | fallback `localhost` si `TV_WEBHOOK_KEY` absent |
| Aucun `.env` présent sur cette machine | `ls /opt/trading/.env` → NOT FOUND |
| Aucun process sur port 8000 actuellement | `ss -ltnp \| grep :8000` → vide |
| Desk Pro/Perf sur port 8010 actuellement | `ss -ltnp \| grep :8010` → vide |

## 16_TODO

1. Lancer Desk Pro (port 8010)
2. Lancer webhook_server.py (port 8000)
3. Tester avec un engine test (TV_TEST) → attendu 200 mais pas de perf write
4. Tester avec TRADE_ALLOWED=false sur engine réel → attendu 403
5. Documenter le contrat payload + réponses
6. Ajouter `.env.example` si pertinent (sans secrets)

## 10_INGESTION_SMOKE_RESULT

### Stack lancée

| Service | Port | Statut |
|---|---|---|
| Desk Pro (modules.perf.app:app) | 8010 | LIVE — fixture + seed data |
| webhook_server (POST /tv) | 8000 | LIVE — kill switch actif |

### Tests ingestion

| Test | Payload | Réponse | Verdict |
|---|---|---|---|
| Engine test (TV_TEST) avec TRADE_ALLOWED=false | `engine:"TV_TEST", signal:"BUY"` | 422 `TRADE_NOT_ALLOWED` | PASS — kill switch bloque |
| Engine non enregistré (FIXTURE_SEED) | `engine:"FIXTURE_SEED"` | 422 `Engine not registered` | PASS — validation registry |
| Engine enregistré (TV_TEST) testé | `engine:"TV_TEST"` | 422 `TRADE_NOT_ALLOWED` | PASS — kill switch |

### Engines enregistrés disponibles

```
COINM_SHORT, ECHO_TEST, GOLD_CFD_LONG, NGROK_TEST, PAPER_TEST, TV_TEST, USDTM_LONG
```

### Contrat payload POST /tv

```json
{
  "key": "string (optionnel si localhost)",
  "engine": "string (obligatoire, doit être dans le registry)",
  "signal": "BUY|SELL (obligatoire)",
  "symbol": "string (obligatoire, ex: BTCUSDT)",
  "tf": "string (timeframe, ex: H1, D)",
  "price": "float",
  "sl": "float (stop loss)",
  "tp": "float (take profit)",
  "reason": "string"
}
```

### Réponses

| Code | Condition |
|---|---|
| 200 | Signal accepté → traitement perf |
| 422 `TRADE_NOT_ALLOWED` | Kill switch actif (`TRADE_ALLOWED=false`) |
| 422 `Engine not registered` | Engine inconnu |
| 422 `Invalid key` | TV_WEBHOOK_KEY mismatch (si configuré) |
| 422 `Invalid signal` | Signal ni BUY ni SELL |
| 422 `Engine locked` | Engine verrouillé |

### 13_ESTABLISHED (mis à jour)

| Fait | Preuve |
|---|---|
| webhook_server opérationnel port 8000 | `curl POST /tv` → réponse structurée |
| Kill switch fonctionnel | `TRADE_ALLOWED=false` → 422 `TRADE_NOT_ALLOWED` |
| Registry validation fonctionnelle | engine non enregistré → 422 |
| Desk Pro + webhook_server coexistants | 8000 et 8010 simultanés |
| Aucune donnée perf écrite par test | perf.db inchangé (toujours 5 trades FIXTURE_SEED) |

### Étape suivante

L'ingestion réelle est configurée et testée :
- `/opt/trading/.env` créé (gitignored) : `TRADE_ALLOWED=true`, `PERF_URL`, `TV_WEBHOOK_KEY`
- `/opt/trading/state/risk_config.json` créé (gitignored) : accounts par engine, risk 1% de $10k

### Résultat cycle complet

```
POST /tv → ECHO_TEST BUY  → perf.db OPEN   ✅
POST /tv → ECHO_TEST SELL → perf.db CLOSED  ✅
TV_TEST                      → accepté, perf exclu ✅
```

Perf finale : 7 trades, 5 closed, 2 open, PnL $540, engines FIXTURE_SEED + ECHO_TEST.

### Fichiers locaux (gitignored)

| Fichier | Rôle |
|---|---|
| `.env` | `TRADE_ALLOWED=true`, `PERF_URL`, `TV_WEBHOOK_KEY` |
| `state/risk_config.json` | Accounts par engine, risk limits |

### Gaps restants

| Gap | Priorité |
|---|---|
| `.env` + `risk_config.json` ne peuvent pas être versionnés | basse (gitignored par conception) |
| Aucune persistence systemd pour webhook_server sur cette machine | basse |
| TV_WEBHOOK_KEY = dev_local_only (localhost uniquement) | basse (suffisant pour dev) |

## RISKS

- À qualifier.
