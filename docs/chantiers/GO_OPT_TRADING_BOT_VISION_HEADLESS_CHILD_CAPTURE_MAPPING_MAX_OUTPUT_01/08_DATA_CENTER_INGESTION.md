# 08 — Data Center Ingestion

## Vue d'ensemble

Le Data Center a une architecture deux couches :
1. **Couche producteur** : chaque module écrit dans son répertoire dédié
2. **Couche vue** : chemins neutres découplés du producteur

Pour vision_analysis, on écrit directement dans la couche vue (pas de producteur dédié — le pipeline bot_vision n'est pas un collecteur régulier).

## Chemins

```
data/data_center/views/vision_analysis/
├── latest.json                    # Dernière analyse (écrasé à chaque run)
├── by_symbol/
│   ├── BTCUSDT.P.json
│   ├── ETHUSDT.P.json
│   └── ...                        # Dernier résultat par symbole
└── history/
    ├── BTCUSDT.P_2026-05-30_12-00-00.json
    └── ...                        # Historique des analyses
```

## Format

Même format que DeskPro (`vision_analysis.v1`). Le writer `vision_analysis_writer.py` copie atomiquement le même payload vers les deux destinations.

## Registre producteur

À ajouter dans `modules/data_center/registry/producers.json` :

```json
{
  "bot_vision_headless": {
    "family": "vision",
    "producer_id": "bot_vision_headless",
    "produces": ["vision_analysis.v1"],
    "source": "modules/bot_vision/headless_capture/"
  }
}
```

## Registre consommateur

DeskPro lit déjà depuis `data/deskpro/inputs/vision_analysis/latest.json` via `vision_analysis_reader.py`. Pour lire depuis le Data Center, ajouter à `modules/data_center/registry/consumers.json` :

```json
{
  "desk_pro__vision_analysis_from_dc": {
    "consumer_id": "desk_pro__vision_analysis",
    "reads": "views/vision_analysis/latest.json",
    "contract": "vision_analysis.v1"
  }
}
```

## État actuel

- L'écriture DeskPro (data/deskpro/inputs/vision_analysis/latest.json) est fonctionnelle
- L'écriture Data Center est implémentée dans vision_analysis_writer.py
- Le registre producteur/consommateur N'EST PAS mis à jour dans ce GO (nécessite modification des index globaux, hors scope)
