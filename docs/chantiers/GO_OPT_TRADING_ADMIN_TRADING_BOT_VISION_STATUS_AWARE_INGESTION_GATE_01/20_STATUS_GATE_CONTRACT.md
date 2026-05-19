# 20_STATUS_GATE_CONTRACT

## Règles de gate

| Status sidecar | vision_bot | bridge | ingest | Comportement |
|---|---|---|---|---|
| `ready` | process normal | crop + push | ingest normal | Flux Desk OK |
| `invalid_visual` | → rejected/ | skip | skip | Pas de promotion Desk |
| `blocked` | → rejected/ | skip | skip | Audit JSON only |
| absent (legacy) | process normal | push normal | ingest normal | Backward compatible |

## Comportement rejected

Les fichiers `invalid_visual` et `blocked` sont déplacés vers `processed/rejected/` :

```
vision_processed/
  rejected/
    screen_tradingview_XAUUSD_H1_2026-05-19_05-02-12.png
    screen_tradingview_XAUUSD_H1_2026-05-19_05-02-12.json
    screen_coinglass_BTCUSDT.P_FLOW_2026-05-19_05-02-51.json
```

Le PNG `invalid_visual` est conservé (pas de suppression).

## Sans sidecar

Si un PNG n'a pas de fichier `.json` compagnon, il est traité normalement. Cela préserve la compatibilité avec les workflows legacy.

## Orphelins blocked

Les JSON `blocked` sans PNG correspondant sont nettoyés par `vision_bot.py` vers `rejected/` en fin de cycle.
