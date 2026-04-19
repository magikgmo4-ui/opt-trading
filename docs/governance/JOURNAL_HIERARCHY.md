---
doc_id: OPT_TRADING_JOURNAL_HIERARCHY
doc_type: intent
repo: opt-trading
project: opt-trading
module: journal
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - journal
  - hierarchy
  - governance
surface: governance
source_kind: canonical
updated_at: 2026-04-18
links:
  - journal.md
  - journal/index/ACTIVE_GO_MATRIX.md
  - journal/canon/JOURNAL_CANON_FULL_20260301_071931.md
  - docs/index/REPRISE.md
---

# JOURNAL_HIERARCHY — opt-trading

## Objet
Fixer une hiérarchie opposable des surfaces journal afin d’éviter :
- confusion entre brut vivant, dérivés opératoires et archives
- dérive des index de continuité vers des sources non canoniques

## Hiérarchie retenue
### 1) journal.md — brut vivant
- contenu : notes, commandes, fragments, traces non consolidées
- statut : source de brut ; non canonisée
- usage : lecture de reprise terrain, extraction, consolidation

### 2) journal/index/* — dérivés opératoires
- contenu : index et synthèses générés ou maintenus comme aides opératoires
- statut : dérivé ; ne remplace pas la continuité canonique
- usage : navigation, repérage, matrices de travail

### 3) journal/canon/* — archive / historique de lecture
- contenu : lecture canonisée et figée d’un état du brut, produite pour extraction et traçabilité
- statut : archive ; référence historique
- usage : base de lecture structurée, extraction de doctrine, preuve de continuité à une date donnée

## Règles
- la continuité active se pilote via `docs/index/*`
- `journal/canon/*` ne doit pas être traité comme une base active de pilotage, mais comme archive de lecture
- `journal/index/*` ne doit pas devenir une source de vérité concurrente aux index `docs/index/*`

## REPRISE
- reprise opérationnelle : `docs/index/REPRISE.md`
