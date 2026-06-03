# Première capture Telegram read-only bornée

**Generated:** 2026-06-03 05:05 UTC  
**Branch:** `go/GO_OPT_TRADING_TELEGRAM_LIVE_CAPTURE_READONLY_01`  
**Base:** `sot/mainline` (propre, PR #1069 + #1070 mergées)  

---

## 1. Pre-flight validation

### Credential validation

| Script | Result |
|---|---|
| `validate_credentials.py --machine fantome --job telegram_collect_channel` | ✅ OK — 6 credentials validés |
| `resolve_credentials.py --print-status` | ✅ **READY_TO_INJECT** |

Credentials authorised: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SESSION_PATH`, `TELEGRAM_ALERT_CHAT_ID`, `TELEGRAM_CHANNELS_CONFIG`.

### Sanity

```json
{
  "python_ok": true,
  "channels_total": 17,
  "channels_enabled": 13,
  "telegram_api_id_present": true,
  "telegram_api_hash_present": true,
  "session_path": "/etc/opt-trading/secrets/telegram/collector.session"
}
```

### Status avant run

```json
{
  "state": "healthy",
  "freshness_state": "fresh",
  "last_success_at": "2026-06-03T04:10:15Z",
  "last_failure_run_id": null
}
```

---

## 2. Capture run

**Commande :**
```bash
bash scripts/run_telegram_collector.sh --channel coinglass_alerts --limit 5 run
```

**Résultat brut :**
```json
{
  "run_id": "20260603T050457Z-a36bd3c5",
  "channels": ["coinglass_alerts"],
  "messages_total": 5,
  "channel_results_path": "outputs/channel_results/channel_results_20260603T050457Z-a36bd3c5.json"
}
```

---

## 3. Messages capturés (raw)

Source : `outputs/raw/coinglass_alerts.jsonl` — 5 messages, expéditeur **CoinGlass_Alerts**.

| # | Msg ID | Timestamp | Type | Symbole | Direction | Leverage | Prix entrée | Valeur position |
|---|---|---|---|---|---|---|---|---|
| 1 | 215050 | 05:01:33Z | Hyperliquid whale | BTC | SHORT | 40x | $66,090.40 | $2.557M |
| 2 | 215049 | 05:01:31Z | Hyperliquid whale | BTC | LONG | 40x | $66,269.20 | $5.378M |
| 3 | 215048 | 05:00:26Z | Hyperliquid whale | BTC | SHORT | 40x | $66,373.80 | $1.021M |
| 4 | 215047 | 04:57:11Z | Hyperliquid whale | ZEC | LONG | 10x | $615.37 | $1.076M |
| 5 | 215046 | 04:54:39Z | Hyperliquid whale | BTC | SHORT | 40x | $66,252.00 | $2.000M |

Tous les messages sont en chinois (mandarin), format coinglass whale alert avec lien Hyperliquid.

---

## 4. Channel results

```json
{
  "channel_alias": "coinglass_alerts",
  "role": "LIQUIDITY_OI",
  "messages_total": 5,
  "parsed_count": 5,
  "claims_count": 0,
  "needs_review_count": 5,
  "unknown_raw_count": 0,
  "noise_count": 0,
  "dominant_message_types": ["MARKET_STRUCTURE"],
  "avg_parser_score": 0.78,
  "recommended_status": "KEEP_REVIEW_REQUIRED"
}
```

- **5/5 parsed** — tous les messages ont été reconnus par le parser
- **0 claims** — aucun message forwardé à un consumer
- **5 needs_review** — tous nécessitent validation humaine (première capture)
- **avg_parser_score: 0.78** — score correct mais perfectible (parser coinglass encore PARTIAL)
- **Dominant: MARKET_STRUCTURE** — typage cohérent avec des signaux whale/leverage

---

## 5. Errors

Aucune erreur pour ce run. L'historique `errors.jsonl` montre des échecs historiques résolus :

| Date | Error | Résolu |
|---|---|---|
| 01-Jun 20:39 | `unable to open database file` | ✅ Session path corrigé |
| 01-Jun 20:46 | `Cannot send requests while disconnected` | ✅ Session stabilisée |
| 01-Jun 20:53 | `Nobody is using this username` | ✅ Channel map corrigée |
| 01-Jun 21:37 | `api.api_id must be set` | ✅ Credentials chargés |

---

## 6. Statut final (status.json)

```json
{
  "state": "healthy",
  "last_success_run_id": "20260603T050457Z-a36bd3c5",
  "last_failure_run_id": null,
  "message": "run succeeded"
}
```

---

## 7. Décision

| Critère | Statut |
|---|---|
| Capture live fonctionnelle | ✅ 5 messages / 0 erreur |
| Parser coinglass reconnaît les messages | ✅ 5/5 parsed |
| Qualité parser (avg score) | ⚠️ 0.78 — acceptable pour phase 1 |
| Nécessite révision humaine | ✅ Oui (première passe) |
| Forward trading | ❌ Pas activé (0 claims) |
| Secrets sécurisés | ✅ Gitignore + /etc/opt-trading |

**Recommandation :** Passer à `--limit 20` sur coinglass_alerts pour valider la montée en charge, puis étendre à 1-2 autres canaux (glassnode, whale_alert_io).

---

## 8. Outputs

| Fichier | Chemin |
|---|---|
| Raw messages | `outputs/raw/coinglass_alerts.jsonl` |
| Channel results | `outputs/channel_results/channel_results_20260603T050457Z-a36bd3c5.json` |
| Status | `outputs/status.json` |
| Manifest | `outputs/manifest.json` |
| Events | `outputs/events.jsonl` |
| Errors | `outputs/errors.jsonl` |
