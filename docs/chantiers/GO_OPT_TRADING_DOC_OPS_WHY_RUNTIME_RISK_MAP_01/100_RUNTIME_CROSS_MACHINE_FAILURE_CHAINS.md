# 100_RUNTIME_CROSS_MACHINE_FAILURE_CHAINS

## Objectif

Formaliser les chaines de defaillance multi-machine.

## Chaines critiques

### TradingView -> webhook -> Telegram

| Etape | Machine | Risque |
| --- | --- | --- |
| TradingView alert | externe | signal perdu |
| webhook runtime | admin-trading | runtime indisponible |
| Telegram notification | admin-trading | perte observabilite |

### ShareX -> bot vision -> ingestion desk

| Etape | Machine | Risque |
| --- | --- | --- |
| capture ShareX | cursor-ai | capture manquante |
| bridge vision | admin-trading | transfert casse |
| ingestion snapshots | admin-trading | stale state |

### OpenClaw orchestration

| Etape | Machine | Risque |
| --- | --- | --- |
| provider routing | db-layer | mauvais routage |
| orchestration | db-layer | supervision degradee |
| consumers downstream | multi-machine | propagation erreur |

## Invariant

Toute chaine critique devrait:
- etre observable,
- etre reprise,
- avoir des gates,
- documenter les points de rupture.
