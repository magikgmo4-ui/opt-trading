---
doc_id: OPT_TRADING_GUIDE_LOCALCMS_READONLY
doc_type: implementation_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/
  - docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/
---

# Guide d'implementation - LocalCMS

> **Sous-type :** `DOC_ONLY_IMPLEMENTATION_READY`
> Projet externe consommateur, cadrage et plan documentes, GO consumer parent ouvert. L'implementation est la prochaine etape.

## 1_MASTER_TARGET

Consumer UI operationnel exploitant `/shared`, explorant les modules, servant de cockpit utilisateur pour opt-trading.

## FINAL_TARGET

Consumer UI integre avec lecture `/shared`, exploration modules, cockpit utilisateur et forms integration.

## CURRENT_STATE

`DOC_ONLY` -- `DOC_ONLY_IMPLEMENTATION_READY`. Cadrage et plan documentes. GO consumer parent ouvert. Projet externe, pas de runtime integre dans opt-trading.

## USAGE_ALLOWED_NOW

- Lire le cadrage du consumer parent.
- Lire le forms integration doc.
- Preparer l'implementation.

## USAGE_FORBIDDEN_NOW

- Traiter comme produit integre au repo.
- Traiter comme cockpit operationnel aujourd'hui.
- Traiter comme source canonique.

## IMPLEMENTATION_PATH

1. Ouvrir et passer `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`.
2. Prouver un usage reel.
3. Integrer la lecture `/shared`.
4. Construire le cockpit utilisateur.

## CONTINUITY_STATE

En attente d'implementation -- GO consumer parent ouvert, forms integration en cadrage.

## MACHINE / SURFACE

`MSI / db-layer` (surface de lecture cible, selon docs/ui_screenshots).

## REPRISE_POINT

```text
docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/
docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/
```

## TODO

1. Passer `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`.
2. Prouver un usage reel.
3. Integrer `/shared`.
4. Construire le cockpit.

## REMAINING_GAP

Projet externe, pas de runtime integre, usage reel a prouver.

## NEXT_GO

`GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` puis preuve d'usage reel.

## PROMOTION_CONDITIONS

`DOC_ONLY` -> `USABLE_LIMITED` quand :
- forms integration prouvee,
- usage reel demontre.

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- cockpit operationnel,
- closeout produit pose.

## Ce que c'est

Projet consommateur UI externe prevu pour exploiter `/shared` et servir de cockpit.

## A quoi ca sert

Futur consumer UI lisant les surfaces partagees sans remplacer le repo canonique.

## Quand le consulter

- Pour comprendre le role futur de la couche UI.
- Pour preparer l'integration forms.

## Quand ne pas l'utiliser

- Comme produit integre au repo.
- Comme cockpit operationnel aujourd'hui.
- Comme source canonique.

## Prerequis de lecture

- `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`
- `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`

## Procedure de lecture

1. Lire le cadrage du consumer parent.
2. Lire le forms integration doc.
3. Noter que le projet est externe.
4. Noter le NEXT_GO.

## Limites

- Projet externe, pas de runtime integre.
- Aucun usage reel prouve.
- Consumer UI en phase de cadrage.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`
- `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`
