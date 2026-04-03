# INDEX — OT / TRADING

## RÔLE

Ce fichier est le **point d’entrée local** de `docs/ot/trading/`.

Il sert à :
- repérer rapidement les documents trading de cette zone ;
- distinguer cadrage, reprise, et futures briques ;
- offrir une lecture simple sans devoir relire tout le dossier.

## DOCUMENTS CANONIQUES ACTUELS

- **docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md** : cadrage canonique V1 du système dual **Lab + Real-Time**, verdict multi-rôles, architecture cible, garde-fous, et décision de design.
- **docs/ot/trading/01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md** : point de reprise opératoire minimal pour ouvrir la suite du chantier sans relire tout le cadrage.
- **docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md** : spec opératoire V1 du noyau commun `frame / strategy / execution / analytics`, config V1, event schema, trade schema, et variantes Gold/session.

## ÉTAT ACTUEL DE LA ZONE

### Établi
- le principe **dual stack Lab + Real-Time** est cadré ;
- le **cadre trader humain** est retenu comme invariant ;
- le focus V1 initial est **Gold / XAUUSD**, fenêtres `18:00` et `00:00`, timezone `America/Montreal` ;
- le trigger canonique de reprise est défini ;
- la **core spec V1** du noyau commun est désormais matérialisée.

### Non encore matérialisé ici
- schémas machine-lisibles V1 ;
- implémentation LAB ;
- runner REAL-TIME ;
- comparateur lab/live exécuté sur données réelles.

## ORDRE DE LECTURE RECOMMANDÉ

1. lire `00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
2. lire `01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`
3. lire `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
4. seulement ensuite ouvrir la matérialisation ou l’implémentation suivante

## POINT DE REPRISE COURT

Trigger actif : `GO_OT_TRADING_DUAL_STACK_V1_01`

Trigger naturel suivant : `GO_OT_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01`
