---
doc_id: SIGNAL_DIAG_01_LAST_SIGNAL
doc_type: last_signal
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_WEBHOOK_LAST_SIGNAL

## Derniers POST /tv (April 1, 2026)

```
avr 01 06:53:05 POST /tv 200 OK (127.0.0.1:44586)
avr 01 06:54:02 POST /tv 200 OK (127.0.0.1:46512)
...
avr 01 07:12:05 POST /tv 200 OK (127.0.0.1:40102)
```

- Rythme: ~1/min (TradingView alert cadencee)
- Tous depuis 127.0.0.1 (ngrok forward local)
- Tous 200 OK (pas de rejet, pas d'erreur)
- **Dernier: 2026-04-01 07:12:05 UTC / 03:12:05 EDT**

## Depuis April 1

| Evenement | Date |
| --- | --- |
| Dernier POST /tv | 2026-04-01 07:12 |
| Derniere activite (GET /dash) | 2026-04-01 16:00 |
| Restart webhook (PID change) | 2026-04-16 13:49 |
| Boot + restart | 2026-04-19 17:36 |
| Jours sans signal | **33 jours** |

## Erreurs webhook

**AUCUNE** — aucun log d'erreur depuis April 1.
Le webhook n'a rien a traiter, donc rien a rejeter.

## Conclusion

Le serveur webhook est UP et fonctionnel. Il a correctement traite tous les signaux
jusqu'au April 1. Depuis: zero input. Pas de crash, pas de rejet, juste... rien.
