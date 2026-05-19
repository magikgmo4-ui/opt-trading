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
- **docs/ot/trading/04_TRADING_LAB_V1_SKELETON_01.md** : clôture documentaire de l’ouverture du squelette LAB V1 et définition du prochain trigger naturel.
- **docs/ot/trading/05_TRADING_LAB_V1_FIRST_RUNNER_PASS_01.md** : clôture documentaire de la première passe du runner LAB V1 et définition du trigger naturel suivant.
- **docs/ot/trading/06_TRADING_LAB_V1_MARKET_INPUT_PASS_01.md** : clôture documentaire de la première passe input marché LAB et définition du trigger naturel suivant.
- **docs/ot/trading/07_TRADING_LAB_V1_FEATURE_ENGINE_PASS_01.md** : clôture documentaire de la première passe feature engine LAB et définition du trigger naturel suivant.
- **docs/ot/trading/08_TRADING_LAB_V1_BATCH_PASS_01.md** : clôture documentaire de la première passe batch LAB et définition du trigger naturel suivant.
- **docs/ot/trading/09_TRADING_LAB_V1_BATCH_REPORTING_PASS_01.md** : clôture documentaire de la première passe batch reporting LAB et définition du trigger naturel suivant.
- **docs/ot/trading/10_TRADING_LAB_V1_REPORT_EXPORT_PASS_01.md** : clôture documentaire de la première passe report export LAB et définition du trigger naturel suivant.

## SCHÉMAS MACHINE-LISIBLES

- **docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml** : profil YAML V1 du focus `XAUUSD`.
- **docs/ot/trading/schemas/trading_event_v1.schema.json** : schéma JSON des événements V1.
- **docs/ot/trading/schemas/trading_trade_v1.schema.json** : schéma JSON des trades V1.

## MODULES LIÉS

- **modules/trading_lab_v1/** : squelette standard minimal du LAB V1, avec docs, scripts, runner Python, entrée marché CSV, feature engine initial, batch pass initial, batch reporting initial, et report export initial.

## ÉTAT ACTUEL DE LA ZONE

### Établi
- le principe **dual stack Lab + Real-Time** est cadré ;
- le **cadre trader humain** est retenu comme invariant ;
- le focus V1 initial est **Gold / XAUUSD**, fenêtres `18:00` et `00:00`, timezone `America/Montreal` ;
- la **core spec V1** du noyau commun est matérialisée ;
- les **schémas machine-lisibles V1** sont matérialisés ;
- le **squelette LAB V1** est posé ;
- une **première passe du runner LAB** est posée ;
- une **première passe input marché LAB** est posée ;
- une **première passe feature engine LAB** est posée ;
- une **première passe batch LAB** est posée ;
- une **première passe batch reporting LAB** est posée ;
- une **première passe report export LAB** est posée.

### Non encore matérialisé ici
- comparateur lab/live ;
- runner REAL-TIME.

## ORDRE DE LECTURE RECOMMANDÉ

1. lire `00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
2. lire `01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`
3. lire `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
4. lire `03_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01.md`
5. lire `04_TRADING_LAB_V1_SKELETON_01.md`
6. lire `05_TRADING_LAB_V1_FIRST_RUNNER_PASS_01.md`
7. lire `06_TRADING_LAB_V1_MARKET_INPUT_PASS_01.md`
8. lire `07_TRADING_LAB_V1_FEATURE_ENGINE_PASS_01.md`
9. lire `08_TRADING_LAB_V1_BATCH_PASS_01.md`
10. lire `09_TRADING_LAB_V1_BATCH_REPORTING_PASS_01.md`
11. lire `10_TRADING_LAB_V1_REPORT_EXPORT_PASS_01.md`
12. seulement ensuite ouvrir l’implémentation suivante

## POINT DE REPRISE COURT

Trigger courant clos au niveau report export : `GO_OT_TRADING_LAB_V1_REPORT_EXPORT_PASS_01`

Trigger naturel suivant : `GO_OT_TRADING_LAB_V1_COMPARATOR_PASS_01`
