# Etat db-layer

## Role
- `db-layer` est la machine runtime/app actuelle prioritaire.
- Elle sert de surface de clarification avant `admin-trading`.
- Elle reste dependante du chantier transverse `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` pour les validations physiques multi-machines finales.

## Etat connu
- Parent machine ouvert : `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`.
- Raccourci SSH canonique attendu : `db-layer`.
- Depot attendu sur la machine : `/opt/trading`.
- `LocalCMS` et `OpenClaw` y sont deja references comme surfaces actives, sans changer leurs parents respectifs.

## Etat verifie dans ce GO
- `hostname` distant lu via SSH : `db-layer`.
- Alias SSH resolu depuis la session courante : `ghost@192.168.0.100`.
- Acces distant en lecture seule reussi depuis la session courante.
- Utilisateur distant verifie : `ghost`.
- Repertoire depot verifie : `/opt/trading`.
- Repertoire de depart de session distante observe : `/home/ghost`.

## Etat non verifie dans ce GO
- Inventaire complet des services systeme de `db-layer`.
- Cartographie exhaustive des ports applicatifs hors controle cible `OpenClaw`.
- Equivalence nominale stricte entre la session courante et un poste nomme litteralement `cursor-ai`.

## Gaps
- La couche `reseau_ssh` reste une dependance avant les tests physiques multi-machines finaux.
- L'etat runtime detaille de `OpenClaw` doit etre repris dans un GO dedie.
- Le statut d'execution exact de `LocalCMS` reste a preciser au-dela des chemins verifies.

## RISKS

- À qualifier.
