# 50_DATA_CENTER_HANDOFF

## Objectif

Documenter le schema `max data out` du pipeline vision vers Data Center.

## Categories proposees

- `raw_capture`
- `visual_context`
- `vision_analysis`
- `extracted_signal`
- `generated_summary`
- `distribution_payload`

## Alignement avec les conventions Data Center du repo

Le handoff vision doit reutiliser autant que possible les conventions deja
visibles dans `market_metrics.v1` et dans les contrats producer Data Center :

- top-level `schema`
- top-level `input_class`
- `contract_version`
- `module_id`
- `produced_at`
- `refs`
- payload JSON stable, lisible par des consumers filesystem et DeskPro

Le producer contract existant documente aussi un layout `data/data_center/<producer>/`
avec `raw/`, `normalized/`, `latest.json`, `manifest.json`, `status.json`.

## Positionnement recommande

### 1. Payload Data Center canonique

Le pipeline bot vision devrait produire un payload principal de type :

- `schema = vision_pipeline_payload.v1`
- `input_class = vision_pipeline_payload.v1`

Ce payload principal peut ensuite alimenter :

- une vue Data Center neutre
- une extraction `visual_context` pour DeskPro dry-run
- une extraction `vision_analysis.v1` pour DeskPro
- une extraction `vision_context.<source>.v1` specialisee quand une source a deja
  un consumer dedie, comme `vision_context.coinglass.v1`

### 2. Derives compatibles DeskPro

Pour garder la compatibilite avec les consumers existants, le handoff doit
pouvoir produire ou deriver :

- `visual_context` avec les champs requis par `load_latest_visual_context()`
- `vision_analysis.v1` avec le resume exploitable
- `vision_context.coinglass.v1` pour le panel vision Coinglass quand applicable

## Schéma max data out recommandé

### Top-level

| Champ | Description |
|---|---|
| `schema` | contrat Data Center canonique, propose: `vision_pipeline_payload.v1` |
| `input_class` | meme valeur que `schema` pour lecture consumer simple |
| `contract_version` | version du contrat (`v1`) |
| `module_id` | producteur logique, ex. `bot_vision_headless` |
| `producer_id` | producteur runtime ou source specialisee |
| `produced_at` | timestamp ISO UTC du handoff |
| `capture_timestamp` | timestamp ISO UTC de la capture source |
| `source_url` | origine de la capture |
| `source_id` | identifiant source canonique |
| `asset_scope` | assets / indices / screener concernes |
| `refs` | refs vers images, runs, manifests, files |
| `freshness_state` | fresh / stale / unknown |
| `confidence` | confiance globale du payload |

### Bloc `raw_capture`

| Champ | Description |
|---|---|
| `capture_id` | identifiant unique de capture |
| `image_ref` | chemin ou URI image raw |
| `annotated_image_ref` | image annotee si generee |
| `viewport` | viewport applique |
| `capture_mode` | full-page / crop / multi-capture |
| `sections` | zones capturees |
| `file_size_bytes` | garde-fou anti 0-byte |
| `sha256` | hash optionnel d'integrite |

### Bloc `visual_context`

Ce bloc doit rester compatible avec DeskPro dry-run.

| Champ | Description |
|---|---|
| `source` | source logique de la capture |
| `capture_id` | ref de jointure |
| `symbol` | symbole principal |
| `timeframe` | timeframe visible ou deduite |
| `captured_at` | timestamp de capture |
| `image_ref` | image de reference |
| `status` | ok / partial / failed |

### Bloc `vision_analysis`

| Champ | Description |
|---|---|
| `input_class` | `vision_analysis.v1` si payload derive |
| `analysis_type` | OCR / setup / heatmap / mixed |
| `summary` | resume texte court |
| `setup_bias` | bull / bear / neutral / mixed |
| `key_levels` | niveaux extraits |
| `detections` | detections structurees |
| `warnings` | alertes de confiance / ambiguite |
| `confidence` | confiance analyse |

### Bloc `generated_outputs`

| Champ | Description |
|---|---|
| `raw_image_available` | image raw presente |
| `annotated_image_available` | image annotee presente |
| `textual_analysis` | analyse textuelle longue ou courte |
| `setup_summary` | resume setup court |
| `telegram_payload` | payload de distribution potentiel |
| `deskpro_payload` | projection resumee pour DeskPro |

### Bloc `distribution_payload`

| Champ | Description |
|---|---|
| `telegram` | message ou structure outbound Telegram |
| `deskpro` | bloc d'affichage ou de jointure DeskPro |
| `data_center_views` | vues ciblees a publier |

## Exemple de shape propose

```json
{
  "schema": "vision_pipeline_payload.v1",
  "input_class": "vision_pipeline_payload.v1",
  "contract_version": "v1",
  "module_id": "bot_vision_headless",
  "producer_id": "coinglass_headless_bot",
  "produced_at": "2026-05-29T12:00:00Z",
  "capture_timestamp": "2026-05-29T11:59:30Z",
  "source_id": "coinglass_heatmap",
  "source_url": "https://...",
  "asset_scope": ["BTC", "ETH"],
  "freshness_state": "fresh",
  "confidence": 0.84,
  "refs": {
    "image_ref": "data/vision/...png",
    "annotated_image_ref": "data/vision/...annotated.png",
    "manifest_ref": "data/data_center/.../manifest.json"
  },
  "raw_capture": {
    "capture_id": "cap_...",
    "viewport": {"width": 1440, "height": 2200},
    "capture_mode": "multi-capture",
    "sections": ["heatmap", "liquidations", "oi"]
  },
  "visual_context": {
    "source": "coinglass_headless_bot",
    "capture_id": "cap_...",
    "symbol": "BTC",
    "timeframe": "H1",
    "captured_at": "2026-05-29T11:59:30Z",
    "image_ref": "data/vision/...png",
    "status": "ok"
  },
  "vision_analysis": {
    "input_class": "vision_analysis.v1",
    "analysis_type": "heatmap+ocr",
    "summary": "Liquidation cluster above price, OI rising.",
    "setup_bias": "bull",
    "key_levels": [108500, 109200],
    "detections": []
  },
  "generated_outputs": {
    "textual_analysis": "...",
    "setup_summary": "...",
    "telegram_payload": {"enabled": false},
    "deskpro_payload": {"panel": "vision"}
  }
}
```

## Règles de dérivation recommandées

1. Le payload principal doit etre preservable tel quel dans Data Center.
2. `visual_context` doit pouvoir etre extrait sans appel externe.
3. `vision_analysis.v1` doit pouvoir etre publie comme payload derive si DeskPro
   ou d'autres consumers le lisent directement.
4. Une source specialisee peut publier un payload secondaire, ex.
   `vision_context.coinglass.v1`, si un consumer existant l'exige deja.
5. Les refs images et manifests doivent toujours rester resolvables localement.

## Contrat minimal

| Champ | Description |
|---|---|
| source_url | origine de la capture |
| capture_timestamp | horodatage |
| asset_scope | assets / indices / screener concernes |
| capture_ref | reference de l'image source |
| extracted_data | champs structures extraits |
| generated_outputs | sorties derivees |
| confidence | niveau de confiance |
| schema_version | version du payload |

## TODO

- `DATA_CENTER_MAX_DATA_OUT_SCHEMA`
- choisir si `vision_pipeline_payload.v1` devient schema canonique ou simple schema de travail
- decider quelles vues Data Center exposeront le payload principal vs les payloads derives
