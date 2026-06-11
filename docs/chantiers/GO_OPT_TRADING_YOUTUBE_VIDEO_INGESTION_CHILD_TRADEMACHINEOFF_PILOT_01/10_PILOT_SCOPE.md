---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_PILOT_SCOPE
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: pilot_scope
status: draft_reference
created_at: 2026-06-11
---

# 10_PILOT_SCOPE

## Source unique

```text
handle: @trademachineoff
url: https://youtube.com/@trademachineoff
scope: Shorts first
priority: P0_PILOT
parser_profile: youtube_trading_short_v1
```

## Source registry entry cible

```json
{
  "source_type": "youtube_channel",
  "handle": "@trademachineoff",
  "url": "https://youtube.com/@trademachineoff",
  "channel_id": null,
  "theme": "trading_short_form",
  "language_hint": "auto",
  "priority": "P0_PILOT",
  "video_scope": "shorts_first",
  "collection_mode": "latest_or_keyword",
  "keywords": ["gold", "xau", "btc", "nasdaq", "entry", "scalping", "strategy", "long", "short", "tp", "sl"],
  "max_videos_per_run": 20,
  "parser_profile": "youtube_trading_short_v1",
  "status": "candidate",
  "notes": "Source pilote initiale pour validation YouTube video ingestion."
}
```

## Volume pilote

```text
videos candidates: 10 a 20
fixtures annotees: 5 minimum
source expansion: interdite avant decision pilote
```

## Selection video

Priorite :

1. Shorts recents contenant du texte ecran trading.
2. Shorts contenant des termes explicites : `entry`, `long`, `short`, `tp`, `sl`.
3. Shorts avec actifs detectables : `XAUUSD`, `BTCUSDT`, `ETHUSDT`, `NASDAQ/US100`, `SPX/US500`.
4. Shorts educatifs seulement s'ils contiennent une structure exploitable.

## Exclusions

- Videos longues hors echantillon pilote.
- Contenu sans lien trading ou marche.
- Videos sans element de signal ou contexte exploitable.
- Toute interpretation en signal executable sans preuve entry/direction.

