---
doc_id: SIGNAL_DIAG_01_NGROK
doc_type: ngrok_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_NGROK_TUNNEL_STATE

## Public URL

`https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev`

## Match avec docs

Le journal.md reference la meme URL. **Aucun changement d'URL ngrok.**

## Etat tunnel

| Propriete | Valeur |
| --- | --- |
| Proto | HTTPS |
| Local addr | http://localhost:8000 |
| Session | CONNECTED (14:48 today) |
| Status API | 200 OK |

## Metrics (CRITIQUE)

| Metric | Value |
| --- | --- |
| conns.count | **0** |
| conns.gauge | **0** |
| http.count | **0** |
| All rates | **0.00** |

**Zero external connections.** Le tunnel est UP mais personne n'appelle.

## Stabilite ngrok

- Sessions instables: heartbeat timeouts frequents
- May 1: DNS failures ("server misbehaving"), multiples reconnects
- May 1, 4: connection resets, session drops
- Auto-reconnect fonctionnel mais intermittent
