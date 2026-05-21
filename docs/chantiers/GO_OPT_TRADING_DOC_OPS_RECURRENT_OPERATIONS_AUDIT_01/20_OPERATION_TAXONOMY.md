# 20_OPERATION_TAXONOMY.md

## Taxonomie des opérations récurrentes basée sur l'analyse des données

### Niveau CORE (Opérations fondamentales, quasi-universelles)

1. **Vérification état réel Git**
   - Fréquence: Très élevée (présente dans presque chaque chantier)
   - Preuves: git status, git fetch --prune, comparaison avec origin/sot/mainline
   - Chantiers concernés: Tous
   - Rôle: Première étape de toute opération pour éviter les hypothèses mémoire

2. **Lecture du canon avant action**
   - Fréquence: Très élevée
   - Preuves: Consultation systématique de MATRICE_DOC_OPS_MASTER_MATRIX_01, GO_INDEX, ACTIVE_STREAMS, REPRISE, BRANCH_STATE
   - Chantiers concernés: Majorité
   - Rôle: Assurer l'alignement avec la gouvernance établie

3. **Création/reprise de GO borné**
   - Fréquence: Élevée
   - Preuves: 566 dossiers chantiers, nommage GO_<SCOPE>_<SURFACE>_<ROLE>_<OBJECT>_<NN>
   - Chantiers concernés: Tous les chantiers
   - Rôle: Isoler le travail selon les principes de la matrice

4. **Documentation initiale du chantier**
   - Fréquence: Élevée
   - Preuves: 152 fichiers 00_INITIAL_PROJECT_DOC.md
   - Chantiers concernés: ~27% des chantiers
   - Rôle: Cadrage initial, objectifs, contraintes

### Niveau FREQUENT (Opérations très communes)

5. **Documentation de clôture**
   - Fréquence: Très élevée
   - Preuves: 415 fichiers de closeout (90_CLOSEOUT.md ou *CLOSEOUT*.md)
   - Chantiers concernés: ~73% des chantiers ayant un init
   - Rôle: Synthèse des résultats, preuves, verdicts

6. **Entrée inbox pour découvrabilité**
   - Fréquence: Élevée
   - Preuves: 174 entrées dans docs/index/inbox/
   - Chantiers concernés: Majorité des chantiers parents significatifs
   - Rôle: Maintenir la continuité parent-enfant sans modifier les gros index

7. **Utilisation de mots-clés de statut**
   - Fréquence: Très élevée
   - Preuves: PASS (5376), FAIL (2322), BLOCKED (786), PARTIAL (138)
   - Chantiers concernés: Presque tous les chantiers avec validation
   - Rôle: Standardiser la communication des résultats

8. **Opérations de reprise et planification**
   - Fréquence: Élevée
   - Preuves: REPRISE (1365), NEXT_GO (1010)
   - Chantiers concernés: Chantiers en cours ou récemment fermés
   - Rôle: Assurer la continuité entre les chantiers

### Niveau SUPPORT (Opérations de soutien régulières)

9. **Validation et tests**
   - Fréquence: Élevée
   - Preuves: validation (2124), smoke (703), dry-run (709)
   - Chantiers concernés: Chantiers impliquant des changements techniques
   - Rôle: S'assurer que les changements respectent les contraintes

10. **Gestion de registre et configuration**
    - Fréquence: Élevée
    - Preuves: registry (1549), strategy_id (575)
    - Chantiers concernés: Chantiers liés à la gouvernance, stratégies, workers
    - Rôle: Maintenir la cohérence des composants configurables

11. **Opérations sur surfaces spécifiques**
    - Fréquence: Variable selon la surface
    - Preuves: 
      - OpenClaw (2075) - interface/automatisation
      - tmux (1644) - orchestration/deploiement
      - Desk Pro (1152) - UI/productization
      - Telegram (898) - notifications/alertes
    - Chantiers concernés: Spécifiques à chaque surface
    - Rôle: Maintenir et développer les composants surface-spécifiques

### Niveau OCCASIONAL (Opérations moins fréquentes mais significatives)

12. **Contraintes d'accès restreint**
    - Fréquence: Faible à nulle dans le comptage direct
    - Preuves: READ_ONLY (158), DOC_ONLY (385)
    - Chantiers concernés: Chantiers de gouvernance, audit, documentation pure
    - Rôle: Protéger l'intégrité du système pendant les opérations sensibles

13. **Travail sur workers stricts**
    - Fréquence: Modérée
    - Preuves: strict-workers (123)
    - Chantiers concernés: Chantiers liés à la validation des job packets, modèles
    - Rôle: Assurer la conformité des workers aux exigences de sécurité

### Patterns de surface observés (top 5 combinaisons)

1. **OPT_TRADING_ADMIN** (81 chantiers) - Gouvernance, configuration, administration
2. **OPT_TRADING_DOC** (52 chantiers) - Documentation pure, standards, procédures
3. **OPENCLAW_OPT_TRADING** (48 chantiers) - Interface d'automatisation, intégrations
4. **OPT_TRADING_CURSOR** (28 chantiers) - Outils de développement, assistants AI
5. **OPT_TRADING_DESKPRO** (24 chantiers) - Interface utilisateur, productisation

## Synthèse du workflow dominant

Le workflow le plus récurrent observable est :
1. Vérifier l'état réel Git (status, fetch)
2. Lire le canon (matrice, index, reprise)
3. Créer ou reprendre un GO borné avec nommage standardisé
4. Documenter l'initialisation (00_INITIAL_PROJECT_DOC.md)
5. Effectuer le travail (variable selon la surface)
6. Valider/tester (smoke, dry-run, validation)
7. Documenter les résultats avec mots-clés de statut (PASS/FAIL/BLOCKED/PARTIAL)
8. Créer une entrée inbox pour la découvrabilité
9. Documenter la clôture (90_CLOSEOUT.md ou similaire)
10. Planifier la reprise ou le prochain GO (REPRISE, NEXT_GO)

Ce schéma apparaît dans la majorité des chantiers analysés, variant principalement selon la surface d'intervention et le type de travail effectué.