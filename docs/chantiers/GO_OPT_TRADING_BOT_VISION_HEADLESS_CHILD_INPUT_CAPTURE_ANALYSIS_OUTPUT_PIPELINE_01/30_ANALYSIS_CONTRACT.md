# 30_ANALYSIS_CONTRACT

## Objectif

Definir comment la couche d'analyse transforme les screenshots en donnees
lisibles, classifiees et reutilisables.

## Couches d'analyse

- OCR / lecture visuelle
- detection de contenu
- extraction de signaux, niveaux, tendance, setup
- classification du type de contenu

## Shapes deja etablis dans le repo

### Vision context Coinglass

Le shape deja consomme par DeskPro pour `vision_context.coinglass.v1` contient :

- `contract_version`
- `input_class`
- `source_id`
- `screenshot_ts`
- `symbol`
- `timeframe`
- `board`
- `page`
- `freshness_state`
- `detections`
- `warnings`
- `refs`

### Shape des detections etabli

Les tests DeskPro fixent deja la forme suivante pour chaque detection :

| Champ | Description |
|---|---|
| `detected_metric_type` | type de metrique ou signal detecte |
| `extracted_value` | valeur extraite ou `null` |
| `unit` | unite (`USD`, etc.) |
| `confidence` | float `0.0 - 1.0` |
| `evidence_ref` | ref vers image ou preuve |
| `notes` | details libres |

Metriques deja observees :

- `liquidations_long`
- `liquidations_short`
- `long_short_ratio`
- `open_interest`
- `liquidation_heatmap_level`

## Types d'analyse recommandes pour le pipeline elargi

| `analysis_type` | Usage |
|---|---|
| `ocr` | lecture texte simple |
| `chart_setup` | analyse chart / niveaux / biais |
| `heatmap` | lecture heatmap / flow / cluster |
| `macro_panel` | synthese dashboard macro |
| `mixed` | plusieurs modes sur une meme capture |

## Regles de confiance

- seuil bas utile deja etabli dans le repo : `confidence < 0.60`
- Coinglass Telegram summary :
  - `confidence < 0.85` -> warning explicite
  - `confidence < 0.60` -> low confidence
- recommandation pipeline :
  - `< 0.60` : detection non fiable, ne pas promouvoir en signal exploitable
  - `0.60 - 0.84` : detection usable avec warning
  - `>= 0.85` : detection forte

## Contrat de sortie recommande

### Bloc `vision_analysis`

| Champ | Description |
|---|---|
| `input_class` | `vision_analysis.v1` |
| `capture_id` | jointure avec la capture |
| `source_id` | source logique |
| `symbol` | symbole principal |
| `timeframe` | timeframe visible ou deduite |
| `analysis_type` | type d'analyse |
| `summary` | resume texte court |
| `setup_bias` | `bull`, `bear`, `neutral`, `mixed` |
| `key_levels` | liste de niveaux extraits |
| `detections` | liste structuree de detections |
| `warnings` | liste de warnings |
| `confidence` | confiance globale |

### Shape recommande pour une detection elargie

```json
{
  "detected_metric_type": "open_interest",
  "extracted_value": 126069243.0,
  "unit": "USD",
  "confidence": 1.0,
  "evidence_ref": "data/vision/coinglass/raw/screenshot.png",
  "notes": "ocr exact",
  "zone_id": "oi_top_right",
  "source_kind": "heatmap"
}
```

## Regles de derivation

1. Une capture peut produire zero, une ou plusieurs detections.
2. `extracted_value = null` doit rester permis mais ne doit pas etre promu en metrique DeskPro.
3. Les detections doivent rester tracables vers une preuve image via `evidence_ref`.
4. La `confidence` globale d'analyse ne doit pas exceder arbitrairement la meilleure preuve disponible.

## Format de sortie vise

- raw_capture_reference
- extracted_signal
- generated_summary
- distribution_payload

## Mapping source -> payload derive -> consumer

| Source | Payload derive principal | Consumer cible |
|---|---|---|
| Coinglass heatmap / liquidations | `vision_context.coinglass.v1` | DeskPro vision panel + metrics reader |
| TradingView chart | `visual_context` + `vision_analysis.v1` | DeskPro dry-run / vues futures |
| Macro dashboard | `vision_analysis.v1` + payload Data Center | DeskPro synthese / contexte |
