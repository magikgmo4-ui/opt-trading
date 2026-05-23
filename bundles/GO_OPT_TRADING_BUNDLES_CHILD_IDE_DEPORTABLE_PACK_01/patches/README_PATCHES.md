# patches — GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01

## Objet

Dossier canonique pour conserver les `.patch` de transport liés à ce GO.

## Règle pratique

Au téléchargement depuis une session conversationnelle, déposer temporairement le `.patch` à la racine du repo local.

Exemple :

```text
./20260521_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_initial_bundle.patch
```

Puis déplacer avec :

```bash
tools/session_transport/bootstrap_patch_inbox.sh ./20260521_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_initial_bundle.patch GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 initial_bundle
```

Ou PowerShell :

```powershell
.\tools\session_transport\bootstrap_patch_inbox.ps1 -PatchPath .\20260521_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_initial_bundle.patch -GoId GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 -Slug initial_bundle
```

## Emplacement final

```text
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/patches/<YYYYMMDD>_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_<slug>.patch
```

## Interdits

- ne pas committer un `.patch` à la racine ;
- ne pas conserver un patch anonyme ;
- ne pas inclure de secret ;
- ne pas traiter un patch comme source canonique finale.

## Patchs conservés

- `20260521_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_initial_bundle.patch` : première version du bundle IDE déportable préparée en session.
