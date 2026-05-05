---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_20_SCOPE
doc_type: chantier/scope
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - webhook_server.py
  - shared/telegram_notify.py
  - modules/auth/webhook_key.py
  - modules/webhook/handlers.py
  - modules/webhook/parse.py
  - modules/webhook/schema.py
  - modules/tradingview_observer/templates/alert_webhook_template_v1.json
---

# 20_TELEGRAM_WEBHOOK_SCOPE — Perimetre du flux Telegram/webhook

## Objet

Decrire le perimetre complet du flux de donnees entre la reception du webhook
TradingView et la notification Telegram, en isolant les points de verification
pour le test en usage reel.

## Flux complet

```
TradingView Alert
       |
       v
  POST /tv  (FastAPI webhook_server.py:364)
       |
       v
  require_key()  (webhook_server.py:338)
  ├─ TV_WEBHOOK_KEY set → hmac.compare_digest (modules/auth/webhook_key.py)
  └─ TV_WEBHOOK_KEY not set → localhost only (127.0.0.1, ::1)
       |
       v
  parse_payload()  (modules/webhook/parse.py)
  ├─ engine validation (registry.get_engine)
  ├─ signal validation (BUY/SELL)
  └─ symbol, tf, price, tp, sl extraction
       |
       v
  enforce_lock()  (webhook_server.py:353)
  └─ router_state.json: only one aggressive engine active at a time
       |
       v
  risk_quote()  (webhook_server.py:224)
  └─ RiskCalculator.calculate_quote(risk_config.json)
       |
       v
  perf_open()  (webhook_server.py:428)
  ├─ SKIPPED for TV_TEST / TEST_* / _TEST_ engines (line 415)
  └─ Ledger trade only for real engines
       |
       v
  record_event()  (webhook_server.py:456)
  └─ → state/events.jsonl
       |
       v
  telegram_send()  (webhook_server.py:466)
  ├─ Gated: TELEGRAM_ENABLED flag (line 459)
  └─ → shared/telegram_notify.py → Telegram Bot API
```

## Points de verification

### A. Reception webhook

| Point | Fichier | Ligne | Description |
| --- | --- | --- | --- |
| A1 | `webhook_server.py` | 364 | POST `/tv` entrypoint |
| A2 | `webhook_server.py` | 338-351 | `require_key()` authentication |
| A3 | `webhook_server.py` | 382-392 | Engine/signal validation |
| A4 | `webhook_server.py` | 394 | `enforce_lock()` call |

### B. Traitement

| Point | Fichier | Ligne | Description |
| --- | --- | --- | --- |
| B1 | `webhook_server.py` | 402-404 | `risk_quote()` call |
| B2 | `webhook_server.py` | 415-416 | TEST engine skip (perf ledger bypass) |
| B3 | `webhook_server.py` | 439-454 | Event construction |
| B4 | `webhook_server.py` | 456 | `record_event()` |

### C. Notification Telegram

| Point | Fichier | Ligne | Description |
| --- | --- | --- | --- |
| C1 | `webhook_server.py` | 459 | `TELEGRAM_ENABLED` gate |
| C2 | `webhook_server.py` | 461-465 | Message construction |
| C3 | `webhook_server.py` | 466 | `telegram_send()` call |
| C4 | `shared/telegram_notify.py` | 6-21 | Bot API POST |

### D. Execution (guardee)

| Point | Fichier | Ligne | Description |
| --- | --- | --- | --- |
| D1 | `webhook_server.py` | 469 | `engine == "PAPER_TEST"` gate |
| D2 | `webhook_server.py` | 470 | `pos_manager.can_open_position()` guard |
| D3 | `webhook_server.py` | 472-474 | Guard BLOCKED return |

## Code source references

### telegram_send() — webhook_server.py:459-466

```python
if TELEGRAM_ENABLED:
    q = risk_quote(engine, price=price, sl=sl, tp=tp) if (price and sl) else None
    qty_txt = ""
    if q and q.get("qty"):
        qty_txt = f"\nqty: {q['qty']} | risk_usd: {q.get('risk_usd')}"
    msg = f"{signal} {symbol} {tf}\nengine: {engine}\nprice: {price} | tp: {tp} | sl: {sl}\nreason: {reason}{qty_txt}"
    telegram_send(msg)
```

### send_telegram() — shared/telegram_notify.py:6-21

```python
def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Telegram env vars not set")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": html.escape(message), "parse_mode": "HTML", "disable_web_page_preview": True}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
```

### TEST engine bypass — webhook_server.py:415-416

```python
if engine == "TV_TEST" or engine.startswith("TEST_") or engine.startswith("_TEST_"):
    pass  # skip perf ledger
```

### PAPER_TEST engine gate — webhook_server.py:469-474

```python
if engine == "PAPER_TEST":
    guard = pos_manager.can_open_position(symbol, signal)
    if not guard["ok"]:
        log.warning(f"GUARD BLOCKED: {guard}")
        return {"ok": True, "skipped": guard["reason"]}
```

## Payload de test safe

Payload JSON minimal pour test controle (envoye depuis TradingView ou curl local) :

```json
{
    "key": "tk:test_webhook_real_usage_01",
    "engine": "TV_TEST",
    "signal": "BUY",
    "symbol": "TEST/USDT",
    "tf": "1m",
    "price": 100.0,
    "tp": 110.0,
    "sl": 95.0,
    "reason": "GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01"
}
```

Caracteristiques du payload safe :
- `engine: "TV_TEST"` → bypass complet du perf ledger (webhook_server.py:415)
- `engine != "PAPER_TEST"` → bypass complet du bloc execution (webhook_server.py:469)
- Aucun trade reel possible
- Passage par risk_quote, record_event, et Telegram notify (si TELEGRAM_ENABLED)

## Hors perimetre

- Engine PAPER_TEST (declenche l'execution papier → hors scope)
- Engine COINM_SHORT, USDTM_LONG, GOLD_CFD_LONG (engines reels → hors scope)
- Modification de `webhook_server.py`
- Modification de `modules/webhook/`
- Exposition d'un endpoint ngrok en production
