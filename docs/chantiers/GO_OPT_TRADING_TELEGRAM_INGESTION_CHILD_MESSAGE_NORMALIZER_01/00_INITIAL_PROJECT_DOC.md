---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01
pf_id: PF_TELEGRAM_INGESTION
status: open
lifecycle_stage: implementation
surface: modules/telegram_ingestion
source_kind: canonical
created_at: 2026-05-29
updated_at: 2026-05-29
upstream:
  - GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_RUNTIME_01
links:
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01/10_INBOUND_SPEC.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01

## Objectif

Implémenter le normalizer de messages Telegram inbound : détection de type (text/image/poll/link), extraction de métadonnées (mentions, hashtags, links), production d'InboundMessage normalisé.

Prend RawMessage en entrée, produit InboundMessage normalisé en sortie.

## 1_MASTER_TARGET

```text
MessageNormalizer : RawMessage → InboundMessage avec détection de type + extraction métadonnées
```

## 4_MASTER_PROJECT_PLAN

1. **Type detection** : classifier le message (text/image/poll/link) selon raw_text + sender
2. **Metadata extraction** : extraire mentions, hashtags, URLs du raw_text
3. **Normalizer orchestrator** : `normalize(raw: RawMessage) → InboundMessage` avec type + metadata
4. **Tests** : couvrir text, image, poll, link + edge cases (empty, no metadata)

## 12_INVARIANTS

- Aucun appel réseau
- Aucune modification de l'inbound parser existant
- Aucune dépendance Telethon
- Tous les tests unitaires sans side-effect

## 17_RESUME_POINT

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01
```
