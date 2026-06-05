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
- **docs/ot/trading/03_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01.md** : clôture documentaire de la matérialisation des schémas V1 et pointage vers la suite naturelle.

## SCHÉMAS MACHINE-LISIBLES

- **docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml** : profil YAML V1 du focus `XAUUSD`.
- **docs/ot/trading/schemas/trading_event_v1.schema.json** : schéma JSON des événements V1.
- **docs/ot/trading/schemas/trading_trade_v1.schema.json** : schéma JSON des trades V1.

## ÉTAT ACTUEL DE LA ZONE

### Établi
- le principe **dual stack Lab + Real-Time** est cadré ;
- le **cadre trader humain** est retenu comme invariant ;
- le focus V1 initial est **Gold / XAUUSD**, fenêtres `18:00` et `00:00`, timezone `America/Montreal` ;
- la **core spec V1** du noyau commun est matérialisée ;
- les **schémas machine-lisibles V1** sont maintenant matérialisés.

### Non encore matérialisé ici
- squelette LAB exécutable ;
- runner REAL-TIME ;
- comparateur lab/live exécuté sur données réelles.

## ORDRE DE LECTURE RECOMMANDÉ

1. lire `00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
2. lire `01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`
3. lire `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
4. lire `03_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01.md`
5. seulement ensuite ouvrir la matérialisation ou l’implémentation suivante

## POINT DE REPRISE COURT

Trigger courant clos au niveau schémas : `GO_OT_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01`

Trigger naturel suivant : `GO_OT_TRADING_LAB_V1_SKELETON_01`

## RISKS

- À qualifier.
