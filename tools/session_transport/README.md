# session_transport

## Objet

Outils locaux pour appliquer et classer des fichiers `.patch` produits par une session conversationnelle.

## Zone d'entrée pratique

Déposer les patchs téléchargés à la racine du repo local :

```text
./<patch>.patch
```

Cette zone est temporaire. Aucun patch racine ne doit être committé.

## Emplacement canonique

```text
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Fallback temporaire :

```text
docs/chantiers/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

## Scripts

```text
bootstrap_patch_inbox.sh
bootstrap_patch_inbox.ps1
apply_session_patch.sh
apply_session_patch.ps1
```

## Usage Bash — déplacer un patch racine

```bash
tools/session_transport/bootstrap_patch_inbox.sh ./some.patch GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 initial_bundle
```

## Usage Bash — appliquer un patch

```bash
tools/session_transport/apply_session_patch.sh ./some.patch go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
```

## Usage PowerShell — déplacer un patch racine

```powershell
.\tools\session_transport\bootstrap_patch_inbox.ps1 -PatchPath .\some.patch -GoId GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 -Slug initial_bundle
```

## Usage PowerShell — appliquer un patch

```powershell
.\tools\session_transport\apply_session_patch.ps1 -PatchPath .\some.patch -Branch go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
```

## Règles

- les scripts ne commitent pas automatiquement;
- ils ne poussent pas;
- ils ne modifient pas les index globaux par eux-mêmes;
- ils appliquent le patch seulement après `git apply --check`;
- ils affichent les fichiers modifiés;
- l'opérateur doit valider avant commit;
- le patch racine est une inbox temporaire.
