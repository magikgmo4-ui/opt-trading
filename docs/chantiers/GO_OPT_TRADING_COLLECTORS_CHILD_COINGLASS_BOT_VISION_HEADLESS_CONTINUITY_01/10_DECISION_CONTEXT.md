---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_DECISION_CONTEXT
doc_type: decision_context
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_DECISION_CONTEXT

## Décision source

PR #707 — `20_ACCEPTANCE_REPORT.md` du parent `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` :

> Coinglass est un service payant. Aucun adapter API runtime ne sera implémenté dans ce chantier. Les données de liquidations Coinglass seront produites par un **bot vision headless** externe. Le statut `not_proven_runtime_adapter` est maintenu de façon permanente pour Coinglass dans le contrat `market_metrics.v1`.

## Pourquoi Coinglass via bot vision et non API

| Critère | API Coinglass | Bot vision headless |
|---|---|---|
| Coût | Payant (abonnement) | Gratuit si self-hosted |
| Latence | Faible | Modérée (capture + OCR) |
| Fiabilité | Haute (JSON structuré) | Dépend du layout |
| Maintenabilité | Stable (API versionnée) | Fragile si UI change |
| Usage trading | Contexte liquidations / LSR | Idem, mais confiance partielle |
| Justification ici | Non retenu — coût | Retenu pour instant |

## Ce que le bot vision headless doit produire

Le bot capture des screenshots de l'interface Coinglass (tableau de liquidations, LSR, heatmap) et extrait les valeurs pertinentes via OCR ou vision LLM. La sortie est un contrat structuré `vision_context.coinglass.v1` — distinct de `market_metrics.v1`.

## Ce que le bot vision NE doit pas faire

- Inventer des valeurs non lisibles dans le screenshot
- Passer pour un provider API runtime
- Écrire directement dans `data/derivatives/` ou dans le contrat `market_metrics.v1`
- Déclencher des décisions de trading sans validation humaine intermédiaire

## Statut Coinglass dans `market_metrics.v1`

`NOT_PROVEN_RUNTIME_ADAPTER` — permanent. Même si des données Coinglass deviennent disponibles via bot vision, elles transitent par `vision_context.coinglass.v1`, pas par `market_metrics.v1`.

## Séparation des surfaces

```text
market_metrics.v1          ← providers API prouvés (Binance FULL, Bitget FULL)
vision_context.coinglass.v1 ← bot vision headless (source visuelle externe)
```

Desk Pro peut consommer les deux, mais via des inputs distincts et des confidence scores différents.
