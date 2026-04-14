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
surface: modules
source_kind: canonical
updated_at: 2026-04-14
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
- la consolidation physique n’a pas encore été faite

### 3. Rôles séparés
- rôle repo : `opt-trading` porte le chantier
- rôle produit : consolidation structurelle interne du repo
- rôle IA/IDE : auditeur puis consolidateur ciblé
- rôle machine : non engagé tant qu’aucun patch runtime live n’est demandé

---

## Gap restant

Il reste à produire pour cette famille :

- la preuve détaillée du survivant réel
- la classification explicite de chaque sibling
- le correctif minimal de structure / doc / liens si nécessaire

---

## Next GO interne au chantier

### Prochaine étape opératoire immédiate
`GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` — lot audit détaillé de la famille

Ce même GO reste le contenant du chantier ; la prochaine action n’est pas un nouveau GO parc, mais l’exécution bornée de cette consolidation ciblée.

---

## Règle issue de ce cadrage

Pour cette suite :

- ne pas relancer un audit global du parc
- ne pas rouvrir des familles non prioritaires
- utiliser la cartographie comme base de tri
- documenter explicitement ce qui devient survivant, runtime utile, doc/gouvernance, legacy
- faire suivre explicitement, dans les GO suivants, **l’intention** et le **target final** du chantier pour garder une suite fluide

---

## Statut

**OPEN — cadrage posé, consolidation ciblée à exécuter**
