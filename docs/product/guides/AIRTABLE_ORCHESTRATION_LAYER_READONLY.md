---
doc_id: OPT_TRADING_GUIDE_AIRTABLE_ORCHESTRATION_LAYER_READONLY
doc_type: implementation_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md
---

# Guide d'implementation - Airtable Orchestration Layer

> **Sous-type :** `DOC_ONLY_IMPLEMENTATION_READY`
> Le produit est cadre, le verdict est `GO_LIMITED`, le plan de finition est documente. L'implementation du bridge est la prochaine etape.

## 1_MASTER_TARGET

Couche Airtable legere de journal, review humaine, signaux et exports, integree au repo via un bridge optionnel.

## FINAL_TARGET

Produit borne avec base Airtable, bridge `modules/airtable_bridge/`, exports JSON/CSV et role humain clair.

## CURRENT_STATE

`DOC_ONLY / GO_LIMITED` -- `DOC_ONLY_IMPLEMENTATION_READY`. Le role produit, le schema et le finish plan sont documentes. Le verdict est `GO_LIMITED`. Le bridge repo n'est pas encore materialise.

## USAGE_ALLOWED_NOW

- Lire le verdict, le finish plan et l'architecture.
- Preparer le GO de creation du bridge.
- Aligner les tables et flux avec le plan produit.

## USAGE_FORBIDDEN_NOW

- Usage runtime Airtable direct sans bridge.
- Traiter Airtable comme source canonique.
- Traiter Airtable comme moteur trading live ou DB historique.

## IMPLEMENTATION_PATH

1. Creer `modules/airtable_bridge/` (client API, config, sanity, cmd/menu).
2. Finaliser les tables produit (Trades, Signals, Backtests, GO_Status).
3. Mettre en place les exports JSON/CSV.
4. Prouver un usage borne.
5. Closeout produit.

## CONTINUITY_STATE

En attente d'implementation -- `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` est le prochain GO.

## MACHINE / SURFACE

`fantome` (bridge, integration repo).

## REPRISE_POINT

```text
docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md
```

## TODO

1. Ouvrir `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.
2. Creer `modules/airtable_bridge/`.
3. Finaliser les tables produit.
4. Mettre en place les exports.
5. Prouver l'usage borne.

## REMAINING_GAP

Bridge `modules/airtable_bridge/`, tables produit finales, exports controles, preuve d'usage borne.

## NEXT_GO

`GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`

## PROMOTION_CONDITIONS

`DOC_ONLY` -> `USABLE_LIMITED` quand :
- bridge cree et operationnel,
- tables produit finalisees,
- preuve d'usage borne posee.

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- closeout produit pose.

## Ce que c'est

Couche de journal, review humaine, signaux et exports prevue pour orchestrer les donnees legeres du trading.

## A quoi ca sert

Futur cockpit data leger : journal trading, validation humaine, dashboard operateur, exports.

## Quand le consulter

- Pour comprendre le role futur d'Airtable.
- Pour lire le verdict et le finish plan.
- Pour preparer le GO de creation du bridge.

## Quand ne pas l'utiliser

- Comme produit runtime operationnel (bridge absent).
- Comme moteur trading live ou DB historique.
- Comme source canonique.

## Prerequis de lecture

- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`
- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md`

## Procedure de lecture

1. Lire le verdict (`GO_LIMITED`).
2. Lire le finish plan (tables, flux, strategie de sortie).
3. Identifier le NEXT_GO : `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.
4. Ne pas tenter d'usage runtime avant PASS de ce GO.

## Limites

- Pas de bridge `modules/airtable_bridge/`.
- Pas de tables produit finales.
- Pas d'exports prouves.
- Pas de preuve d'usage borne.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md`
- `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md`
