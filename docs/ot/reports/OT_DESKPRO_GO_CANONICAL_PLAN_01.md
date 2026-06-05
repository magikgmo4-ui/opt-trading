# OT_DESKPRO_GO_CANONICAL_PLAN_01

Date (America/Montreal) : 2026-04-11

## 1. Objet
Formaliser, pour `opt-trading`, la distinction canonique entre :
1. le GO global de sélection ;
2. les missions Desk Pro candidates non-Trae ;
3. les chantiers DEV `fantome` qui ne doivent s’ouvrir qu’après sélection explicite.

Cette note ne modifie ni le kanban, ni le runtime, ni Trae Windows.

## 2. Règle canonique de sélection
- Le GO global de continuité reste : `GO_OT_NEXT_MISSION_SELECTION_01`.
- Tant qu’aucune mission n’est explicitement sélectionnée, il ne faut pas ouvrir de patch/runtime par défaut.
- Les missions listées ci-dessous sont des **candidates** sous ce GO global.
- Les chantiers DEV `fantome` ne sont pas des GO globaux de continuité ; ce sont des chantiers locaux/repo-first qui dérivent d’une mission candidate explicitement choisie.
- Trae reste hors périmètre de cette note ; les chantiers Trae continuent sur Windows / `cursor-ai`.

## 3. Distinction des niveaux

| Niveau | Rôle | Format | Exemple | Règle |
|---|---|---|---|---|
| Continuité canonique | Sélection prudente du prochain chantier | `GO_OT_*` | `GO_OT_NEXT_MISSION_SELECTION_01` | Toujours relire le canon avant d’ouvrir une mission |
| Mission candidate Desk Pro | Chantier canonique non-Trae à sélectionner | `OT_*` | `OT_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_01` | Ne devient active qu’après sélection explicite |
| Chantier DEV local | Travail repo-first sur `fantome` | `GO_FANTOME_*` | `GO_FANTOME_DESKPRO_INSTALLERS_WRAPPERS_INVENTORY_01` | S’ouvre seulement quand une mission candidate a été retenue |

## 4. Missions candidates non-Trae — file canonique Desk Pro

### 4.1 Priorité actuelle
1. `OT_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_01`
2. `OT_DESKPRO_RELEASE_OPS_DRILL_01`
3. `OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01`
4. `OT_DESKPRO_INSTALLERS_WRAPPERS_INVENTORY_01`
5. `OT_DESKPRO_RELEASE_REFERENCE_CONSOLIDATION_01`
6. `OT_DESKPRO_DB_LAYER_INGESTION_PREP_AUDIT_01`

### 4.2 Tableau de qualification

| Mission candidate | Nature | Portée | Machine logique | Sortie attendue |
|---|---|---|---|---|
| `OT_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_01` | audit / cadrage | repo-first + gouvernance wrappers admin | `fantome` (lecture repo) | verdict sur la coexistence doctrine vs install admin |
| `OT_DESKPRO_RELEASE_OPS_DRILL_01` | drill ops | release/tag proof | `admin-trading` + Linux targets | preuve que la chaîne release est réellement rejouable |
| `OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01` | drill ops multi-machine | export admin -> `/shared` -> lecture student/db-layer | `admin-trading`, `student`, `db-layer` | preuve de flux bout-en-bout |
| `OT_DESKPRO_INSTALLERS_WRAPPERS_INVENTORY_01` | audit repo-first | inventaire des installateurs et wrappers par machine | `fantome` | matrice wrappers installés vs doctrine |
| `OT_DESKPRO_RELEASE_REFERENCE_CONSOLIDATION_01` | doc-only | consolidation docs release | `fantome` | docs release moins dispersées |
| `OT_DESKPRO_DB_LAYER_INGESTION_PREP_AUDIT_01` | audit de cadrage futur | préparation ingestion db-layer | `fantome` | cadrage de la future couche d’ingestion |

## 5. Traduction en chantiers DEV `fantome`
Les chantiers DEV `fantome` recommandés, si les missions correspondantes sont retenues, sont :
- `GO_FANTOME_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_AUDIT_01`
- `GO_FANTOME_DESKPRO_INSTALLERS_WRAPPERS_INVENTORY_01`
- `GO_FANTOME_DESKPRO_RELEASE_REFERENCE_CONSOLIDATION_01`
- `GO_FANTOME_DESKPRO_DB_LAYER_INGESTION_PREP_AUDIT_01`

Les drills ops ne doivent pas être déguisés en chantiers DEV `fantome` :
- `OT_DESKPRO_RELEASE_OPS_DRILL_01`
- `OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01`

## 6. Règle de décision
Ordre recommandé :
1. conserver `GO_OT_NEXT_MISSION_SELECTION_01` comme seul GO global actif ;
2. choisir explicitement une mission candidate ;
3. seulement ensuite ouvrir, si nécessaire, le chantier DEV `fantome` correspondant ;
4. ne pas mélanger Trae Windows et Desk Pro non-Trae dans le même flux de reprise.

## 7. Point de reprise
- GO global conservé : `GO_OT_NEXT_MISSION_SELECTION_01`
- Tête de file non-Trae actuelle : `OT_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_01`
- Chantier DEV `fantome` recommandé si cette mission est retenue : `GO_FANTOME_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_AUDIT_01`

## 8. Limites
- Cette note ne change aucun statut du kanban.
- Cette note n’ouvre aucune mission automatiquement.
- Cette note ne remplace pas le kanban ni les closings.

MEM_CANDIDATE
NO_MEMORY

## RISKS

- À qualifier.
