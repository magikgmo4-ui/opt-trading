# Dependances et prochain GO

## Dependances restantes
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`
  - `db-layer` reste la machine prioritaire actuelle.
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
  - garde le cadrage projet consumer.
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
  - reste transverse
  - non bloquant pour les lectures documentaires et read-only
  - toujours necessaire avant certaines validations physiques multi-machines plus larges
- `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
  - si pris en compte, reste transverse / methode
  - pas un blocage direct pour `LocalCMS` sur `db-layer`

## Relation avec OpenClaw
- `OpenClaw` est hors perimetre actif de ce GO.
- Le cycle `OpenClaw/db-layer` est considere clos localement et ne doit pas etre remelange avec `LocalCMS`.

## Relation avec admin-trading
- aucune action maintenant
- `admin-trading` reste differe
- ne pas relancer `admin-trading` avant la consolidation transverse restante

## Next GO recommande
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01`

## Justification
- Le cycle `db-layer` est maintenant clarifie sur ses deux surfaces locales prioritaires :
  - `OpenClaw`
  - `LocalCMS consumer`
- La prochaine dependance transversale restante avant un retour serein vers `admin-trading` est `reseau_ssh`.
- `admin-trading` doit donc rester derriere ce closeout transverse.

## RISKS

- À qualifier.
