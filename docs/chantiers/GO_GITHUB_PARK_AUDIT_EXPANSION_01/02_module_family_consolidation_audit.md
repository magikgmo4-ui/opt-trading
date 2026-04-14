---
doc_id: OPT_TRADING_GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01
doc_type: chantier_report
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01
status: closed
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - families
  - consolidation
  - audit
surface: modules
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
  - docs/governance/GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03.md
---

# GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01

## Objet

Auditer les familles de modules dans `opt-trading` à partir du trunk ZIP réel, afin de distinguer :

- familles stables
- familles versionnées / step-by-step
- familles parallèles à clarifier
- reliquats legacy
- écarts entre parc réel et couche canonique registry

---

## Besoin initial

Le croisement `branches ↔ trunks` a montré que le vrai nœud restant du parc actif se concentrait désormais dans `opt-trading`, non plus au niveau global des repos mais dans la structure interne de `modules/`.

Le besoin était donc de lire le parc module par module, puis de regrouper les modules par familles réellement observables.

---

## Cible finale

Obtenir une lecture exploitable des familles de modules, permettant ensuite :

- des consolidations physiques ciblées
- une future cartographie fichier par fichier
- des décisions plus fiables sur les survivants, archives et miroirs

---

## Périmètre et méthode

### Source réelle utilisée
- trunk ZIP `opt-trading` (`sot/mainline`) réellement inspecté

### Méthode
1. recensement des modules présents sous `modules/`
2. croisement avec `registry/modules_registry.yaml`
3. regroupement par familles nominales et structurelles
4. classement par nature de consolidation

Cette passe est un audit de structure.
Elle ne supprime aucun module et ne reclassifie pas physiquement le repo.

---

## État établi — vue globale

### Taille du parc
- modules inspectés : **87**

### Couverture registry
- modules présents dans `registry/modules_registry.yaml` : **29**
- modules présents dans `modules/` mais absents de la registry : **58**

### Profil de standardisation wrappers
- modules avec triade `cmd/menu/sanity_check` : **62**
- modules avec triade `cmd/menu/sanity` : **11**
- modules sans wrappers standards détectés : **11**
- modules avec profil atypique résiduel : **3**

### Conclusion globale
Le parc `modules/` est **fortement standardisé en surface opérateur**, mais **faiblement reflété dans la registry canonique**.

Le principal gap n’est donc pas seulement la présence de quelques doublons nominatifs.
Le principal gap est aussi le décalage entre :
- le parc réel des modules
- la couche canonique de description / statut / priorité

---

## Familles auditées — verdicts structurants

### A. Familles déjà identifiées comme lignées de consolidation

#### `workflow_post_change_v2*`
Modules :
- `workflow_post_change_v2`
- `workflow_post_change_v2_fix1`
- `workflow_post_change_v2_fix2`
- `workflow_post_change_v2_fix3`

Verdict :
- famille déjà consolidée côté continuité
- survivant live = `workflow_post_change_v2`
- `fix3` = historique déjà mergé
- `fix1` / `fix2` = historiques obsolètes

Statut retenu dans cet audit :
- **famille clôturable**, sauf éventuelle suppression physique ultérieure si un GO dédié le demande

#### `reseau_ssh*`
Modules :
- `reseau_ssh`
- `reseau_ssh_step1b`
- `reseau_ssh_step2`

Verdict :
- vraie lignée step-by-step
- famille non consolidée physiquement
- cible de continuité déjà retenue par la gouvernance antérieure : `reseau_ssh_step2`

Statut retenu dans cet audit :
- **candidat prioritaire de consolidation**

---

### B. Familles parallèles / stacks à clarifier plutôt qu’à fusionner aveuglément

#### `desk_pro*`
Modules :
- `desk_pro`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`

Verdict :
- famille réelle mais non strictement doublonnée
- coexistence plausible entre noyau, runner, dashboard, orchestrateur
- la famille a besoin d’une clarification des rôles, pas d’une fusion brutale

Statut retenu :
- **stack à cartographier**

#### `desk_*` hors `desk_pro*`
Modules :
- `desk_analyze`
- `desk_capture_inputs`
- `desk_common`
- `desk_retention`
- `desk_snapshot_ingest`
- `desk_state`

Verdict :
- sous-système desk plus large que `desk_pro`
- pas de doublon évident, mais plusieurs modules adjacents avec frontière à préciser

Statut retenu :
- **stack stable mais à cartographier**

#### `openclaw*`
Modules :
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `gateway_openclaw`
- `install_module_openclaw`
- `menu_openclaw`
- `model_provider_openclaw`
- `openclaw_config_modulaire`

Verdict :
- famille fortement structurée
- modules complémentaires, pas doublons simples
- gros écart entre richesse réelle de la famille et couverture registry

Statut retenu :
- **stack cohérente, mais à clarifier par cartographie de rôles et couverture registry**

#### `registry*`
Modules :
- `machines_registry_reader`
- `modules_registry_reader`
- `registry_meta_reader`
- `registry_router`
- `ui_registry_msi`
- `wrappers_registry_reader`

Verdict :
- famille outillage/lecture registry clairement réelle
- un seul module de la famille est actuellement porté comme actif dans la registry (`ui_registry_msi`)
- la famille a davantage un problème de couverture canonique qu’un problème de duplication

Statut retenu :
- **famille registry à cartographier**

#### `shared*`
Modules :
- `shared`
- `shared_files_sftp`
- `shared_sshfs_permanent`

Verdict :
- famille d’infrastructure cohérente
- pas de doublon simple
- hiérarchie plausible entre surface générale, couche SFTP et montage permanent

Statut retenu :
- **stack stable**

---

### C. Familles parallèles susceptibles de cacher des survivants concurrents

#### `vision`
Modules :
- `bot_vision`
- `bot_vision_step2`
- `vision_bot`

Verdict :
- vraie coexistence parallèle avec mélange de nomenclature step/nom final
- risque de confusion entre ancien step, point d’entrée et survivant réel

Statut retenu :
- **candidat réel de consolidation / clarification**

#### `deepseek`
Modules :
- `deepseek_hub`
- `deepseek_response`
- `deepseek_student`
- `deepseek_thinking`

Verdict :
- famille parallèle plausible
- pas de doublon prouvé par nom seul
- besoin fort de clarification des frontières et survivants fonctionnels

Statut retenu :
- **candidat de clarification**

#### `journal`
Modules :
- `journal_de_bord`
- `journal_engine`

Verdict :
- coexistence potentiellement intentionnelle, mais frontière non explicite à ce niveau d’audit
- risque de dualité moteur vs surface historique/opérateur

Statut retenu :
- **legacy + engine à clarifier**

#### `perf`
Modules :
- `perf`
- `perf_engine`

Verdict :
- coexistence de type legacy + engine plausible
- `perf_engine` apparaît comme survivant plus canonisable que `perf`
- clarification nécessaire avant tout nettoyage

Statut retenu :
- **legacy + engine à clarifier**

#### `trading`
Modules :
- `trading_lab_v1`
- `trading_realtime_v1`

Verdict :
- paire logique plus qu’un doublon
- besoin de frontière explicite Lab vs Real-Time

Statut retenu :
- **frontière à expliciter**

---

### D. Familles courtes mais saines

#### `derivatives`
Modules :
- `derivatives_analyzer`
- `derivatives_collector`

Verdict :
- paire pipeline cohérente
- collector partiellement moins formalisé côté registry que analyzer

Statut retenu :
- **famille saine, avec couverture canonique incomplète**

#### `ops`
Modules :
- `ops_menu_hub`
- `ops_super_menu`
- `ops_wrappers`

Verdict :
- famille opérateur réelle
- pas de fusion aveugle à faire
- besoin de préciser hiérarchie et place de `ops_super_menu`

Statut retenu :
- **famille partiellement clarifiée**

#### `collector`
Modules :
- `collector_binance_spot`
- `collector_coingecko`

Verdict :
- binômes de connecteurs plutôt que doublons
- faible priorité de consolidation structurelle

Statut retenu :
- **faible priorité**

---

## Singletons et parc diffus

Le parc contient aussi un grand nombre de modules isolés ou non familiaux à ce niveau de lecture, par exemple :

- `decision_engine`
- `risk_engine`
- `position_engine`
- `portfolio_engine`
- `probability_engine`
- `mimo_open_observer`
- `memory_bricks`
- `validated_prompt_factory`
- `trae_module_validator`
- `simex_bitget_bridge`
- `winscp_transfer`
- etc.

Verdict :
- pas de problème de famille détecté immédiatement
- la plupart relèvent davantage d’une future cartographie de rôle que d’une consolidation nominale

---

## Ce qui est établi à ce stade

1. Le parc modules d’`opt-trading` est très dense mais pas chaotique.
2. Le problème principal n’est pas un nombre massif de doublons exacts ; c’est un mélange de :
   - lignées versionnées
   - stacks multi-modules
   - survivants implicites non formalisés
   - faible couverture registry
3. Les candidats prioritaires de consolidation ou clarification sont :
   - `reseau_ssh*`
   - `vision`
   - `perf`
   - `journal`
   - `desk_pro*` / `desk_*`
   - `openclaw*`
4. `workflow_post_change_v2*` sort du cœur de dette active car sa continuité est déjà fixée.
5. La cartographie fichier par fichier devient désormais nécessaire pour distinguer clairement :
   - core
   - engine
   - operator surface
   - runtime surface
   - legacy
   - archive

---

## Limites réelles

Cette passe ne fait pas :

- la cartographie fichier par fichier
- la lecture sémantique complète de chaque README/module
- la reclassification physique des dossiers
- la mise à jour exhaustive de `registry/modules_registry.yaml`

---

## Next GO

### GO retenu
`GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01`

### Pourquoi
Parce que l’audit des familles montre que le vrai pas suivant n’est plus seulement de repérer des noms proches.
Il faut maintenant assigner à chaque fichier et sous-surface un rôle canonique stable :

- `doc`
- `code`
- `runtime`
- `gouvernance`
- `consumer`
- `legacy`

C’est cette couche qui permettra ensuite des consolidations physiques propres sans casser les frontières utiles.

---

## Verdict

**PASS — audit des familles de modules établi ; la suite logique devient la cartographie canonique fichier par fichier**
