---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_VISUAL_CONTEXT_CONTRACT
doc_type: visual_context_contract
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 30_VISUAL_CONTEXT_CONTRACT - Visual Context Contract V1

## Objet

Définir un contrat canonique `visual_context` V1 consumable par `desk_bridge`, `signal_event` (via ref) et Desk Pro, sans dépendre des noms de fichiers internes ou de la structure SFTP actuelle.

## JSON schema documentaire minimal

```json
{
  "type": "object",
  "required": [
    "source",
    "capture_id",
    "symbol",
    "timeframe",
    "captured_at",
    "image_ref",
    "status"
  ],
  "properties": {
    "source": {
      "type": "string",
      "enum": ["bot_vision_headless", "sharex", "manual"]
    },
    "capture_id": {
      "type": "string",
      "description": "Unique identifier for this capture, derived from filename or UUID"
    },
    "symbol": {
      "type": "string",
      "description": "Trading symbol, e.g. BTCUSDT.P, XAUUSD"
    },
    "timeframe": {
      "type": "string",
      "description": "Chart timeframe, e.g. H1, H4, D1"
    },
    "captured_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO-8601 UTC timestamp of capture"
    },
    "image_ref": {
      "type": "string",
      "description": "Path or URI to the PNG image"
    },
    "metadata_ref": {
      "type": ["string", "null"],
      "description": "Path or URI to the sidecar JSON"
    },
    "payload_hash": {
      "type": ["string", "null"],
      "description": "SHA-256 of the PNG content"
    },
    "chart_source": {
      "type": ["string", "null"],
      "description": "Origin chart provider, e.g. tradingview"
    },
    "status": {
      "type": "string",
      "enum": ["ready", "stale", "error", "uploading"],
      "description": "Processing status"
    },
    "errors": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of error messages if any"
    },
    "signal_event_ref": {
      "type": ["string", "null"],
      "description": "Optional reference to related signal_event"
    },
    "desk_snapshot_ref": {
      "type": ["string", "null"],
      "description": "Optional reference to resulting desk_snapshot"
    }
  }
}
```

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `source` | string | Producer identifier: `bot_vision_headless`, `sharex`, `manual` |
| `capture_id` | string | Unique capture ID (from filename timestamp or UUID) |
| `symbol` | string | Trading symbol |
| `timeframe` | string | Chart timeframe |
| `captured_at` | string (ISO-8601) | Capture timestamp |
| `image_ref` | string | Path/URI to PNG |
| `status` | string | `ready`, `stale`, `error`, `uploading` |

## Optional fields

| Field | Type | Description |
| --- | --- | --- |
| `metadata_ref` | string\|null | Path to sidecar JSON |
| `payload_hash` | string\|null | SHA-256 of PNG |
| `chart_source` | string\|null | Chart provider name |
| `errors` | array | Error messages |
| `signal_event_ref` | string\|null | Future link to signal_event |
| `desk_snapshot_ref` | string\|null | Future link to desk_snapshot |

## Error semantics

- `ready`: capture valid, image non-empty, sidecar written
- `stale`: capture older than expected freshness window (TBD, e.g. > 30min for H1)
- `error`: capture failed, image missing or corrupt, sidecar incomplete
- `uploading`: atomic write in progress (`.uploading` suffix present)

## Stale semantics

- Un `visual_context` est considéré `stale` si `captured_at` est antérieur à la fenêtre de fraîchesse attendue
- Pour H1: stale si > 30 minutes après la clôture de la bougie
- Pour H4: stale si > 2 heures
- Consumer (Desk Pro) ne doit pas prendre de décision trading sur un `visual_context` stale

## Zero-byte / .uploading semantics

- **0-byte**: le fichier est corrompu ou le write a été interrompu → `status=error`, ignorer
- **< 1KB**: le fichier est probablement invalide → `status=error`, ignorer
- **`.uploading`**: le write atomique est en cours → `status=uploading`, ne pas consommer
- Le producer (`capture_headless.js`) applique ces gardes avant rename atomique
- Le consumer (`desk_bridge`) applique aussi ces gardes avant traitement

## Timestamp semantics

- `captured_at` représente le moment exact de la capture screenshot (côté producer)
- Format: ISO-8601 UTC (`new Date().toISOString()`)
- Le timestamp dans le nom de fichier (`screen_{source}_{symbol}_{tf}_{ts}.png`) est le même que `captured_at`
- `desk_snapshot_ingest` extrait le timestamp du nom de fichier pour `snapshot_ts`

## Hash/ref semantics

- `payload_hash`: SHA-256 du contenu PNG, pour déduplication et intégrité
- `image_ref`: chemin absolu ou relatif au moment de l'ingestion
- `metadata_ref`: chemin vers le sidecar JSON co-produit
- Ces champs permettent le rattachement downstream sans re-parsing du nom de fichier

## Mapping sidecar JSON actuel → V1

| Sidecar actuel | V1 canonique | Transformation |
| --- | --- | --- |
| `producer` | `source` | renommage |
| `source` (chart provider) | `chart_source` | renommage |
| `symbol` | `symbol` | direct |
| `timeframe` | `timeframe` | direct |
| `created_at_utc` | `captured_at` | direct |
| `output_png` | `image_ref` | derive chemin |
| `output_json` | `metadata_ref` | derive chemin |
| `status` (`ready`) | `status` | direct |
| — | `capture_id` | derive du nom de fichier |
| — | `payload_hash` | calcul SHA-256 (non produit actuellement) |
| — | `signal_event_ref` | futur |
| — | `desk_snapshot_ref` | futur |

## Verdict de définition

`visual_context` V1 peut être défini proprement en l'état. Le sidecar JSON produit par `capture_headless.js` couvre les champs principaux. Les champs `payload_hash`, `capture_id`, `signal_event_ref` et `desk_snapshot_ref` sont ajoutables sans breaking change.
