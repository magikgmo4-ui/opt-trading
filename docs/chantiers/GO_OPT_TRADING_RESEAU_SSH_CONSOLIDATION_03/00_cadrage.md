---
doc_id: OPT_TRADING_GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - consolidation
  - modules
  - structure
  - canon
  - unified_module
surface: modules
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
---

# GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 — Cadrage

## Objet

Ouvrir le chantier de consolidation ciblée de la famille `reseau_ssh*` dans `opt-trading`, en s’appuyant sur la trilogie d’audit déjà établie.

---

## Intention

- ne pas rouvrir un audit de parc large
- partir maintenant sur une consolidation ciblée
- utiliser la cartographie comme base de tri entre :
  - survivant
  - runtime utile
  - doc/gouvernance
  - legacy

Cette intention doit rester visible et transmissible dans les prochains GO de la même trajectoire.

---

## Produits finaux voulus / objectifs du chantier

### Produit final voulu du GO
Pour la famille `reseau_ssh*`, obtenir un résultat où chaque élément est clairement trié et assumé comme :

- survivant
- runtime utile
- doc/gouvernance
- legacy

avec :

- une cible canonique unique
- une continuité non ambiguë
- une hiérarchie claire entre ce qui reste actif, ce qui doit être conservé comme preuve ou doctrine, et ce qui doit cesser de porter la continuité

### Objectif final de trajectoire
Contribuer à un repo :

- **100% consolidé**
- **aligné**
- à **structure claire**
- **ordonnée**
- sans parasite
- sans historique mal situé
- sans item mal structuré
- sans item mal indexé
- sans item mal situé
- sans item mal documenté
- sans item non canonisé

Cet objectif final doit être rappelé comme horizon dans la suite fluide des GO de consolidation.

---

## Objectifs

### Objectif immédiat du GO
Consolider la famille `reseau_ssh*` autour d’une cible canonique unique, avec séparation claire entre :

- survivant actif
- runtime utile encore nécessaire
- documentation / gouvernance à conserver
- reliquats legacy / historiques / étapes intermédiaires

### Objectif final de trajectoire
Aller vers un repo :

- **100% consolidé**
- **aligné**
- à **structure claire et ordonnée**
- sans parasite
- sans historique mal situé
- sans items mal structurés
- sans items mal indexés
- sans items mal situés
- sans items mal documentés
- sans items non canonisés

Cet objectif final vaut comme horizon de consolidation du repo, même si ce GO ne traite qu’une famille ciblée.

---

## Besoin initial

Les audits précédents ont établi que :

- la dette active du parc ne justifie plus un nouvel audit global
- `opt-trading` concentre le principal nœud de consolidation restante
- `reseau_ssh*` est la lignée versionnée la plus nette à consolider ensuite
- la cible de continuité retenue est déjà `reseau_ssh_step2`

Il faut maintenant transformer cette lecture en chantier opératoire borné.

---

## Cible finale

Obtenir, pour la famille `reseau_ssh*` :

- un survivant canonique explicite
- une hiérarchie claire des couches runtime / doc / legacy
- une suppression des ambiguïtés de continuité
- une reprise propre sans relecture globale du parc

Et, dans la continuité des GO suivants, garder explicites :

- l’intention de consolidation ciblée
- le target final de repo consolidé et canonisé

---

## Plan validé

### Lot 1 — état réel de la famille
- relire la famille `reseau_ssh`, `reseau_ssh_step1b`, `reseau_ssh_step2`
- identifier exactement ce qui relève de :
  - code / scripts actifs
  - wrappers / runtime utile
  - doc / gouvernance
  - historique / legacy

### Lot 2 — décision de consolidation
- confirmer le survivant canonique
- classer les autres dossiers comme :
  - absorbés
  - intermédiaires
  - legacy
  - archive

### Lot 3 — patch minimal de consolidation
- appliquer uniquement le minimum nécessaire pour aligner le repo sur cette décision
- documenter ce qui reste conservé pour historique

### Lot 4 — cadrage du module cible unique
- fixer explicitement le sous-chantier de convergence vers un module SSH unique
- documenter ce sous-chantier dans le parent pour ne plus dépendre de la session
- préparer ensuite un GO enfant dédié avant tout refactor physique

---

## État établi courant

### 1. Héritage des audits précédents
Les audits déjà clos ont établi :

- la cartographie fichier par fichier du parc
- l’audit des familles de modules
- la sortie des repos legacy hors parc actif
- la concentration de la dette active dans `opt-trading`

### 2. État établi sur `reseau_ssh*`
Famille observée :

- `modules/reseau_ssh`
- `modules/reseau_ssh_step1b`
- `modules/reseau_ssh_step2`

Établi à ce stade :
- il s’agit d’une vraie lignée step-by-step
- la cible de continuité retenue par les audits précédents est `reseau_ssh_step2`
- la consolidation documentaire racine de la famille a été absorbée sur `sot/mainline`
- la consolidation physique complète n’a pas encore été faite

### 3. Rôles séparés
- rôle repo : `opt-trading` porte le chantier
- rôle produit : consolidation structurelle interne du repo
- rôle IA/IDE : auditeur puis consolidateur ciblé
- rôle machine : non engagé tant qu’aucun patch runtime live n’est demandé

### 4. Point de continuité post-merge PR #152
État Git réel validé pour la reprise :

- branche courante correcte : `sot/mainline`
- worktree courant : propre
- tracking : `sot/mainline...origin/sot/mainline`
- tête réelle : `b35e4d4`
- merge PR `#152` bien présent dans l’historique réel au commit `bcee8fe`
- la branche `codex/reseau-ssh-runtime-compat-retirement-01-isolate` reste une branche historique, mais n’est plus la base de reprise active

Établi à ce stade :

- le blocage d’hygiène Git locale est levé
- il n’y a pas de divergence locale à corriger avant reprise
- l’état courant est plus avancé que le strict post-merge PR `#152`
- le lot fusionné par la PR `#152` reste strictement doc-only
- `NO_GO_PHYSICAL` reste maintenu

Conséquence de continuité :

- le prochain arbitrage n’est plus Git
- le prochain arbitrage redevient fonctionnel / documentaire
- la suite admissible est soit un maintien en pilotage doc-only, soit l’ouverture explicite d’un lot physique séparé, borné machine par machine, avec rollback et smoke tests

---

## Gap restant

Il reste à produire pour cette famille :

- la preuve détaillée du survivant réel
- la classification explicite de chaque sibling
- le correctif minimal de structure / doc / liens si nécessaire
- le cadrage durable du sous-chantier de convergence vers un module SSH unique
- l’audit des callers runtime et wrappers avant toute fusion physique

---

## Décision de consolidation — Lot 2

### Décision figée (repo-sourcée)
- **Survivant canonique confirmé** : `modules/reseau_ssh_step2`
- **Prérequis utile intermédiaire (à conserver à ce stade)** : `modules/reseau_ssh_step1b`
- **Legacy / doc-gouv pré-step** : `modules/reseau_ssh`

### Règles de consolidation retenues
- pas de fusion brutale de `step1b` vers `step2` dans ce lot
- pas d’archivage immédiat de `step1b`
- pas de suppression physique dans ce lot
- consolidation par patch minimal documenté, puis validation

### Ambiguïtés restantes à traiter en Lot 3
- formaliser explicitement, côté documentation de `step2`, la dépendance de préparation héritée de `step1b` (bootstrap SSH/Windows)
- décider si certains éléments doc de `reseau_ssh` restent en référence historique ou doivent être reclassés

---

## Patch minimal proposé — Lot 3 (préparation)

### Cible
Rendre explicite la hiérarchie de continuité sans suppression large :

- `step2` = survivant actif
- `step1b` = prérequis intermédiaire
- `step1` = legacy/doc

### Fichiers doc/structure à toucher (proposition)
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`
  - figer le verdict Lot 2 et le plan d’exécution Lot 3
- `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/README.md`
  - ajouter une note courte “prérequis step1b” (sans réécrire le fond)
- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/README.md`
  - marquer explicitement le statut “intermédiaire / prérequis”
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step1/README.md`
  - marquer explicitement le statut “legacy / doc-gouv pré-step”

### Hors-scope Lot 3
- suppression physique de dossiers
- refactor runtime
- migration massive de scripts
- commit/push automatiques

---

## Sous-chantier fixé dans le parent

### GO enfant retenu
`GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01`

### Besoin initial du sous-chantier
La famille `reseau_ssh*` est désormais clarifiée côté continuité documentaire, mais reste éclatée physiquement entre :

- `modules/reseau_ssh` (legacy / doc)
- `modules/reseau_ssh_step1b` (préparation hosts / ssh config / key tests)
- `modules/reseau_ssh_step2` (WireGuard / firewall / inventory)

Il faut fixer dans le repo, et non dans la session, que la cible finale de trajectoire est bien un **module SSH unique** — sans lancer une fusion brutale sans audit préalable.

### Cible finale du sous-chantier
Aboutir à un **module canonique unique** couvrant :

- inventory
- hosts
- ssh config
- key tests
- WireGuard
- firewall
- wrappers opérateur
- sanity
- documentation d’usage

avec disparition à terme des lignées parallèles actives `step1b` / `step2`, après convergence propre.

### Plan validé du sous-chantier
1. auditer les callers réels de `modules/reseau_ssh_step1b/scripts/*`
2. auditer les callers réels de `modules/reseau_ssh_step2/scripts/*`
3. comparer les surfaces utiles `step1b` et `step2`
4. définir la structure cible du module SSH unique
5. définir la stratégie de compatibilité transitoire (wrappers ou rupture assumée)
6. ouvrir ensuite un GO d’implémentation séparé si et seulement si le cadrage est stabilisé

### État établi du sous-chantier
- la famille est un candidat clair à la consolidation vers un module unique
- ce n’est pas encore un candidat à une fusion physique immédiate
- le blocage principal est l’absence d’audit complet des dépendances entrantes et des wrappers consommés

### Gap restant du sous-chantier
- cartographie des dépendances entrantes
- liste des chemins réellement consommés
- décision de compatibilité
- design cible unique suffisamment figé pour implémentation

---

## Next GO interne au chantier

### Prochaine étape opératoire immédiate
`GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01`

### Position de ce next GO dans le parent
- `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_01` est clos côté patch documentaire minimal
- le parent reste ouvert
- la suite naturelle du parent est désormais explicitement le cadrage du module unique SSH

### Arbitrage actif après validation Git
Le parent porte désormais explicitement le point de continuité suivant :

- état Git réel validé sur `sot/mainline`
- état canonique `reseau_ssh` confirmé
- lot PR `#152` relu comme lot doc-only uniquement
- `NO_GO_PHYSICAL` maintenu

Le prochain lot actif doit être choisi explicitement :

- soit continuité doc-only / pilotage
- soit ouverture d’un lot physique séparé

Ce choix ne peut pas être déduit du merge documentaire seul.

---

## Règle issue de ce cadrage

Pour cette suite :

- ne pas relancer un audit global du parc
- ne pas rouvrir des familles non prioritaires
- utiliser la cartographie comme base de tri
- documenter explicitement ce qui devient survivant, runtime utile, doc/gouvernance, legacy
- faire suivre explicitement, dans les GO suivants, **l’intention** et le **target final** du chantier pour garder une suite fluide
- ne pas lancer de fusion physique `step1b + step2` avant le cadrage du module unique et l’audit de dépendances

---

## Statut

**OPEN — cadrage parent maintenu, sous-chantier de convergence vers module unique fixé dans le parent**
