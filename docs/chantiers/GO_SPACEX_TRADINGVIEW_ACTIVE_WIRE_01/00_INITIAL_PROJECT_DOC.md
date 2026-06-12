# GO_SPACEX_TRADINGVIEW_ACTIVE_WIRE_01

## Objectif

Connecter TradingView comme producteur actif pour le SpaceX desk.
TradingView envoie des alertes webhook → `/tv/spacex` → persist event → collect_once.

## Séparation stricte

- `/tv/spacex` : observer-only, aucun risque, aucun trade engine
- `/tv` : trade/risk engine — ne pas utiliser pour SpaceX

## Payload attendu (TradingView webhook message)

```json
{
  "key": "{{TV_WEBHOOK_KEY}}",
  "source": "tradingview",
  "symbol": "{{ticker}}",
  "exchange": "{{exchange}}",
  "interval": "{{interval}}",
  "price": {{close}},
  "alert_name": "{{alert_name}}",
  "signal": "BULLISH",
  "note": "SpaceX desk alert"
}
```

## Persistance

- `data/ipo/spacex/raw/spacex_snapshots.jsonl` — append JSONL
- `data/ipo/spacex/latest_snapshot.json` — dernier événement
- `data/ipo/spacex/raw/` est dans `.gitignore` (runtime data)

## Dépendances URL publique

TradingView webhooks requièrent port 80 ou 443. Options :
- ngrok (dev)
- Cloudflare Tunnel (production)
- Reverse proxy VPS

## État

| Étape | Statut |
|---|---|
| Endpoint `/tv/spacex` | DONE — smoke PASS 2026-06-12 |
| Expose HTTPS 443 | TODO |
| Alerte TradingView SPCX | TODO |
| Vérification persistance prod | TODO |
| Telegram push SpaceX | WIRED (TELEGRAM_ENABLED requis) |
| Pine setup pack | TODO |
| TV snapshots périodiques | TODO |
