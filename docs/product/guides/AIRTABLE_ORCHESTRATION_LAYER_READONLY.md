---
doc_id: OPT_TRADING_GUIDE_AIRTABLE_ORCHESTRATION_LAYER_READONLY
doc_type: user_guide_readonly
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md
---

# Guide de lecture - Airtable Orchestration Layer

> **ATTENTION : ceci est un guide de lecture, pas un guide d'usage live.**
> Ce produit est `DOC_ONLY / GO_LIMITED`. Le bridge repo n'existe pas encore. Aucun usage runtime n'est prouve.

## Ce que c'est

Airtable Orchestration Layer est une couche de journal, review humaine, signaux et exports prevue pour orchestrer les donnees legeres du trading sans remplacer le coeur Python ni le repo.

## A quoi ca sert

Elle sert de cadre documente pour un futur cockpit data leger : journal trading, validation humaine, dashboard operateur, exports CSV/JSON.

## Quand le consulter

- pour comprendre le role futur d'Airtable dans la stack ;
- pour lire le verdict, l'architecture et le finish plan ;
- pour preparer le GO de creation du bridge `airtable_bridge`.

## Quand ne pas l'utiliser

- comme un produit runtime operationnel (le bridge n'existe pas) ;
- comme moteur trading live ou DB historique ;
- comme source canonique (le repo prime).

## Ce qu'il ne faut pas en deduire

- Ce produit n'est pas `USABLE_NOW`. Il est `DOC_ONLY`.
- Airtable ne remplace pas le repo, Google Sheets, la DB layer ou LocalCMS.
- Le bridge `modules/airtable_bridge/` doit etre cree avant tout usage runtime.

## Prerequis de lecture

- lecture du verdict : `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`
- lecture du finish plan : `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md`
- lecture de l'architecture : `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/02_INTEGRATION_ARCHITECTURE.md`

## Procedure de lecture

1. Lire le verdict (`99_VERDICT.md`) pour comprendre la decision `GO_LIMITED`.
2. Lire le finish plan (`04_PRODUCT_FINISH_PLAN.md`) pour voir les tables, flux et strategie de sortie prevus.
3. Lire l'architecture d'integration (`02_INTEGRATION_ARCHITECTURE.md`) pour comprendre les couches.
4. Identifier le NEXT_GO : `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.
5. Ne pas tenter d'usage runtime tant que ce GO n'est pas passe.

## Limites

- pas de bridge `modules/airtable_bridge/` cree ;
- pas de tables produit finales ;
- pas d'exports controles prouves ;
- pas de preuve d'usage borne.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`
- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md`

## NEXT_GO

`GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`
