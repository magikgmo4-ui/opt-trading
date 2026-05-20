---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_DESKPRO_INPUT_EXPANSION_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener -> Desk Pro
- Telegram inbound screener -> claims -> Desk Pro
- Telegram outbound notification multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- inputs réels Desk Pro recensés (desk_snapshot, signal_event, visual_context)
- classes d’inputs cibles posées (vision_analysis, market_metrics, telegram_claim)
- contraintes de jointure et preuves minimales fixées

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat :

```text
31 passed in 78.89s
```

## Lecture minimale

1. `20_TARGET_INPUT_CLASSES.md`
2. `30_PROOF_MATRIX_AND_CONSTRAINTS.md`
3. `40_GAPS_AND_NEXT_GO.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q
```

## Next GO bundle

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du hub consumer Desk Pro dans la
chaine du produit final total.

## Prochain item Kanban exact

`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01`

## Gaps encore ouverts

- wrappers read-only non encore poses
- `vision_analysis`, `market_metrics`, `telegram_claim` encore contractuels seulement
- refs/timestamps de jointure encore incomplets selon les producers
- aucune ecriture Google Sheets transverse n'est ouverte a ce stade
