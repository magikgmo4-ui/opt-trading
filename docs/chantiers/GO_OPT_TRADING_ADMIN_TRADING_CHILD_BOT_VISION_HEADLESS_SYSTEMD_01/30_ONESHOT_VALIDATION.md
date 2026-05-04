---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_ONESHOT
doc_type: oneshot_validation
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_ONESHOT_VALIDATION

## Commande

```bash
sudo systemctl start bot-vision-headless-capture.service
```

## Resultat

**PASS** — Exit 0/SUCCESS.

## Journal

```
Starting bot-vision-headless-capture.service - Bot Vision Headless Capture...
[2026-05-04_17-28-50] Capturing: tradingview BTCUSDT.P
OK: .../screen_tradingview_BTCUSDT.P_H1_2026-05-04_17-28-50.png (91323B)
OK: .../screen_tradingview_BTCUSDT.P_H1_2026-05-04_17-28-50.json (497B)
DONE: tradingview -> screen_tradingview_BTCUSDT.P_H1_2026-05-04_17-28-50.png
Capture cycle complete.
bot-vision-headless-capture.service: Deactivated successfully.
```

## Verification

| Check | Resultat |
| --- | --- |
| PNG > 0 | 91323 B (91 KB) |
| JSON sidecar | 497 B |
| 0-byte | 0 |
| .uploading restant | 0 |
| Exit code | 0 (SUCCESS) |
| CPU | 10.189s (Chromium render) |

## Note: CRLF fix

Les fichiers copies depuis Windows avaient des line endings CRLF.
Corrige avec `sed -i "s/\r$//"`.
A ne pas reproduire (utiliser git avec core.autocrlf ou transferer en binaire).
