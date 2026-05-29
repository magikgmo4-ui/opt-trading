---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
pf_id: PF_TELEGRAM_SCREENER
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - PF_TELEGRAM_INGESTION
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01

## Objectif

Câbler les 5 étapes du pipeline Telegram Screener en un appel unique :
`raw_text + channel_alias → ScreenerSignal → RouteDecision → ScreenerProducedSignal → telegram_claim.v1`

Actuellement chaque étape est testable individuellement mais il n'existe pas d'orchestrateur.

## 1_MASTER_TARGET

```text
ScreenerPipeline : orchestrateur qui enchaîne parser → router → signal producer → Desk Pro adapter
```

## 4_MASTER_PROJECT_PLAN

1. **Pipeline interface** : définir `ScreenerPipeline.run(raw_text, channel_alias, ...) → dict`
2. **Wiring** : enchaîner parse → route → produce → adapt
3. **Error handling** : gérer les échecs à chaque étape (parse None, route reject, etc.)
4. **Tests** : valider le pipeline complet avec des entrées réelles (trade, news, alpha)
5. **Fixtures** : tests d'intégration avec les 3 types de signaux

## 12_INVARIANTS

- Aucun appel Telegram live
- Aucune modification des 5 modules existants (parser, registry, router, signal, adapters)
- Tous les tests sont unitaires ou d'intégration sans réseau
- Le pipeline peut être appelé sans effet de bord (pure function)

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01
```
