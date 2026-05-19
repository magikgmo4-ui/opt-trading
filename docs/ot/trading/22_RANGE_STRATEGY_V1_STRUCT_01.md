# RANGE STRATEGY V1 — STRUCT 01

Date (America/Montreal) : 2026-04-14

## RÔLE DU DOCUMENT

Ce document ouvre le cadrage canonique de `Range Strategy V1` dans `opt-trading`.

Il sert à figer :
- le besoin initial ;
- la cible finale / objectif final visé ;
- le plan validé reconstitué ;
- l'état établi courant ;
- le gap restant ;
- le next GO.

Il ne vaut ni validation statistique, ni backtest, ni ouverture runtime.

## Besoin initial

Le besoin initial retenu est de construire une stratégie de trading en range simple, lisible et disciplinée, à partir d'actifs connus pour présenter régulièrement des phases de range relativement stables et exploitables.

L'objectif n'est pas de multiplier les actifs ni de surcharger la logique, mais de partir d'un petit noyau d'actifs faciles à lire et à comparer.

## Cible finale

La cible finale visée est une stratégie `Range Strategy V1` qui :
- reste simple ;
- reste exécutable humainement ;
- est compatible avec journalisation et évaluation statistique ultérieure ;
- sépare clairement cadre de marché, signal, invalidation et discipline de session ;
- reste bornée à un noyau initial de trois actifs.

### Noyau initial retenu
- `AUD/NZD`
- `USD/CHF`
- `XAUUSD`

### Intention produit retenue
Le produit visé n'est pas un bot automatique.
Le produit visé est d'abord un cadre stratégique exploitable, documentable, testable et journalisable.

## CLASSIFICATION

- Type : structuration stratégique canonique
- Classe de travail : module durable documentaire
- Portée : doc-only
- Repo canonique : `opt-trading`
- Branche canonique de continuité : `sot/mainline`

## RÔLES / POSTURES RETENUS

### Recommandation par défaut
- posture retenue : **architecte stratégie + cadrage opératoire**

### Séparation explicite
- **Rôle machine** : aucun runtime ni aucune machine d'exécution engagés à ce stade.
- **Rôle IA/IDE** : figer le chantier, le plan validé, le point de reprise.
- **Rôle repo / produit** : ancrer `Range Strategy V1` dans `opt-trading`.

## ETABLI

À ce stade, les points suivants sont retenus comme établis :
- le besoin utilisateur est explicitement centré sur des actifs faciles à trader en range ;
- le chantier a été ouvert sur la branche dédiée `feat/range-strategy-v1-struct` ;
- deux artefacts initiaux ont été créés :
  - `docs/ot/reports/OT_RANGE_STRATEGY_V1_STRUCT_01.md`
  - `docs/ot/closings/OT_RANGE_STRATEGY_V1_STRUCT_01_CLOSING.txt`
- trois actifs ont été retenus et validés en séance comme noyau initial :
  - `AUD/NZD` = range serré / propre / répétitif ;
  - `USD/CHF` = range lent / stable / technique ;
  - `XAUUSD` = range exploitable avec meilleur potentiel de RR mais timing plus exigeant.
- le chantier est désormais replacé dans la couche canonique `docs/chantiers/` + `docs/ot/trading/`.
- aucun patch runtime, aucun module d'exécution, aucun backtest et aucune preuve statistique ne sont encore ouverts ici.

## Plan validé

Le plan validé reconstitué pour `Range Strategy V1` est le suivant :
1. figer le noyau d'actifs de référence ;
2. définir le cadre de lecture du range par actif ;
3. formaliser les règles d'entrée ;
4. formaliser les règles de sortie, invalidations, SL et TP ;
5. définir les fenêtres de session et les cas d'abstention ;
6. préparer une journalisation exploitable ;
7. préparer ensuite seulement une couche d'évaluation statistique ou de backtest ;
8. décider en dernier lieu si une déclinaison module, sheet ou bundle est justifiée.

## Gap restant

Le chantier n'établit pas encore :
- les règles exactes d'entrée / sortie ;
- le protocole de confirmation figé ;
- les sessions privilégiées par actif ;
- le modèle de risque unifié ;
- le format canonique de journalisation ;
- le protocole de comparaison inter-actifs ;
- la forme de livraison future la plus pertinente.

## Next GO

`GO_RANGE_STRATEGY_V1_RULES_01`

Objectif du prochain GO :
- formaliser les règles opératoires minimales ;
- séparer explicitement `ETABLI`, `HYPOTHESE`, `A TESTER` ;
- préparer une base exploitable pour journalisation et évaluation future.

## REPRISE

- repo : `opt-trading`
- branche de travail : `feat/range-strategy-v1-struct`
- document d'entrée : `docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md`
- prochain GO : `GO_RANGE_STRATEGY_V1_RULES_01`

## MEM_CANDIDATE

NO_MEMORY
