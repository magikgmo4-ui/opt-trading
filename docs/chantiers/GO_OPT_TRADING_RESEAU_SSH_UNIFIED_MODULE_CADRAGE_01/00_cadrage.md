---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - unified_module
  - aliases
  - wrappers
  - compat
surface: modules
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - scripts/reseau_ssh/install_reseau_ssh.sh
  - modules/reseau_ssh_step2/scripts/install_shortcuts.sh
  - modules/reseau_ssh_step1b/README.md
---

# GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 — Cadrage

## Objet

Fixer le cadrage enfant de convergence vers un module SSH unique, en bornant explicitement la compatibilité transitoire des alias et wrappers sans lancer de fusion physique.

---

## Intention

- préserver la continuité opérateur pendant le cadrage du module unique
- rendre explicite ce qui doit rester maintenu à titre transitoire
- subordonner toute rupture à l'audit des callers runtime et wrappers consommés

---

## Besoin initial

Le parent a fixé la cible d'un module SSH unique, mais la convergence reste bloquée tant que la compatibilité transitoire n'est pas cadrée explicitement pour :

- les alias opérateur encore publiés
- les wrappers encore susceptibles d'être consommés
- la séparation entre runtime actif, survivant de famille et compatibilité legacy

---

## Cible finale

Obtenir un cadrage stable qui permette ensuite de décider, sans spéculation et sans rupture prématurée :

- quels alias doivent rester conservés pendant la transition
- quels wrappers doivent rester maintenus pendant l'audit
- quelles règles bornent la coexistence entre runtime actif, `step1b` et `step2`
- sous quelles conditions un retrait futur devient légitime

---

## Plan validé

1. figer les alias et wrappers à maintenir pendant la phase transitoire
2. borner explicitement les règles de compatibilité transitoire
3. fixer les conditions de retrait futur sans décider la fusion physique
4. laisser l'implémentation et les retraits à un GO séparé après audit complet des callers

---

## État établi courant

- le parent confirme `modules/reseau_ssh_step2` comme survivant canonique de famille
- le parent confirme `modules/reseau_ssh_step1b` comme prérequis utile intermédiaire
- le parent confirme `modules/reseau_ssh` comme legacy / doc pré-step
- le parent interdit la fusion physique immédiate
- le parent impose l'audit des callers runtime et wrappers avant toute fusion physique
- le runtime actif actuel reste `scripts/reseau_ssh/`

---

## Gap restant

- auditer les callers réels des wrappers historiques et des installeurs encore consommés
- qualifier la surface opérateur réellement utilisée pendant la coexistence
- décider la stratégie de retrait ou de convergence uniquement après cet audit

---

## Compatibilité transitoire — alias et wrappers

### ETABLI
- Le runtime actif actuel reste `scripts/reseau_ssh/`.
- Le survivant canonique de famille reste `modules/reseau_ssh_step2`.
- `modules/reseau_ssh_step1b` reste un prérequis utile intermédiaire.
- `modules/reseau_ssh` reste au niveau legacy / doc pré-step.
- Les aliases courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` restent la surface opérateur canonique actuelle.
- Les aliases suffixes `menu-reseau_ssh_step2`, `cmd-reseau_ssh_step2`, `sanity-reseau_ssh_step2` sont tolérés comme compatibilité transitoire pour `reseau_ssh_step2`.
- Les scripts racine historiques de type `scripts/reseau_ssh_cmd.sh` et `scripts/reseau_ssh_menu.sh` ne sont pas des points de vérité canoniques par simple présence.
- Le runtime actif ne doit pas être écrasé implicitement par `modules/reseau_ssh*`.

### Alias à conserver
- alias : `menu-reseau_ssh`
  - rôle : surface opérateur canonique actuelle
  - source : `scripts/reseau_ssh/install_reseau_ssh.sh`
  - condition de maintien : tant que `scripts/reseau_ssh/` reste le runtime actif canonique et qu'aucune migration runtime validée ne redéfinit la surface opérateur
- alias : `cmd-reseau_ssh`
  - rôle : surface opérateur canonique actuelle
  - source : `scripts/reseau_ssh/install_reseau_ssh.sh`
  - condition de maintien : même condition
- alias : `sanity-reseau_ssh`
  - rôle : surface opérateur canonique actuelle
  - source : `scripts/reseau_ssh/install_reseau_ssh.sh`
  - condition de maintien : même condition
- alias : `menu-reseau_ssh_step2`
  - rôle : surface module explicite tolérée pour `reseau_ssh_step2`
  - source : `modules/reseau_ssh_step2/scripts/install_shortcuts.sh`
  - condition de maintien : compatibilité transitoire seulement ; ne remplace pas les aliases courts
- alias : `cmd-reseau_ssh_step2`
  - rôle : surface module explicite tolérée pour `reseau_ssh_step2`
  - source : `modules/reseau_ssh_step2/scripts/install_shortcuts.sh`
  - condition de maintien : même condition
- alias : `sanity-reseau_ssh_step2`
  - rôle : surface module explicite tolérée pour `reseau_ssh_step2`
  - source : `modules/reseau_ssh_step2/scripts/install_shortcuts.sh`
  - condition de maintien : même condition

### Wrappers à maintenir
- wrapper : `scripts/reseau_ssh/install_reseau_ssh.sh`
  - rôle : publication de la surface opérateur canonique actuelle
  - condition de maintien : tant que `scripts/reseau_ssh/` reste le runtime actif
- wrapper : wrappers / installeurs historiques de `step1b`
  - rôle : compatibilité legacy, non doctrine cible
  - condition de maintien : tant que l'audit des dépendances entrantes et wrappers consommés n'a pas borné ou retiré cette compatibilité
- wrapper : `scripts/reseau_ssh_cmd.sh`
  - rôle : reliquat / compatibilité historique
  - condition de maintien : pas de suppression avant audit complet des callers et revalidation explicite
- wrapper : `scripts/reseau_ssh_menu.sh`
  - rôle : reliquat / compatibilité historique
  - condition de maintien : même condition

### Règles de compatibilité transitoire
- Les aliases courts restent la surface opérateur canonique tant qu'aucune migration runtime n'est validée.
- Les aliases suffixes `step2` sont tolérés comme surface module explicite et ne remplacent pas les aliases courts.
- `step2` survivant canonique de famille ne vaut pas à lui seul validation comme runtime opérateur canonique.
- `step1b` reste un prérequis utile intermédiaire et ne devient pas le publicateur canonique final.
- Toute republication des aliases courts par `step1b` doit être lue comme compatibilité legacy.
- Les surfaces historiques homonymes hors `scripts/reseau_ssh/` restent non canoniques sauf revalidation explicite.
- Toute évolution de la surface opérateur active doit être traitée comme sujet runtime.

### Conditions de retrait futur
- Valider explicitement une cible runtime canonique unique.
- Revalider la publication canonique des aliases courts sur cette cible unique.
- Borner ou retirer la compatibilité legacy `step1b` par GO explicite.
- Faire converger sans ambiguïté la documentation opérateur et les installateurs.
- Terminer l'audit complet des callers runtime et wrappers consommés avant tout retrait.
- Ne retirer un alias ou wrapper que si son équivalent canonique unique est prouvé.

### Contraintes
- pas de rupture avant audit complet des callers
- pas de suppression tant que l'équivalent canonique unique n'est pas prouvé
- tout retrait doit avoir une condition explicite de sortie

---

## Next step

- auditer les callers runtime et wrappers consommés avant toute décision de fusion physique ou de retrait

---

## Statut

**OPEN — cadrage enfant créé pour borner la compatibilité transitoire avant toute convergence physique vers un module SSH unique**

## RISKS

- À qualifier.
