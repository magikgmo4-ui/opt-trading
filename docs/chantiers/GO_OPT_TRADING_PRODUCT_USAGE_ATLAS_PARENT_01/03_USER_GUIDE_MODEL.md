---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_USER_GUIDE_MODEL
doc_type: guide_model
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
---

# 03_USER_GUIDE_MODEL - Modele de guide utilisateur

## Modele

```text
# Guide utilisateur - <Produit>

## Ce que c'est
## A quoi ca sert
## Quand l'utiliser
## Quand ne pas l'utiliser
## Prerequis
## Commandes / acces
## Procedure simple
## Verification PASS
## Limites
## Depannage
## Source canonique
## NEXT_GO
```

## Regles d'usage

- Le guide doit parler de l'usage actuel prouve, pas du reve produit.
- Le guide doit dire explicitement quand ne pas utiliser la surface.
- Les prerequis ne doivent jamais demander un secret commite.
- Si la surface est `SIMULATED_PASS`, le guide doit dire qu'il s'agit d'un usage test seulement.
- Si la surface est `DOC_ONLY_READY`, le guide doit rester un guide de lecture, pas un guide live.
- Si la surface est `NOT_USABLE_YET` ou `DO_NOT_USE_LIVE`, ne pas ecrire de guide live.
