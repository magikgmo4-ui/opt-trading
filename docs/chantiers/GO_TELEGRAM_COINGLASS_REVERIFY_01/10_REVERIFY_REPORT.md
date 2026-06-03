# Re-vérification coinglass_alerts après parser transfer

**Generated:** 2026-06-03 05:30 UTC  
**Branch:** `go/GO_TELEGRAM_COINGLASS_REVERIFY_01`

## Résultat capture

| Métrique | Valeur |
|---|---|
| Messages | 20 |
| Parsed | **20/20** |
| Unknown | **0** |
| Noise | 0 |
| Score | 0.777 |
| Transfer present | Non (aucun message transfer dans cette fenêtre) |

## Vérification parser transfer

Test direct du parser sur le format `大额转账` :

```
Schema: telegram_transfer_candidate.v1
Asset: WBTC
Amount USD: 422638351.0
Status: PARTIAL (entities = unknown)
```

Le parser fonctionne. La capture n'a pas rencontré de message transfer dans cette fenêtre de 20 messages — normal, ces notifications sont sporadiques.
