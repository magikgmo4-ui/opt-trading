---
doc_id: GO_EVENT_TAXONOMY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_EVENT_TAXONOMY_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram inbound screener
- Telegram outbound notification
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- L’enveloppe canonique V1 est définie (read-only).
- Les familles et types cibles sont mappés sur les payloads existants (dataclasses + dicts).
- Aucun changement runtime requis dans ce GO.

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\test_signal_event_adapter.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat :

```text
61 passed in 78.80s
```

## Lecture minimale

1. `20_CANONICAL_EVENT_ENVELOPE.md`
2. `30_EVENT_FAMILY_MAPPING.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO (bundle)

```text
GO_TELEGRAM_EVENT_ROUTING_MAP_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local de la taxonomie transverse dans la
chaine du produit final total.

## Prochain item Kanban exact

`GO_TELEGRAM_EVENT_ROUTING_MAP_01`

## Gaps encore ouverts

- intents outbound Telegram encore heterogenes entre dispatcher et helper
- policy de routing par famille d'evenements a concretiser dans le GO suivant
- raccord futur des surfaces inbound Telegram encore ouvert
- propagation de l'enveloppe vers Sheets / Perf / Registry encore a verifier
