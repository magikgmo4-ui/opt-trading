# 00_CANONICAL_CONTEXT

## État validé

- PR #705 mergée : standard `bundle + .patch + .zip` canonisé dans la matrice et `BUNDLE_TYPES.md`.
- Les index globaux actuels sont trop larges pour l'usage voulu.
- Le nouveau target ne vise pas à tout indexer, mais à réduire les index globaux au niveau parent/produit.

## Nouvelle règle cible

Les index globaux doivent contenir seulement :

```text
chantiers parents
+ produit fini utilisable ou produit cible utilisable
+ état courant
+ gap restant
+ prochain target
```

## Exclusions

Ne doivent plus vivre comme lignes actives dans les index globaux :

- enfants techniques ;
- micro-GO ;
- bundles ;
- patchs ;
- branches ;
- PR ;
- entrées historiques ;
- références non opératoires ;
- surfaces machine sans produit utilisable explicite.

## Destination des exclusions

| Élément | Destination |
|---|---|
| enfant technique | `docs/chantiers/<GO_ID>/` + `docs/index/inbox/<GO_ID>.md` |
| micro-GO terminé | `docs/index/GO_CLOSED_INDEX.md` si clos/PASS, sinon inbox/local |
| bundle | `bundles/<GO_ID>/` + `bundles/BUNDLE_TARGET_INDEX.md` si target suivi |
| branche | `docs/index/BRANCH_STATE.md` |
| historique/référence | `GO_CLOSED_INDEX.md` ou dossier chantier, pas index actif |
