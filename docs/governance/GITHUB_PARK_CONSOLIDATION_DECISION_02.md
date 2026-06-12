---
doc_id: OPT_TRADING_GITHUB_PARK_CONSOLIDATION_DECISION_02
doc_type: governance_decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_GITHUB_PARK_CONSOLIDATION_DECISION_02
status: validated
lifecycle_stage: governance
topic_keys:
  - github
  - repo_inventory
  - park
  - consolidation
  - decision
surface: repo
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/REPO_ROLE.md
  - docs/ot/README.md
---

# GITHUB_PARK_CONSOLIDATION_DECISION_02

## Objet

Ce document fixe la décision de consolidation du parc GitHub à partir :

- de l’inventaire réel des trunks fournis
- de la lecture des rôles déjà documentés
- de l’inventaire des branches via GitHub
- des doublons réels ou familles multi-versions déjà établies

Il ne remplace pas les audits détaillés futurs.
Il fixe la **ligne de décision validée** pour éviter la dérive des rôles et la prolifération de doublons.

---

## Besoin initial

Obtenir une décision exploitable repo par repo et famille par famille :

- quoi garder
- quoi geler
- quoi archiver
- quoi traiter comme miroir
- quoi consolider dans un GO dédié

---

## Cible finale

Stabiliser le parc autour d’une répartition claire :

- `opt-trading` = canon exécution / modules / `memory_bricks`
- `openclaw` = canon transverse de gouvernance
- `localcms` = repo produit / consumer humain
- `llm_wiki_minimal` = pré-consolidation documentaire
- `hf_trading` = labo / amorçage
- les doublons et multi-versions = gelés puis traités dans des GO dédiés

---

## Plan validé

1. Ne pas fusionner à l’aveugle les repos ou familles proches.
2. Garder un seul canon par rôle.
3. Geler d’abord les surfaces concurrentes.
4. Consolider physiquement ensuite, par famille, dans des GO ciblés.
5. Documenter explicitement ce qui est validé pour éviter les réouvertures implicites.

---

## ETABLI

### Rôles de repo établis

#### `opt-trading`
Rôle retenu :
- repo canonique principal
- canon d’exécution
- canon structurel des modules durables
- source operative de `memory_bricks`

#### `openclaw`
Rôle retenu :
- canon transverse de gouvernance
- workflow
- statuts
- séquence GO

#### `localcms`
Rôle retenu :
- repo produit
- consumer humain
- continuité projet
- consumer de `memory_bricks`

#### `hf_trading`
Rôle retenu :
- repo de laboratoire / amorçage

#### `llm_wiki_minimal`
Rôle retenu :
- repo de pré-consolidation documentaire

#### `Llm-wiki`
État retenu :
- placeholder documentaire quasi vide
- pas de rôle distinct validé face à `llm_wiki_minimal`

#### `Magikgmo`
État retenu :
- surface legacy en fort chevauchement avec `opt-trading`
- pas de rôle distinct validé à ce stade

#### `algo_hf`
État retenu :
- repo à rôle encore non figé faute d’audit trunk complet

---

## Décisions validées — niveau repo

| Repo | Décision validée | Statut d’action |
|---|---|---|
| `opt-trading` | KEEP_CANONICAL_EXECUTION | actif |
| `openclaw` | KEEP_CANONICAL_GOVERNANCE | actif |
| `localcms` | KEEP_PRODUCT_CONSUMER | actif |
| `hf_trading` | KEEP_LAB_BOOTSTRAP | actif |
| `llm_wiki_minimal` | KEEP_PRECONSOLIDATION | actif |
| `Llm-wiki` | FREEZE_THEN_ARCHIVE_OR_REPURPOSE | gel de fait |
| `Magikgmo` | FREEZE_LEGACY_READ_ONLY_PENDING_AUDIT | gel logique |
| `algo_hf` | HOLD_PENDING_TRUNK_AUDIT | non tranché définitivement |

### Interprétation

#### 1. `opt-trading`
Validé comme repo dominant du parc pour :
- exécution réelle
- modules durables
- wrappers opératoires
- closeouts techniques locaux
- compaction structurée

Aucun second repo ne doit concurrencer `opt-trading` sur ce rôle.

#### 2. `openclaw`
Validé comme repo dominant pour :
- méthode transverse
- gouvernance
- statuts
- séquences GO
- garde-fous inter-repos

Aucun repo d’exécution ne doit devenir son doublon gouvernance.

#### 3. `localcms`
Validé comme repo produit/consumer.
Aucune tentative de le transformer en repo de gouvernance transverse ou en canon runtime principal n’est retenue.

#### 4. `hf_trading`
Validé comme lane laboratoire légère.
Pas de fusion imposée à ce stade.

#### 5. `llm_wiki_minimal`
Validé comme lane de pré-consolidation documentaire.
C’est la lane retenue pour ce rôle.

#### 6. `Llm-wiki`
Décision validée :
- ne pas développer en parallèle de `llm_wiki_minimal`
- geler
- archiver ou réaffecter seulement via décision explicite ultérieure

#### 7. `Magikgmo`
Décision validée :
- ne plus l’utiliser comme repo actif concurrent d’`opt-trading`
- le considérer legacy tant qu’un audit trunk complet n’a pas démontré un rôle réellement distinct
- aucune consolidation destructive immédiate n’est validée

#### 8. `algo_hf`
Décision validée :
- pas de fusion
- pas d’archivage
- audit trunk complet requis avant décision finale

---

## Décisions validées — doublons et multi-versions

### A. Frontière `openclaw` ↔ `opt-trading`

Décision validée :
- `openclaw` porte le **canon de gouvernance transverse**
- `opt-trading` porte le **runtime, l’évidence locale et les closeouts d’exécution**
- les contenus proches mais de nature différente ne doivent pas être fusionnés en masse
- les miroirs divergents doivent être remplacés par :
  - un original dominant
  - un lien croisé
  - ou une simple référence

Règle retenue :
- règle transverse = `openclaw`
- preuve locale, implémentation, runtime, evidence = `opt-trading`

---

### B. `Llm-wiki` ↔ `llm_wiki_minimal`

Décision validée :
- `llm_wiki_minimal` est retenu comme lane canonique de pré-consolidation
- `Llm-wiki` n’est pas retenu comme lane parallèle active
- `Llm-wiki` devient candidat d’archivage ou de réaffectation explicite

---

### C. `Magikgmo` ↔ `opt-trading`

Décision validée :
- `opt-trading` reste le repo canonique
- `Magikgmo` est gelé en statut legacy/read-only logique
- aucune nouvelle continuité active ne doit partir de `Magikgmo`
- un audit trunk dédié est requis avant toute décision de migration ou archivage final

---

### D. `localcms` — bundles et archives historiques

Décision validée :
- `INVENTORY_CANONICAL_SOURCES.md` est retenu comme liste source de conservation
- les bundles déclarés obsolètes ne doivent pas être réinjectés dans la continuité active
- `localcms_archive/` reste historique uniquement

---

### E. `opt-trading/modules/workflow_post_change_v2*`

Famille constatée :
- `workflow_post_change_v2`
- `workflow_post_change_v2_fix1`
- `workflow_post_change_v2_fix2`
- `workflow_post_change_v2_fix3`
- archive associée

Décision validée :
- gel immédiat de la prolifération de nouveaux siblings sur cette famille
- cible de consolidation retenue : **lignée `fix3` comme survivant candidat**
- consolidation physique à faire dans un GO dédié
- aucune nouvelle extension ne doit partir de `v2`, `fix1` ou `fix2` tant que la consolidation n’est pas faite

Note :
- le choix `fix3` est un **point d’atterrissage de consolidation**
- il ne vaut pas validation fonctionnelle complète tant qu’un GO de consolidation n’a pas clos la famille

---

### F. `opt-trading/modules/reseau_ssh*`

Famille constatée :
- `reseau_ssh`
- `reseau_ssh_step1b`
- `reseau_ssh_step2`

Décision validée :
- cible de continuité retenue : **`reseau_ssh_step2`**
- `step1b` est traité comme étape intermédiaire/historique
- `reseau_ssh` est traité comme base legacy/compat/documentation tant qu’une consolidation physique n’a pas été exécutée
- pas de nouvelle divergence latérale sur cette famille

---

### G. `opt-trading` — miroirs `student`

Doublons exacts établis :
- `student/docs/*.source.md` ↔ `docs/student_*.md`
- `student/scripts/wrappers/*` ↔ `scripts/student/*`
- `student/exports/kanban/KANBAN.csv` ↔ `docs/project_management/kanban/kanban_board.csv`

Décision validée :
- source dominante retenue :
  - `student/docs/*.source.md`
  - `student/scripts/wrappers/*`
  - `student/exports/kanban/KANBAN.csv`
- les copies sous `docs/` et `scripts/student/` sont traitées comme :
  - miroirs publiés
  - ou cibles de génération/sync
  - mais plus comme sources concurrentes

Règle retenue :
- une seule source éditable
- les autres surfaces = publication, export ou compatibilité

---

### H. Templates `cmd.sh` / `menu.sh` / `sanity_check.sh`

Décision validée :
- cette duplication est **structurelle et voulue**
- elle n’est pas traitée comme doublon métier
- aucune fusion fonctionnelle de ces scripts n’est demandée
- une éventuelle industrialisation par template/générateur est autorisée plus tard, sans changer la convention visible module par module

---

## Ce qui est explicitement validé

Est validé à partir de ce GO :

1. Le parc n’a pas plusieurs repos canoniques concurrents.
2. `opt-trading` reste la source canonique d’exécution.
3. `openclaw` reste la source canonique de gouvernance transverse.
4. `llm_wiki_minimal` est la lane retenue pour la pré-consolidation documentaire.
5. `Llm-wiki` n’est pas une lane active concurrente.
6. `Magikgmo` n’est pas une base de continuité active.
7. Les familles `workflow_post_change_v2*` et `reseau_ssh*` sont gelées côté prolifération.
8. Les miroirs `student` ne doivent plus être édités comme sources concurrentes.
9. Les bundles historiques obsolètes de `localcms` restent hors continuité active.

---

## Gap restant

Les points encore ouverts mais cadrés :

- audit trunk complet de `Magikgmo`
- audit trunk complet de `algo_hf`
- consolidation physique de `workflow_post_change_v2*`
- consolidation physique de `reseau_ssh*`
- normalisation de la chaîne miroir `student`
- synchronisation propre des frontières `openclaw` / `opt-trading`

---

## Next GO

### GO_GITHUB_PARK_MAGIKGMO_AUDIT_03
But :
- inspecter le trunk réel de `Magikgmo`
- décider archive finale vs extraction utile

### GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03
But :
- consolider la famille `workflow_post_change_v2*`
- atterrir sur une seule version live

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
But :
- consolider la famille `reseau_ssh*`
- figer le rôle final de `step2`

### GO_OPT_TRADING_STUDENT_MIRROR_NORMALIZATION_03
But :
- transformer les copies `docs/` et `scripts/student/` en miroirs assumés ou outputs générés
- garder `student/*` comme source dominante

### GO_OPENCLAW_OPT_TRADING_BOUNDARY_SYNC_03
But :
- nettoyer les chevauchements documentaires entre gouvernance transverse et evidence locale

### GO_GITHUB_PARK_ALGO_HF_AUDIT_03
But :
- inspecter le trunk de `algo_hf`
- trancher son rôle réel

---

## Règle de continuité issue de cette décision

Tant qu’un GO de consolidation dédié n’a pas clos une famille :

- on ne crée pas de nouveau sibling versionné
- on ne rouvre pas un repo gelé comme s’il était actif
- on n’édite pas un miroir comme source primaire
- on n’ajoute pas de seconde source canonique concurrente pour un même rôle

---

## Verdict

**PASS — décision de consolidation retenue**

Cette décision ne fait pas la consolidation physique à elle seule.
Elle fixe le cadre validé qui doit gouverner les prochains patchs et audits.

## RISKS

- À qualifier.
