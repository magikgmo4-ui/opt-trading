---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_DESKPRO
doc_type: deskpro_consumption
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 60_DESKPRO_CONSUMPTION.md

Besoins DeskPro côté consommation : format, granularité, champs.

## 1_CONTRAT_DESKPRO

DeskPro est le consommateur final des données produites par le pipeline. Il doit pouvoir :

- Afficher les dernières analyses par actif
- Naviguer dans l'historique des captures
- Voir les setups actifs / passés
- Rechercher par actif, type, date, signal
- Recevoir des notifications de signaux forts

## 2_FORMATS_CONSOMMES_PAR_DESKPRO

| Format | Source | Usage DeskPro |
|--------|--------|---------------|
| `desk_snapshot` V1 | Pipeline headless (via desk_snapshot_ingest) | Affichage snapshot par actif |
| `visual_context` V1 | Analyse du snapshot | Contexte visuel associé |
| `vision_analysis` (nouveau) | Pipeline enrichi | Signaux, niveaux, setup |
| `signal_event` V1 | Decision engine / webhook | Signal trading corrélé |
| `setup_card` (nouveau) | Pipeline enrichi | Setup cards dans DeskPro |

## 3_CHAMPS_ATTENDUS_PAR_DESKPRO

Pour chaque actif suivi, DeskPro a besoin de :

| Champ | Source | Priorité | Disponible V1 ? |
|-------|--------|----------|-----------------|
| Dernière image raw | Capture | P0 | Oui (desk_snapshot) |
| Dernière analyse texte | Analyse | P0 | Partiel (visual_context) |
| Signaux détectés | Analyse | P0 | Non |
| Niveaux S/R | Analyse | P0 | Non |
| Setup actif | Setup pipeline | P0 | Non |
| Risk flags | Analyse | P1 | Non |
| Trend direction | Analyse | P1 | Non |
| Timeframe analysis | Capture | P1 | Oui (desk_snapshot) |
| Corrélation macro | Analyse | P2 | Non |
| Historique 24h | DC query | P1 | Non |

## 4_FLUX_DESKPRO_VISE

```
Pipeline headless
  ↓
Capture + Analyse
  ↓
desk_snapshot_ingest (existant) → desk/snapshots/latest.json + {symbol}.latest.json
  ↓
vision_analysis.json (nouveau) → desk/analysis/{capture_id}.json
  ↓
setup_card.json (nouveau) → desk/setups/active.json
  ↓
DeskPro lit depuis desk/analysis/ + desk/setups/ + desk/snapshots/
```

## 5_GAP_ANALYSE_VS_CONTRATS_EXISTANTS

| Contrat existant | Pipeline V1 | Pipeline enrichi (cible) | Gap |
|-----------------|-------------|-------------------------|-----|
| desk_snapshot V1 | ✅ image + metadata | ✅ image + metadata enrichis | Faible (ajouter analysis_ref) |
| visual_context V1 | ✅ summary + levels | ✅ summary enrichi + signaux + setup | Moyen (ajouter signals, setup, risk_flags) |
| signal_event V1 | ✅ signal trading | ✅ signal enrichi par analyse vision | Faible (enrichir event avec vision_ref) |
| Nouveau : vision_analysis | — | ✅ Analyse complète | Nouveau contrat à créer |
| Nouveau : setup_card | — | ✅ Setup card | Nouveau contrat à créer |

## 6_VUES_DESKPRO_CYBLEES

| Vue | Données consommées | Usage |
|-----|-------------------|-------|
| Dashboard actifs | Dernière analyse par actif (tous timeframes) | Vue d'ensemble rapide |
| Détail actif | Analyse + image + niveaux + setup | Analyse approfondie |
| Setup watch | Setups actifs tous actifs confondus | Suivi des setups ouverts |
| Timeline | Historique analyses + événements 24h | Relecture de session |
| Macro view | Analyses BTC / Gold / DXY / Oil corrélées | Vue macro intégrée |
| Screener | Stocks screeners clusters | Rotation sectorielle |

## 7_FORMAT_VISION_ANALYSIS_POUR_DESKPRO

```json
{
  "symbol": "BTCUSDT",
  "asset_class": "crypto",
  "timeframe": "15m",
  "last_updated_utc": "2026-05-29T00:00:00Z",
  "latest_capture_id": "uuid",
  "image_path": "desk/snapshots/btcusdt_latest.png",
  "analysis": {
    "summary": "BTC teste résistance avec volume",
    "trend": "bullish",
    "signals": ["breakout_attempt"],
    "levels": {"support": [104000], "resistance": [106500]},
    "risk_flags": ["funding elevated"]
  },
  "setup_active": null,
  "analysis_available": true
}
```

## 8_FORMAT_SETUP_CARD_POUR_DESKPRO

```json
{
  "setup_id": "uuid",
  "symbol": "BTCUSDT",
  "direction": "long",
  "entry_zone": [104500, 105000],
  "stop_loss": 103200,
  "targets": [106500, 108000, 110000],
  "conviction": "high",
  "timeframe": "4h",
  "generated_at_utc": "2026-05-29T00:00:00Z",
  "status": "active|hit_tp1|stopped|cancelled",
  "capture_id": "uuid",
  "image_path": "desk/snapshots/btcusdt_setup.png"
}
```

## 9_INTEGRATION_AVEC_DESKPRO_RUNTIME

- Chemin fichier : `desk/analysis/{symbol}.latest.json` (écrasé à chaque nouvelle analyse)
- Chemin historique : `desk/analysis/history/{symbol}/{date}/{capture_id}.json`
- Chemin setups : `desk/setups/active.json` + `desk/setups/history/{setup_id}.json`
- DeskPro runtime doit être notifié (polling ou inotify) des mises à jour
