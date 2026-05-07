---
doc_id: OPT_TRADING_GUIDE_LOCALCMS_READONLY
doc_type: user_guide_readonly
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/
  - docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/
---

# Guide de lecture - LocalCMS

> **ATTENTION : ceci est un guide de lecture, pas un guide d'usage live.**
> Ce produit est `DOC_ONLY`. C'est un projet externe consommateur, sans runtime integre dans opt-trading.

## Ce que c'est

LocalCMS est un projet consommateur UI externe prevu pour exploiter `/shared`, explorer les modules et servir de futur cockpit utilisateur pour opt-trading.

## A quoi ca sert

Il sert de cadre documente pour un consumer UI qui lira les surfaces partagees sans remplacer le repo canonique.

## Quand le consulter

- pour comprendre le role futur de la couche UI ;
- pour lire le cadrage du consumer parent ;
- pour preparer l'integration forms.

## Quand ne pas l'utiliser

- comme un produit integre au repo (c'est un projet externe) ;
- comme un cockpit operationnel aujourd'hui (pas de runtime prouve) ;
- comme source canonique (le repo prime).

## Ce qu'il ne faut pas en deduire

- Ce produit n'est pas `USABLE_NOW`. Il est `DOC_ONLY`.
- LocalCMS est un consommateur externe, pas une surface runtime du repo.
- Aucun usage reel n'est prouve a ce stade.

## Prerequis de lecture

- lecture du cadrage : `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`
- lecture du forms integration : `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`

## Procedure de lecture

1. Lire le cadrage du consumer parent.
2. Lire le forms integration doc pour comprendre le premier cas d'usage.
3. Noter que le projet est externe et sans runtime integre.
4. Noter le NEXT_GO : `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`.
5. Ne pas traiter LocalCMS comme un produit operationnel du repo.

## Limites

- projet externe, pas de runtime integre dans opt-trading ;
- aucun usage reel prouve ;
- consumer UI en phase de cadrage uniquement.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`
- `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/`

## NEXT_GO

`GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` puis preuve d'usage reel
