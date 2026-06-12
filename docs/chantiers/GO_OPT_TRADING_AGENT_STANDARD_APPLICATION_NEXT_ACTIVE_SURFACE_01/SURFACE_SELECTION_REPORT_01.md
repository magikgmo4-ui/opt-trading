# GO_OPT_TRADING_AGENT_STANDARD_APPLICATION_NEXT_ACTIVE_SURFACE_01

## Surfaces candidates

| Surface | OpenClaw agent | Docs existantes | Priorité |
|---------|:--------------:|:---------------:|:--------:|
| Student/Ollama | ✅ FULLY_CLOSED | ✅ | — (déjà fait) |
| Admin/Trading Desk Pro | ❌ | ✅ runbooks | 2 |
| DB Layer | ❌ | ✅ runbooks | 3 |
| Cursor AI | ❌ | ❌ | 4 |

## Sélection

Surface retenue : **Admin/Trading Desk Pro**.

Justification :
- Dispose déjà de runbooks et documentation opératoire
- Surface active avec des besoins d'automatisation documentés
- Pas de conflit avec le runtime Student/Ollama existant
- Applicable sans rouvrir la chaîne Student/Ollama

## Prochaine action

Ouvrir un chantier dédié pour auditer et configurer l'agent OpenClaw sur Admin/Trading Desk Pro si pertinent, ou documenter pourquoi cette surface ne nécessite pas d'agent.

## Verdict

```
NEXT_SURFACE_SELECTED: ADMIN_TRADING_DESK_PRO
```

Le standard Student/Ollama reste fermé. La prochaine application est sur Admin/Trading Desk Pro si besoin validé.

## RISKS

- À qualifier.
