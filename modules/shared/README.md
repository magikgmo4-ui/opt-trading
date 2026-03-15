# shared — surface canonique inter-machines

## Doctrine (V1)
`shared` est la surface canonique inter-machines du projet.

Il sert par défaut au dépôt, à la récupération, à la livraison et au transfert des artefacts utiles entre `cursor-ai/Windows`, `admin-trading`, `db-layer`, `student`, et selon le cas les sorties générées par Trae.

`shared` est également le dossier par défaut pour les ajouts manuels liés au projet : téléchargements utiles, patchs, bundles, scripts, documents, fichiers externes reçus et livraisons intermédiaires.

Principe : tout fichier utile au projet, susceptible d’être relu, déplacé, exécuté, validé ou récupéré depuis une autre machine, doit aller par défaut dans `shared`.

Règles :
1. fichier utile au projet => `shared` par défaut
2. transfert inter-machines => `shared` comme canal normal
3. livraisons d’outils/docs/bundles/patchs => `shared`
4. racine `shared` légère ; utiliser les sous-dossiers canoniques
5. ne pas déplacer automatiquement les cas ambigus/sensibles
6. Linux client => `/shared`
7. admin-trading (source réelle) => `/srv/sftp/shared_files/shared` (alias `/shared`)
8. Windows local canonique => `C:\Users\ghost\Downloads\SHARED\`

## Chemins canoniques
- `admin-trading`
  - source réelle : `/srv/sftp/shared_files/shared`
  - alias local : `/shared`
- `db-layer`
  - `/shared` (monté via `shared_sshfs_permanent`)
  - raccourci utilisateur : `/home/ghost/Téléchargements/SHARED` -> `/shared`
- `student`
  - `/shared` (monté via `shared_sshfs_permanent`)
- `cursor-ai` (Windows)
  - chemin local canonique : `C:\Users\ghost\Downloads\SHARED\`
  - accès distant validé : SFTP vers `admin-trading`, surface distante `/shared`

## Sous-dossiers canoniques (racine légère)
- `_bundles/` : zips (packs/bundles/patches)
- `_ops/` : scripts opératoires
- `_refs/` : références (md/txt, checksums)
- `_archives/` : anciens/doublons (sur décision)

Les dossiers pipeline/réservés restent stables à la racine :
`inbox/ outbox/ modules/ _logs/ vision_* / desk_pro/ documents/ windows/ _git_archives/`.

## UX minimale (Linux)
Module : `shared`

Commande :
- `cmd-shared ls [<relpath>]`
- `cmd-shared get [--dry-run] [--force] <relpath> [<dest>]`
- `cmd-shared put [--dry-run] [--force] <src> [<relpath|dir>]`
- `cmd-shared cat <relpath>`
- `cmd-shared status`
- `cmd-shared path`

Notes :
- Les chemins `relpath` sont relatifs à la racine `shared` (ex: `_bundles/x.zip`, `README.txt`).
- Par défaut, `cmd-shared` vise `/shared` si présent, sinon `/srv/sftp/shared_files/shared`.

