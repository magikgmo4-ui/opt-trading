---
doc_id: WEBHOOK_REVIEW_01_LOGS
doc_type: logs_risks
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_LOGS_AND_RISKS

## tv-webhook logs

### Activite

- **Dernier POST /tv**: April 1, 2026 07:12:05 (il y a 33 jours!)
- **Derniere activite**: April 1 16:00 GET /dash
- **Depuis**: aucun POST /tv, aucun signal TradingView
- Service up mais idle depuis 33 jours
- Redemarrage Apr 16 (PID change), puis Apr 19 (boot)

### Notre test

- GET /health: 404 (endpoint manquant)
- GET /docs: 200 (OK)

## tv-perf logs

### Activite recente (mai 4)

- GET /perf/summary: toutes les ~5 min (polling actif)
- POST /perf/event: par paires (~1/sec d'ecart), toutes les ~5 min
- Le polling semble venir de cron/autos.sh

### Perf state

- 2 trades ouverts (BITGET_SM_LITE XAUUSDT LONG, COINM_SHORT BTCUSDT SHORT)
- PnL negatif: -84K realized
- max DD: 16509% (catastrophique)
- BITGET_SM_LITE: 100% WR, mais petits gains (+210)
- COINM_SHORT: 48% WR, grosses pertes (-79K)

## Risques identifies

| Risque | Severite | Description |
| --- | --- | --- |
| R1: Webhook idle | **CRITIQUE** | Aucun signal TradingView depuis 33 jours — ngrok peut etre down ou stratum change |
| R2: Perf en root | HAUTE | tv-perf.service tourne en root, pas necessaire |
| R3: Pas de /health | MOYENNE | Aucun healthcheck pour monitoring |
| R4: .env expose | MOYENNE | EnvironmentFile expose tous les secrets comme env vars |
| R5: PnL negatif | HAUTE | -84K PnL, DD 16509% — trading reel avec pertes |
| R6: Ports 0.0.0.0 | MOYENNE | 8000 et 8010 ecoutent sur toutes les interfaces |
| R7: ngrok public | MOYENNE | URL publique exposee, auth par HMAC |

## Verdict

Le webhook est **up mais idle** — aucun signal TradingView depuis 33 jours.
Le perf engine tourne et recoit encore des evenements (internes), mais les signaux
de trading exterieurs sont arretes. COINM_SHORT a accumule des pertes significatives.
