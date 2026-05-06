---
doc_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01_IDE_BUNDLE_README
doc_type: ide_bundle_readme
repo: opt-trading
project: opt-trading
module: botpress_operator
go_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
status: ready_for_ide
lifecycle_stage: cadrage_bundle
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - botpress
  - ide_bundle
  - openclaw
  - telegram
  - lona
  - trading_labs
links:
  - ../README.md
  - ./00_PROMPT_IDE_MASTER.md
  - ./01_PROMPT_DOCS_COMPLETE.md
  - ./02_PROMPT_IMPL_OPENCLAW_GATEWAY.md
  - ./03_PROMPT_IMPL_BOTPRESS_ACTIONS.md
  - ./04_PROMPT_SMOKE_E2E.md
  - ./MANIFEST.json
---

# IDE Bundle — Botpress Operator Parent

## Objet

Bundle IDE autonome pour cadrer, documenter puis implémenter le chantier parent :

`GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01`

## Cible fonctionnelle

```text
Telegram Screener
→ Botpress Operator
→ OpenClaw Gateway
→ student / Trading Labs
→ LONA Trading Assistant
→ opt-trading journalisation
→ retour Telegram
```

## Contenu du bundle

| Fichier | Rôle |
| --- | --- |
| `00_PROMPT_IDE_MASTER.md` | Prompt maître à lancer dans l'IDE |
| `01_PROMPT_DOCS_COMPLETE.md` | Prompt pour compléter la documentation canonique du chantier |
| `02_PROMPT_IMPL_OPENCLAW_GATEWAY.md` | Prompt d'implémentation du gateway local OpenClaw |
| `03_PROMPT_IMPL_BOTPRESS_ACTIONS.md` | Prompt pour générer les actions/code Botpress |
| `04_PROMPT_SMOKE_E2E.md` | Prompt de smoke test end-to-end |
| `MANIFEST.json` | Métadonnées machine du bundle |

## Règles d'exécution

- Travailler sur la branche dédiée : `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01`.
- Ne pas toucher `sot/mainline` directement.
- Ne pas implémenter de trade réel.
- Ne pas ajouter de push Git automatique dans Botpress.
- Ne pas dupliquer la logique métier trading dans Botpress.
- Journaliser les changements réels seulement.

## Point de reprise

Lancer d'abord `00_PROMPT_IDE_MASTER.md`, puis exécuter les prompts dans l'ordre numérique.
