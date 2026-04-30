# Classification des GO LocalCMS

## GO_LOCALCMS_FORMS_INTEGRATION_DOC_01
- Classification retenue : actif documentaire / projet
- Statut : ouvert dans `GO_INDEX.md`
- Role : cadrage d'une future couche `forms` compatible avec `localcms` existant
- Decision : garder actif comme extension documentaire, sans l'absorber dans `db-layer`

## GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01
- Classification retenue : reference-only
- Statut indexe : `REFERENCE`
- Role : inventaire UI reel cote `opt-trading`
- Decision : ne pas l'ouvrir maintenant dans ce GO ; le maintenir comme repere de reprise

## GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01
- Classification retenue : reference-only
- Statut indexe : `REFERENCE`
- Role : matrice producer/consumer par UI
- Decision : garder comme surface derivee a relancer plus tard si necessaire

## GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01
- Classification retenue : reference-only
- Statut indexe : `REFERENCE`
- Role : contrats d'exposition cibles
- Decision : garder en reference tant qu'aucun lot d'implementation ou de validation fine n'est rouvert

## GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01
- Classification retenue : reference-only / differe
- Statut indexe : `REFERENCE`
- Role : premier lot pilote read-only
- Decision : differe tant que le realignment parent/machine n'est pas fige et qu'aucun lot pilote n'est explicitement relance

## Synthese
- Parent actif :
  - `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
- Actif documentaire connexe :
  - `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`
- Reference-only :
  - `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`
  - `GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01`
  - `GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01`
  - `GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01`

## A fermer
- Aucun de ces GO n'est a fermer dans cette passe.
- Le besoin actuel est un realignment de lecture, pas un closeout de famille `LocalCMS`.
