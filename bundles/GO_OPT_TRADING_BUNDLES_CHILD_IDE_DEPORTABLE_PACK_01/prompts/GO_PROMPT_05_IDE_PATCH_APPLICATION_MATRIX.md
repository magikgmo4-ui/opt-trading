# GO_PROMPT_05_IDE_PATCH_APPLICATION_MATRIX

## ROLE

Tu es ChatGPT IDE opérant dans le repo `opt-trading`.

## INSTRUCTION UNIQUE

Lis et applique :

```text
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/docs/EXEMPLE_MATRICE_APPLICATION_PATCH.md
```

## OBJECTIF

Appliquer un patch produit en session conversationnelle selon la méthode canonique :

```text
patch racine temporaire
-> bootstrap vers bundles/<GO_ID>/patches/
-> git apply --check
-> git apply
-> validate
-> commit
-> verify before push
-> push
-> PR
-> review demandée
-> merge si conforme
```

## STOP

Arrêter si :

- `.patch` racine staged;
- index global modifié;
- runtime modifié;
- secret détecté;
- `git apply --check` échoue;
- diff hors scope.
