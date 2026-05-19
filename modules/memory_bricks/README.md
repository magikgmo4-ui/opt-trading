# Memory Bricks V1

## Description
Memory Bricks V1 materialise une surface CLI locale minimale pour la memoire durable canonique.

Cette surface est volontairement bornee pour permettre une validation terrain du pont KIL -> Memory Bricks sans ouvrir de chantier UI, API mutante ou refonte large.

## Surface CLI retenue
- `new --payload-file <path>` : cree une vraie brique et emet un vrai `MB-*`
- `link --id <MB-*> --target <link>` : ajoute un lien a une brique existante
- `index rebuild` : reconstruit `index_full.json` et `index_short.md`
- `query status` : expose l'etat minimal de la source V1

## Source de verite
- racine par defaut : `/opt/trading/_state/memory_bricks`
- override possible : `MEMORY_BRICKS_STATE_ROOT`

## Format d'entree minimal
- `new` accepte un JSON via `--payload-file`
- si le fichier contient une cle `brick`, le contenu de `brick` est utilise comme payload reel
- sinon le fichier entier est traite comme payload de brique

Champs supportes pour la brique :
- `title`
- `type`
- `status`
- `ia`
- `machine`
- `surface`
- `project`
- `module`
- `summary_short`
- `resume_point`
- `tags`
- `links`
- `decisions`
- `todo`

## Format de sortie minimal
- succes : JSON objet sur stdout, code retour `0`
- erreur de validation / absence : JSON objet sur stderr, code retour `2`
- erreur runtime inattendue : JSON objet sur stderr, code retour `1`

## Exemple minimal
```bash
bash modules/memory_bricks/cmd.sh new --payload-file /tmp/brick.json
bash modules/memory_bricks/cmd.sh link --id MB-00001 --target KIL-ABC
bash modules/memory_bricks/cmd.sh index rebuild
bash modules/memory_bricks/cmd.sh query status
```
