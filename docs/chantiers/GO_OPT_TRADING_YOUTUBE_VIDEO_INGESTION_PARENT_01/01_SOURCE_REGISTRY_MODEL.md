---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_SOURCE_REGISTRY_MODEL
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: source_registry_model
status: reference
created_at: 2026-06-06
surface: youtube_video_ingestion
---

# 01_SOURCE_REGISTRY_MODEL

## Objectif

Définir un registre stable pour les chaînes YouTube ciblées avant toute collecte vidéo.

Le registre évite la saisie manuelle des URLs vidéo et empêche le discovery massif non contrôlé.

## Modèle minimal

```json
{
  "source_type": "youtube_channel",
  "source_id": "youtube_trademachineoff",
  "handle": "@trademachineoff",
  "url": "https://youtube.com/@trademachineoff",
  "channel_id": null,
  "theme": "trading_short_form",
  "language_hint": "auto",
  "priority": "P0_PILOT",
  "video_scope": "shorts_first",
  "collection_mode": "latest_or_keyword",
  "keywords": ["gold", "xau", "btc", "nasdaq", "entry", "long", "short", "tp", "sl"],
  "max_videos_per_run": 20,
  "parser_profile": "youtube_trading_short_v1",
  "status": "candidate",
  "notes": "Chaîne pilote validée pour premier échantillon."
}
```

## Priorités

```text
P0_PILOT      chaîne pilote active
P1_TARGET     chaîne validée à collecter ensuite
P2_DISCOVERY  chaîne candidate à vérifier
P3_CONTEXT    chaîne utile pour contexte, non parser prioritaire
REJECTED      hors scope ou trop bruitée
```

## Modes de collecte

```text
latest              derniers contenus seulement
shorts_first        Shorts priorisés
keyword             filtrage par titres/descriptions
date_range          fenêtre temporelle
manual_seed         vidéos fournies manuellement
```

## Règles

- Une chaîne doit exister dans le registre avant batch.
- Le champ `parser_profile` est obligatoire.
- Les mots-clés limitent la collecte, ils ne remplacent pas la validation humaine.
- Le registre conserve les chaînes rejetées avec raison, pour éviter de les redécouvrir.

## Premier registre attendu

```text
registry/youtube_sources.jsonl
```

## NEXT_GO

Créer un child pilote `GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01` et y ajouter l'entrée `@trademachineoff`.