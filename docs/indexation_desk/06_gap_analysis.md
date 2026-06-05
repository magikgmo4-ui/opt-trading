# 06_gap_analysis.md

## Résumé exécutif
L’indexation ne révèle pas un manque de briques fonctionnelles. Elle révèle surtout un manque de **cohérence d’exposition**, de **nomenclature**, et de **packaging opérateur** pour les modules déjà présents.

---

## GAP-01 — Couverture incomplète des wrappers globaux pour les modules cœur Desk Pro
### Constat
De nombreux modules cœur disposent de `menu.sh / cmd.sh / sanity_check.sh`, mais n’apparaissent pas comme wrappers globaux visibles dans `/usr/local/bin`.

### Modules concernés (à vérifier/prioriser)
- `derivatives_analyzer`
- `derivatives_collector`
- `decision_engine`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `execution_engine`
- `journal_engine`
- `liquidation_analyzer`
- `market_scanner`
- `opportunity_ranker`
- `perf_engine`
- `portfolio_engine`
- `position_engine`
- `probability_engine`
- `risk_engine`

### Impact
Les briques existent mais ne sont pas toutes opérables de manière homogène par l’utilisateur ou l’opérateur système.

### Priorité
**Haute**

---

## GAP-02 — Incohérences de nommage entre modules, wrappers et aliases
### Constat
Des variantes de noms coexistent déjà dans `/usr/local/bin`, par exemple :
- `menu-desk-pro` et `menu-desk_pro`
- `sanity-desk-pro` et `sanity-desk_pro`
- alias historiques ou hybrides autour de desk/student/ops

### Impact
- confusion opérateur
- difficulté à documenter une surface stable
- risque de duplication ou de wrapper “fantôme”

### Priorité
**Haute**

---

## GAP-03 — Wrappers présents sans visibilité claire sur une structure module standard
### Constat
Certains wrappers globaux existent alors que l’inventaire standard `modules/**/scripts/(menu|cmd|sanity)` ne montre pas la même structure de façon évidente.

### Exemples à vérifier
- `bot_vision_step2`
- `deepseek_hub`
- `journal_de_bord` (legacy retire depuis)
- `shared_sshfs_permanent`

### Hypothèses
- wrappers pointant vers des scripts hors structure standard
- héritage historique / exceptions
- modules non encore réalignés au standard actuel

### Priorité
**Moyenne à haute**

---

## GAP-04 — Mélange partiel entre surfaces opérateur, dev et maintenance
### Constat
Le repo contient à la fois :
- engines métier
- dashboards et orchestrateurs
- modules ops / menus / wrappers
- modules réseau et maintenance
- couches historiques de correctifs

Mais la séparation **opérateur / dev / maintenance** n’est pas encore matérialisée dans une cartographie simple et utilisable.

### Impact
Sans clarification, le futur desk MSI risque d’exposer trop d’outils techniques, ou au contraire de masquer des briques utiles.

### Priorité
**Haute**

---

## GAP-05 — Dette structurelle historique présente dans le repo
### Signaux observés
- `workflow_post_change_v2`, `fix1`, `fix2`, `fix3`
- `reseau_ssh_step1b` / `reseau_ssh_step2` avec imbrications inhabituelles
- `modules/scripts/scripts/...`
- répertoires `_hold`, `_hold_untracked_before_merge_*`, `_work/*`, archives diverses

### Impact
- lisibilité réduite
- risque d’erreur humaine pendant l’évolution
- classification plus difficile

### Règle
**À ne pas refactorer dans cette phase**. À documenter, puis traiter plus tard par chantier dédié.

### Priorité
**Moyenne**

---

## GAP-06 — Couche exploitation réelle encore partielle pour la chaîne Desk Pro unifiée
### Constat
Les services actifs observés concernent surtout :
- `tv-perf`
- `tv-webhook`
- `vision_bot`
- `bot_vision_step2`
- `ngrok-tv`

La chaîne Desk Pro cœur n’apparaît pas encore comme une couche systemd homogène, clairement packagée et pilotable de bout en bout.

### Impact
- backend partiellement industrialisé
- difficulté à savoir ce qui est “en prod locale” vs “prêt mais pas branché”

### Priorité
**Moyenne à haute**

---

## GAP-07 — Mapping écrans / machines encore implicite, pas encore consolidé dans l’inventaire final
### Constat
Le modèle cible Dell / admin-trading / MSI / Debian réseau est connu, mais il n’est pas encore converti en structure opératoire finale validée.

### Impact
- risque de mauvaise allocation des modules
- risque de lancer trop tôt des travaux d’écran réseau ou d’API sans couche UI stabilisée

### Priorité
**Haute**

---

## GAP-08 — Documentation riche mais encore peu synthétisée côté “surface opérateur réelle”
### Constat
La doc est abondante (`docs/admin_trading_desk_pro*`, `docs/desk_pro_multi_machine*`, runbooks modules, etc.), mais la doc “voici ce que l’opérateur lance et regarde réellement” n’est pas encore consolidée à partir de l’inventaire.

### Priorité
**Moyenne**

---

## Ordre recommandé de traitement des gaps
1. **standardiser la surface opérateur Desk Pro**
2. **clarifier nommage et wrappers globaux**
3. **séparer opérateur / dev / maintenance**
4. **stabiliser la cartographie MSI / admin-trading / Debian réseau**
5. **ensuite seulement** reprendre l’extension écran réseau et l’intégration API large

## RISKS

- À qualifier.
