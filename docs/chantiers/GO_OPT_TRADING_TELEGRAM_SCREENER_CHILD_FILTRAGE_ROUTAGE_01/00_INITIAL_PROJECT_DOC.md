---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01
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
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01

## Objectif

Filtrage et routage des signaux Telegram Screener par canal/trust_tier/type.
Utilise le channel registry (channels.yaml + loader) pour déterminer si un signal
entrant doit être traité, ignoré, ou redirigé vers un traitement spécifique.

## 1_MASTER_TARGET

```text
filtrage et routage runtime : router layer entre parser et signal producer, piloté par channel registry
```

## 4_MASTER_PROJECT_PLAN

1. **Router interface** : définir `FilterRouter` qui prend un signal brut + channel metadata → décision de routage
2. **Filtrage par trust_tier** : A/B/C/D → passage/refus selon règle configurable
3. **Filtrage par catégorie** : ne router que les signaux dont la catégorie correspond au canal
4. **Filtrage par parser attendu** : ne router que les signaux dont le type correspond aux parsers déclarés du canal
5. **enabled flag** : ignorer les signaux des canaux désactivés
6. **Tests** : valider chaque règle de filtrage individuellement et en combinaison
7. **Intégration** : câbler le router dans l'appel entre parser et signal producer

## 12_INVARIANTS

- Aucun appel Telegram live
- Aucune modification des services existants en dehors du module telegram_screener
- Le channel registry est read-only (loader déjà validé)
- Les règles de filtrage sont testables sans réseau
- enabled=false par défaut pour tout nouveau canal

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01
```
