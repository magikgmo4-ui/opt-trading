# Etat du parent LocalCMS consumer

## Parent conserve
- Parent projet conserve : `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`.
- Role conserve : chantier d'integration UI `opt-trading producer -> localcms consumer`.
- Ce parent ne doit pas etre transforme en parent machine.

## Fichiers et GO lus
- `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md`
- `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md`
- `docs/index/GO_INDEX.md`
- `docs/index/GO_PARENT_THREAD_MAP.md`

## Role exact retenu
- `opt-trading` reste le producer canonique.
- `localcms` reste le consumer UI.
- Le parent porte la logique d'inventaire, de matrice producer/consumer, de contrats d'exposition et de lot pilote.
- Le parent ne porte pas la machine `db-layer` elle-meme.

## Ce qui est actif
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
  - parent projet actif, ouvert, utile a la continuite.
- `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`
  - actif documentaire connexe sous le fil projet UI
  - oriente vers une future couche `forms` compatible avec `localcms` existant
  - ne remplace pas le parent consumer

## Ce qui est reference-only
- `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`
- `GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01`
- `GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01`
- `GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01`

Ces sous-GO restent reference-only dans les index canoniques et ne sont pas materialises localement sous `docs/chantiers/` sur cette ligne.

## Gaps
- L'inventaire UI reel n'est pas encore rejoue comme GO autonome dans cette passe.
- Les contrats d'exposition restent documentes comme formats cibles, pas comme implementation effective.
- Aucun lot pilote `read-only` n'est rejoue ici.
