---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_REGISTRY_SCHEMA_TARGET
doc_type: schema
repo: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_REGISTRY_SCHEMA_TARGET - Schéma cible registry channels

## Objectif

Définir un fichier de registry (doc-only) qui liste les sources Telegram inbound autorisées, leur niveau de confiance, et les parsers attendus.

## Format cible (YAML)

Fichier candidat:

```text
registry/telegram_screener_channels.yaml
```

Schéma V1:

```yaml
version: 1
updated_at: "2026-05-19"
channels:
  - channel_id_alias: "TG_SRC_EXAMPLE_01"
    kind: "channel" # channel|group|supergroup
    title: "Example Channel Name"
    trust_tier: "C" # A|B|C|D
    categories:
      - "signals"
      - "macro"
    expected_parsers:
      - "trade_claim"
      - "setup"
      - "news"
    symbols_scope:
      - "BTCUSDT"
      - "ETHUSDT"
    timeframes_scope:
      - "1h"
      - "4h"
    allow_forwarded: false
    allow_media: true
    enabled: false
    notes: "doc-only placeholder; no hardcoded ids"
```

## Résolution des IDs

- `channel_id_alias` est résolu via variables d’environnement (ex: `TG_SRC_EXAMPLE_01=<numeric_id>`).
- Aucun id réel dans le repo.

## Gouvernance minimale

- `trust_tier=A/B` seulement pour sources “validated”
- `enabled=true` uniquement après preuve d’observation (dry-run + fixtures)
