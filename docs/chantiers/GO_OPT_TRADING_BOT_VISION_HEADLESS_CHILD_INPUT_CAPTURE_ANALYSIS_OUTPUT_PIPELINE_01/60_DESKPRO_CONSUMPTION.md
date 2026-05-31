# 60_DESKPRO_CONSUMPTION

## Objectif

Documenter ce que DeskPro attend reellement en consommation de la chaine vision
headless.

## Questions de contrat

- quels champs sont necessaires
- quel niveau de detail est utile
- quelles vues finales doivent etre alimentees
- quels outputs sont affiches tels quels vs resumes

## Entrants reels deja visibles dans le repo

| Input DeskPro | Chemin / source | Contrat actuel observe |
|---|---|---|
| `vision_context.coinglass.v1` | `data/deskpro/inputs/vision_context/coinglass/latest.json` | lu par `read_vision_context_coinglass()` et `read_vision_panel_data()` |
| `vision_analysis.v1` | `data/deskpro/inputs/vision_analysis/latest.json` | lu par `read_vision_analysis()` |
| `telegram_claim.v1` | `data/deskpro/inputs/telegram_claim/latest.json` | lu par `read_telegram_claim()` |
| `visual_context` dry-run | chargeur `load_latest_visual_context()` | exige `source`, `capture_id`, `symbol`, `timeframe`, `captured_at`, `image_ref`, `status` |
| `desk_snapshot.v1` | snapshot index consumer | exige `symbol`, `tf`, `snapshot_ts`, `path` |

## Ce que DeskPro sait deja consommer

### Vision context → metrics

Le reader `read_vision_context_coinglass()` convertit des detections vision en
`Metric` DeskPro avec les dimensions suivantes :

- `source`
- `asset`
- `metric`
- `value`
- `unit`
- `window`
- `quality`
- `notes`

Les metriques deja reconnues cote vision Coinglass sont :

- `liquidations_long`
- `liquidations_short`
- `long_short_ratio`
- `open_interest`
- `liquidation_heatmap_level`

### Vision panel UI

Le panel vision DeskPro attend deja :

- `input_class = vision_context.coinglass.v1`
- `screenshot_ts`
- `detections`
- un etat lisible `ok/reason`
- une fraicheur calculable `age_hours`

### Dry-run synthesis / join contract

Le pipeline dry-run DeskPro sait joindre les couches suivantes :

- `signal_event`
- `visual_context`
- `desk_snapshot`
- `market_metrics`
- `vision_analysis`
- `telegram_claim`

Checks explicites deja presents :

- match `symbol` entre signal, snapshot et visual context
- match `timeframe` entre signal et snapshot
- `visual_context_ref` coherent avec `capture_id`

## Cibles produit

- snapshot exploitable
- analyse lisible
- setup card resumee
- lien vers image raw / annotee
- data structurée reutilisable dans d'autres vues

## Contrat minimal recommande pour le pipeline bot vision

### 1. Couche visual_context

Champs minimaux a produire pour etre joignable par DeskPro dry-run :

- `source`
- `capture_id`
- `symbol`
- `timeframe`
- `captured_at`
- `image_ref`
- `status`

### 2. Couche vision_analysis

Champs recommandes :

- `input_class = vision_analysis.v1`
- `capture_id`
- `symbol`
- `timeframe`
- `analysis_type`
- `summary`
- `setup_bias`
- `key_levels`
- `confidence`
- `warnings`

### 3. Couche generated outputs

Outputs que DeskPro doit pouvoir referencer ou afficher :

- image raw
- image annotee
- resume analytique
- setup summary
- eventuel payload Telegram derive

## Vue finale ciblee cote DeskPro

DeskPro devrait pouvoir afficher ou reutiliser :

- un bloc freshness / status de la capture
- une image de reference
- une synthese textuelle courte
- des metriques structurees convertibles en `Metric`
- des niveaux / setups exploitables par score ou decision
- des warnings de confiance / mismatch source

## TODO

- `DESKPRO_CONSUMPTION_CONTRACT`
- valider quelles vues `/desk/ui` ou endpoints API exposeront chaque couche
- valider si `vision_context` et `vision_analysis` restent separes ou fusionnes en aval
