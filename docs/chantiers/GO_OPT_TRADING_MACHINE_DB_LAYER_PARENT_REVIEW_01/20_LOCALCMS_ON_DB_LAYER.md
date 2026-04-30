# LocalCMS sur db-layer

## Relation db-layer <-> LocalCMS
- `db-layer` est confirme comme machine d'execution actuelle pour des surfaces `LocalCMS`.
- Le parent projet reste `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`.
- Ce GO ne requalifie pas `db-layer` en parent projet `LocalCMS`.

## Etat verifie
- Presence d'un depot `LocalCMS` sur `db-layer` : `/home/ghost/localcms`.
- Branche lue sur ce depot : `main`.
- Presence d'un repertoire runtime associe : `/home/ghost/localcms_runtime`.
- Presence de surfaces opt-trading liees a la consommation UI sur `db-layer` :
  - `/opt/trading/docs/ui_indexation`
  - `/opt/trading/docs/ui_screenshots`
  - `/opt/trading/modules/ui_registry_msi`

## Lecture retenue
- `db-layer` heberge bien la presence de travail et d'execution `LocalCMS`.
- La relation a conserver est : parent projet `LocalCMS` d'un cote, machine d'execution `db-layer` de l'autre.
- Toute realignment producteur/consommateur doit rester rattachee au chantier `LocalCMS consumer`, pas a ce parent machine.

## Gaps et checks suivants
- Le statut de service exact de `LocalCMS` n'a pas ete prouve dans ce GO.
- Le contrat d'exposition courant entre opt-trading et `LocalCMS` reste a revisiter dans un GO de realignment dedie.
