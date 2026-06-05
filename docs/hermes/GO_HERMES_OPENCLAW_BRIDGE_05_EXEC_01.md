# GO_HERMES_OPENCLAW_BRIDGE_05_EXEC_01

## Classification
Type : diagnostic ponctuel borne

## But

Passer du cadrage documentaire du bridge Hermes/OpenClaw a une execution reelle du cas 01, sans sortir du perimetre borne deja etabli.

## Cas 01 retenu

Le cas 01 reste strictement minimal :
- un script shell texte genere par Hermes ;
- le script affiche seulement :
  - `bridge_case_01_ok`
  - `pwd`
  - `whoami`
  - `date`
- OpenClaw relit avant execution ;
- l execution n a lieu qu apres validation humaine explicite.

## Sequence reelle attendue

1. utiliser `HERMES_OPENCLAW_BRIDGE_CASE_01_PROMPT.txt`
2. recuperer le script genere par Hermes
3. relire le script humainement
4. faire relire le script par OpenClaw dans un cadre controle
5. valider humainement ou rejeter
6. si valide, executer manuellement le script
7. capturer la sortie
8. remplir `HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_TEMPLATE.txt`

## Regles de validation

Le script doit etre rejete si :
- il depasse le perimetre d affichage borne ;
- il touche au reseau ;
- il installe, demarre ou persiste quoi que ce soit ;
- il modifie la configuration ou des fichiers de production ;
- il fait un commit Git ou une action irreversible.

## Condition de close

Ce GO exec 01 est clos si :
- le script Hermes est capture ;
- la validation humaine est tracee ;
- si execution autorisee, la sortie observee est capturee ;
- le resultat est consigne sans extrapolation sur la maturite generale du bridge.

## Hors perimetre

- pas de second cas de preuve ;
- pas de framework bridge declare etabli ;
- pas de generalisation produit ;
- pas de mutation systeme large.

## RISKS

- À qualifier.
