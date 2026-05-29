# 40_GAPS_AND_NEXT_GO — GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01

## Gaps

| Gap | Traitement |
|---|---|
| Router non implémenté | Ce GO crée FilterRouter avec 5 règles de filtrage |
| Aucun test de routage | Ce GO crée 23 tests |

## Next GO

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01
```

Câblage intégral du pipeline : parser → router → signal producer → Desk Pro adapter.
Actuellement chaque étape est testable individuellement mais il n'existe pas d'orchestrateur
qui enchaîne les étapes automatiquement. Ce GO créerait un `ScreenerPipeline` ou un appel
unique qui prend un raw_text + channel_alias et produit un `telegram_claim.v1` final.

Condition : les 4 child GOs runtime (parser, signal producer, channel registry, router) mergés.
