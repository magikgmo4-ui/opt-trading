# HERMES OPENCLAW BRIDGE CASE 01 V1

## Classification
Type : preuve ponctuelle bornee

## But

Definir le premier cas de preuve Hermes -> OpenClaw -> validation humaine sans declarer un bridge general etabli.

## Cas retenu

Cas minimal recommande :
- Hermes produit un petit script shell texte ;
- le script se contente d afficher :
  - un marqueur `bridge_case_01_ok`
  - `pwd`
  - `whoami`
  - `date`
- OpenClaw relit d abord le script ;
- l execution n a lieu qu apres validation humaine explicite.

## Contraintes sur le script

Le script doit :
- etre court ;
- ne pas modifier la configuration ;
- ne pas toucher au reseau ;
- ne pas ecrire hors d un dossier de travail borne si ecriture il y a ;
- se terminer proprement avec un code de sortie simple.

Le script ne doit pas :
- installer quoi que ce soit ;
- appeler un service externe ;
- modifier des fichiers de production ;
- lancer un daemon ;
- faire un commit Git.

## Sequence recommandee

1. Hermes genere le script texte
2. OpenClaw relit le script
3. validation humaine explicite
4. execution manuelle bornee
5. observation du resultat
6. decision humaine : conserver comme preuve ou rejeter

## Livrables minimaux

- le prompt Hermes utilise
- le script genere
- la preuve de relecture OpenClaw
- la sortie d execution si l execution est autorisee
- une note de validation humaine

## Condition de close

Le cas 01 est clos si :
- le script est produit ;
- il respecte les contraintes ci-dessus ;
- la validation humaine est tracee ;
- s il est execute, la sortie observee reste conforme au perimetre borne.

## Hors perimetre

- pas de patch multi-fichiers ;
- pas de mutation systeme large ;
- pas d auto-merge ;
- pas de declaration de bridge general valide.
