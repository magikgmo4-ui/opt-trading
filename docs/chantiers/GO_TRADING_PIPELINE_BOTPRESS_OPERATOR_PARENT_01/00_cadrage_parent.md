---
doc_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01_CADRAGE
doc_type: cadrage_parent
repo: opt-trading
go_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
status: open
lifecycle_stage: cadrage
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 00_CADRAGE_PARENT — Botpress Operator

## 1_MASTER_TARGET

Faire de Botpress le routeur conversationnel controle du pipeline trading:

```
Telegram Screener → Botpress Operator → OpenClaw Gateway → student/Trading Labs → LONA/opt-trading → retour Telegram
```

## 3_INITIAL_NEED

Apres ClickUp (cockpit), Repo KG (cartographie) et Airtable (data leger), la 4e phase apps est Botpress: operateur conversationnel pour connecter Telegram, OpenClaw, surfaces trading et retour utilisateur.

## 6_FINAL_TARGET V1

- Classification d'intention Telegram (screener, statut, analyse, journal)
- Safety gate bloquant tout trade reel automatique
- Appels API via OpenClaw Gateway existant
- Formatage reponse Telegram (Markdown, recap, confirmation)
- Journalisation trace dans opt-trading
- Smoke E2E Telegram → Botpress → surfaces → Telegram

## 12_INVARIANTS

- Pas de trade reel automatique V1
- Pas de push Git automatique depuis Botpress
- Pas de logique trading dupliquee dans Botpress
- opt-trading = source canonique
- OpenClaw Gateway = existant, a adapter, pas a recreer
- Safety gate obligatoire
- Journalisation obligatoire

## 17_RESUME_POINT

```
docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md
```

## RISKS

- À qualifier.
