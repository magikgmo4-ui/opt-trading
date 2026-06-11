---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_SOURCE_REGISTRY_MODEL
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: source_registry_model
status: draft_reference
created_at: 2026-06-06
---

# 01_SOURCE_REGISTRY_MODEL

## Objectif

Définir le registre canonique des chaînes YouTube à collecter.

Le registre ne doit pas être une liste brute de chaînes. Il doit décrire :

- pourquoi la source est incluse ;
- quel type de vidéos viser ;
- quel parser utiliser ;
- quelles limites de collecte appliquer ;
- quel statut de validation utiliser.

## Format recommandé

Fichier cible futur :

```text
registry/youtube_sources.jsonl
```

Ligne type :

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
  "notes": "Chaîne pilote initiale."
}
```

## Statuts

```text
P0_PILOT       source pilote prioritaire
P1_ACTIVE      source validée pour collecte régulière
P2_DISCOVERY   source candidate non validée
P3_CONTEXT     source informative, non parser prioritaire
REJECTED       source rejetée avec raison
```

## Modes de collecte

```text
latest          dernières vidéos seulement
shorts_first    Shorts priorisés
keyword         vidéos filtrées par mots-clés
date_range      plage temporelle explicite
manual_seed     URLs manuelles pour validation
```

## Règles

- Une chaîne ne passe pas `P1_ACTIVE` sans fixtures validées.
- Le registre doit conserver la raison d'inclusion.
- Les sources doivent être limitées par run.
- Les chaînes non trading ou trop bruitées restent `P3_CONTEXT` ou `REJECTED`.
