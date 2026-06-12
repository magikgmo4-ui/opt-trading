---
doc_id: OPT_TRADING_HUMAN_CONTINUITY_TRUTH_AND_SCOPE
doc_type: intent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - human_layer
  - continuity
  - truth
  - scope
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/HUMAN_FOUNDATIONS_CONTINUITY.md
  - docs/governance/HUMAN_CONTINUITY_ADAPTATION.md
  - docs/governance/HUMAN_CONTINUITY_OPERABILITY.md
  - docs/governance/HUMAN_CONTINUITY_TRANSMISSION.md
  - docs/governance/HUMAN_CONTINUITY_CORRECTION.md
  - docs/governance/HUMAN_CONTINUITY_TIME.md
  - docs/governance/HUMAN_CONTINUITY_CALIBRATION.md
  - docs/governance/HUMAN_CONTINUITY_CANON_USAGE.md
  - docs/governance/HUMAN_CONTINUITY_EVOLUTION.md
  - docs/governance/HUMAN_CONTINUITY_METHOD.md
  - docs/governance/HUMAN_CONTINUITY_DECISION_BOUNDS.md
  - docs/governance/HUMAN_CONTINUITY_MATURITY.md
  - docs/governance/HUMAN_CONTINUITY_OWNERSHIP.md
  - docs/governance/HUMAN_CONTINUITY_CONDITIONS.md
  - docs/governance/HUMAN_CONTINUITY_ECONOMY.md
  - docs/governance/HUMAN_CONTINUITY_TEMPORAL_READING.md
  - docs/governance/HUMAN_CONTINUITY_EXIT_REGIMES.md
  - docs/governance/HUMAN_CONTINUITY_REVERSIBILITY.md
  - docs/governance/HUMAN_CONTINUITY_LAYER_AUTHORITY.md
  - docs/governance/HUMAN_CONTINUITY_SYSTEM_BOUNDARIES.md
---

# HUMAN_CONTINUITY_TRUTH_AND_SCOPE

## Objet

Ce document fixe les principes humains de vérité et de bornage de la continuité, tels qu’ils ressortent des extractions de continuité conservées.

Il complète les blocs humains déjà posés en explicitant la hiérarchie des sources de vérité, la protection des sujets réellement clos, la préférence pour le plus petit scope réellement tenable, et la correspondance stricte entre trigger de reprise et état réellement pilotable.

---

## 1. Les sources de vérité doivent rester hiérarchisées explicitement

La continuité utile devait garder une hiérarchie explicite entre ses sources de vérité.

Lorsque mémoire, documentation, canon Git et état réel divergeaient, la reprise ne devait pas arbitrer implicitement.
Il fallait pouvoir relire ce qui faisait autorité en priorité, notamment :
- l’état réel machine ou repo
- le canon validé
- la mémoire ou les reconstructions secondaires

---

## 2. Les sujets réellement clos ne doivent pas être rouverts sans raison nouvelle

La continuité utile devait protéger les sujets réellement clos contre les réouvertures par oubli, confusion ou reprise mal cadrée.

Un chantier fermé ne devait redevenir actif qu’en présence d’une raison nouvelle explicite.
À défaut, la reprise devait pouvoir relire clairement que le travail avait déjà atteint un état suffisamment établi pour ne pas être retraité comme s’il restait ouvert.

---

## 3. Le plus petit scope réellement tenable doit être préféré

La continuité utile devait préférer le plus petit scope réellement tenable au grand plan théorique mal borné.

Un patch minimal, une lecture utile courte ou une promotion strictement limitée pouvaient avoir plus de valeur de continuité qu’une ambition plus large, dès lors qu’ils :
- préservaient l’existant
- clarifiaient la validation
- évitaient de rouvrir inutilement des surfaces déjà closes

---

## 4. Un trigger de reprise doit correspondre à un état réel pilotable

La continuité utile devait faire correspondre chaque trigger de reprise à un état réel pilotable.

Un GO ne devait pas être seulement un nom.
Il fallait pouvoir relire :
- sa machine porteuse
- son niveau d’autorité
- son dernier point établi
- son prochain pas utile
- son blocage réel si nécessaire

---

## 5. Principe de vérité et de bornage

Une continuité robuste ne doit pas seulement conserver des intentions.
Elle doit aussi rendre lisibles :
- ce qui fait réellement autorité
- ce qui est réellement clos
- ce qui est réellement tenable dans le scope courant
- ce qui rend un trigger réellement opérable

---

## 6. Statut

Bloc humain complémentaire.
À utiliser comme référence de vérité et de bornage de la continuité, sans le substituer aux closeouts, index, reprises ni à la compaction.

## RISKS

- À qualifier.
