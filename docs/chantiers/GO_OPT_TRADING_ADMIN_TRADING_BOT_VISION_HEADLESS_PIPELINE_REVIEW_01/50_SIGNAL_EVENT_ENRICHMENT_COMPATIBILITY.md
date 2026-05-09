---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_SIGNAL_EVENT_ENRICHMENT
doc_type: signal_event_enrichment_compatibility
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 50_SIGNAL_EVENT_ENRICHMENT_COMPATIBILITY - Signal Event Enrichment

## Objectif

Documenter comment `visual_context` V1 peut se relier à `signal_event` V1 pour enrichir le flux Desk Pro.

## signal_event.visual_context_ref

Le champ `visual_context_ref` dans `signal_event` V1 (défini dans `30_SIGNAL_EVENT_CONTRACT.md`) permet de lier un signal webhook à une capture visuelle :

```json
{
  "source": "tradingview.webhook",
  "event_type": "signal_event",
  "engine": "momentum",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "direction": "BUY",
  "timestamp": "2026-05-06T02:20:00Z",
  "status": "accepted",
  "visual_context_ref": "screen_tradingview_BTCUSDT.P_H1_2026-05-06_02-20-15.png",
  "desk_snapshot_ref": "BTCUSDT.P_H1_20260506_022535.png"
}
```

## visual_context.signal_event_ref

Le champ `signal_event_ref` dans `visual_context` V1 permet de lier une capture à un signal :

```json
{
  "source": "bot_vision_headless",
  "capture_id": "screen_tradingview_BTCUSDT.P_H1_2026-05-06_02-20-15",
  "symbol": "BTCUSDT.P",
  "timeframe": "H1",
  "captured_at": "2026-05-06T02:20:15Z",
  "image_ref": "/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-06_02-20-15.png",
  "status": "ready",
  "signal_event_ref": "evt_20260506_022000_BTCUSDT"
}
```

## Pas de coupling direct webhook → capture

- Le webhook (`tv-webhook`) et la capture headless (`capture_headless.js`) sont des producers **indépendants**
- Ils n'ont pas de dépendance runtime l'un envers l'autre
- Le lien entre `signal_event` et `visual_context` est **asynchrone** et **optionnel**
- La jointure se fait a posteriori par le consumer (Desk Pro)

## Lien par ref/hash/timestamp/symbol/timeframe

La jointure entre `signal_event` et `visual_context` peut se faire par :

| Join key | Signal Event | Visual Context | Fiabilité |
| --- | --- | --- | --- |
| `symbol` | `symbol` | `symbol` | haute (normalisation nécessaire) |
| `timeframe` | `timeframe` | `timeframe` | haute |
| `timestamp` (fenêtre) | `timestamp` | `captured_at` | moyenne (tolérance ±5min) |
| `payload_hash` | `payload_hash` | `payload_hash` | haute (si calculé) |
| `*_ref` explicite | `visual_context_ref` | `signal_event_ref` | haute (si produit) |

### Stratégie de jointure recommandée

1. **Par ref explicite** (priorité 1): si `signal_event.visual_context_ref` est défini, jointure directe
2. **Par symbol + timeframe + fenêtre temporelle** (priorité 2): matcher `signal_event.timestamp ± 10min` avec `visual_context.captured_at`
3. **Par hash** (priorité 3): si `payload_hash` est calculé des deux côtés

## Desk Pro doit pouvoir consommer les deux sans dépendre de l'ordre

- `signal_event` arrive via `state/events.jsonl` (webhook)
- `visual_context` arrive via `desk/snapshots/latest.json` (capture → bridge → ingest)
- Les deux flux sont **indépendants** et **asynchrones**
- Desk Pro ne doit pas bloquer si un seul des deux est disponible
- Desk Pro peut enrichir un signal existant quand `visual_context` arrive plus tard
- Desk Pro peut afficher une capture même sans signal event associé

## Matrice de jointure

| Artifact A | Artifact B | Join key | Required? | Consumer | Risk |
| --- | --- | --- | --- | --- | --- |
| signal_event | visual_context | symbol + timeframe + timestamp fenêtre | optionnel | Desk Pro | faible — fallback sans enrichissement |
| signal_event | desk_snapshot | symbol + timeframe + snapshot_ts | optionnel | Desk Pro | faible — fallback sans enrichissement |
| visual_context | desk_snapshot | symbol + timeframe + capture_ts = snapshot_ts | oui (pipeline) | desk_bridge | aucun — lien direct par ingest |
| signal_event | visual_context | visual_context_ref (explicite) | optionnel | Desk Pro | aucun — ref non produite actuellement |
| signal_event | desk_snapshot | desk_snapshot_ref (explicite) | optionnel | Desk Pro | aucun — ref non produite actuellement |

## Gaps d'enrichissement

1. **Pas de `visual_context_ref` produit**: le webhook ne produit pas cette ref car il n'a pas accès au pipeline vision
2. **Pas de `signal_event_ref` produit**: la capture ne produit pas cette ref car elle n'a pas accès au webhook
3. **Pas de `payload_hash`**: ni `signal_event` ni `visual_context` ne produisent de hash actuellement
4. **Join par timestamp**: la fenêtre temporelle doit être calibrée (±5min pour H1, ±15min pour H4)
5. **Normalisation symbol**: `BTCUSDT` (webhook) vs `BTCUSDT.P` (capture) — mismatch à résoudre

## Verdict

L'enrichissement `signal_event` ↔ `visual_context` est **faisable** sans coupling direct, par jointure symbol/timeframe/timestamp. Les refs explicites sont préparées dans les schémas V1 mais non produites par le runtime actuel. Le join par fenêtre temporelle est le mode opérationnel immédiat.
