# CHECKLIST_EXECUTION

## Préconditions

- [ ] Branche `go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01` active.
- [ ] Base alignée sur `origin/sot/mainline`.
- [ ] Aucun fichier hors scope modifié.
- [ ] Patch disponible à la racine ou sous `bundles/<GO_ID>/patches/`.

## Exécution

- [ ] `git apply --check` PASS.
- [ ] `git apply` PASS.
- [ ] `git diff --check` PASS.
- [ ] Fichiers attendus présents.
- [ ] Aucun index global modifié.
- [ ] Aucun runtime modifié.
- [ ] Aucun patch racine inclus dans le commit.

## Sortie

- [ ] Status Git retourné.
- [ ] Liste fichiers retournée.
- [ ] Résultat no-secrets retourné.
- [ ] Root patch check retourné.
- [ ] Commit SHA retourné si commit créé.
