# 30_REPO_EVIDENCE_MAP.md

## Preuves concrètes des opérations récurrentes

### Exemple 1: Cycle complet de chantier (GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01)
Chemin: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/

Fichiers présents:
- 00_INITIAL_PROJECT_DOC.md (cadrage initial)
- 10_SOURCE_STATE.md (audit de l'état existant)
- 20_AUTOMATION_GAP_ANALYSIS.md (analyse spécifique)
- 90_CLOSEOUT.md (synthèse des résultats)
- docs/index/inbox/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01.md (entrée inbox)

Mots-clés trouvés dans les documents:
- PASS, FAIL, BLOCKED (statuts de validation)
- REPRISE, NEXT_GO (planification)
- validation, dry-run, smoke (tests)
- OpenClaw (surface concernée)

### Exemple 2: Chantier de documentation pure (GO_OPT_TRADING_DOC_OPS_RECURRENT_OPERATIONS_AUDIT_01 - ce chantier)
Chemin: docs/chantiers/GO_OPT_TRADING_DOC_OPS_RECURRENT_OPERATIONS_AUDIT_01/

Fichiers présents ou à créer:
- 00_INITIAL_PROJECT_DOC.md (ce fichier)
- 10_RECURRENT_OPERATIONS_COUNTS.md (analyse quantitative)
- 20_OPERATION_TAXONOMY.md (classification qualitative)
- 30_REPO_EVIDENCE_MAP.md (preuves concrètes)
- 40_AUTOMATION_CANDIDATES.md (recommandations)
- 90_RESUME_POINT.md (point de reprise)
- docs/index/inbox/GO_OPT_TRADING_DOC_OPS_RECURRENT_OPERATIONS_AUDIT_01.md (entrée inbox)

Contraintes appliquées:
- READ_ONLY (vérifié par l'absence de modifications)
- DOC_ONLY (seulement de la documentation)
- Aucune modification des index globaux

### Exemple 3: Chantier de reprise (pattern REPRISE)
Recherche de fichiers contenant "REPRISE" dans leur nom ou contenu:
- 90_REPRISE.md (exemple: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_MODEL_REGISTRY_ENDPOINT_RECONCILIATION_01/90_REPRISE.md)
- 90_REPRISE_POINT.md
- Références fréquentes dans les documents de closeout et d'initialisation

### Exemple 4: Chantier avec BRANCH_STATE
Fichiers BRANCH_STATE.md trouvés (11 au total):
- docs/chantiers/GO_OPT_TRADING_AI_AGENT_ORCHESTRATION_WITH_OPENCLAW_01/BRANCH_STATE.md
- docs/chantiers/GO_OPT_TRADING_DB_LAYER_SCHEMA_MIGRATION_POSTGRES_TO_MONGODB_01/BRANCH_STATE.md
- etc.

Contenu typique:
- Branche actuelle
- État de synchronisation avec sot/mainline
- Instructions de reprise
- Contraintes spécifiques

### Preuves des fréquences de surfaces

#### OpenClaw (2075 occurrences)
Examples de chemins contenant OpenClaw:
- docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_*/ 
- docs/chantiers/GO_OPT_TRADING_OPENCLAW_*/
- docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_*/
- modules/openclaw/
- scripts/openclaw/

#### tmux (1644 occurrences)
Examples:
- docs/chantiers/GO_TMUX_IDE_OPT_*/
- docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_*/
- modules/tmux/
- scripts/tmux/
- runbooks/tmux/

#### Desk Pro (1152 occurrences)
Examples:
- docs/chantiers/GO_OPT_TRADING_DESKPRO_*/
- modules/deskpro/
- ui/deskpro/
- docs/runbooks/deskpro-*

#### Telegram (898 occurrences)
Examples:
- docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_*/
- modules/telegram/
- scripts/telegram/
- intégrations dans les workers et alertes

#### registry (1549 occurrences)
Examples:
- docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_MODEL_REGISTRY_*/
- modules/registry/
- configs/registry.json
- références dans les workers et job packets

### Preuves des contraintes de gouvernance

#### READ_ONLY (158 occurrences)
Principalement trouvé dans:
- docs/governance/ (matrices, politiques)
- runbooks/ (procédures opératoires)
- certains scripts de validation
- documentation de procédures

#### DOC_ONLY (385 occurrences)
Concentré dans:
- docs/chantiers/ (chantiers de documentation pure)
- docs/index/ (maintenance des index)
- certains runbooks et procédures

#### NO_RUNTIME_CHANGE et NO_GLOBAL_INDEX_CHANGE (0 occurrences directes)
Ces contraintes sont probablement appliquées implicitement plutôt qu'explicitement mentionnées, ou présentes dans des formulations variantes non capturées par la recherche exacte.

## Cartographie des flux de travail evidenciés

### Flux Type A: Chantier de développement standard
1. Vérification Git (status, fetch-prune)
2. Lecture canon (matrice, index, reprise)
3. Création GO avec nommage standard
4. 00_INITIAL_PROJECT_DOC.md (objectifs, contraintes)
5. Travail de développement (variable)
6. Tests/validation (smoke, dry-run, validation)
7. Mise à jour statut (PASS/FAIL/BLOCKED/PARTIAL)
8. Entrée inbox si chantier parent significatif
9. 90_CLOSEOUT.md (résultats, preuves, décision)
10. Références REPRISE/NEXT_GO pour continuité

### Flux Type B: Chantier de documentation/gouvernance
1. Même début (vérification Git, lecture canon)
2. Création GO DOC_* ou GOVERNANCE_*
3. 00_INITIAL_PROJECT_DOC.md (cadre, portée)
4. Analyse/recherche/documentation
5. Application contraintes spécifiques (READ_ONLY, DOC_ONLY)
6. Revue interne/validation par pairs
7. Statut DOC_ONLY_CLOSEOUT ou équivalent
8. Entrée inbox pour découvrabilité
9. 90_CLOSEOUT.md avec focus sur la décision de gouvernance
10. Mise à jour éventuelle de registres ou index mineurs

### Flux Type C: Chantier de reprise/continuité
1. Déclenché par référence REPRISE ou NEXT_GO
2. Consultation BRANCH_STATE.md si exists
3. Vérification état réel Git
4. Lecture canon mis à jour
5. Continuation du travail depuis point d'arrêt
6. Même séquence validation/clôture que autres flux

## Preuves de l'application de la matrice maîtresse

La matrice MATRICE_DOC_OPS_MASTER_MATRIX_01 est régulièrement référencée dans:
- 00_INITIAL_PROJECT_DOC.md (section contraintes)
- 90_CLOSEOUT.md (vérification conformité)
- Certains runbooks de procédure
- Documents de cadrage de chantier

Elle sert de référence pour:
- L'ordre d'arbitrage (état réel > matrice > annexes > surfaces > chantier)
- La détermination si une branche suffit comme preuve (elle ne suffit pas)
- Les règles de nommage des GO
- Les contraintes applicables par type de travail