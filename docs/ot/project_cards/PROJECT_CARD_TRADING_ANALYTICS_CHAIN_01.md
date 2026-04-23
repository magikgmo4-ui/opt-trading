---
doc_id: OPT_TRADING_PROJECT_CARD_TRADING_ANALYTICS_CHAIN_01
doc_type: project_card
repo: opt-trading
project: opt-trading
module: trading_analytics
go_id:
status: reference
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - project_card
  - trading_analytics
  - continuity
  - product
surface: continuity
source_kind: operational_support
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# PROJECT_CARD_TRADING_ANALYTICS_CHAIN_01

## Role aligne avec la matrice maitre

- role actuel : fiche compacte de reprise pour la chaine analytique trading
- role cible : surface operatoire de reprise produit / pipeline
- cette fiche ne remplace ni la matrice maitre, ni les specs detaillees, ni les closeouts par module

Date: 2026-04-14

## 1. Objet

Figer une fiche compacte de reprise pour la chaîne analytique trading, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche agrège volontairement:
- les artefacts repo déjà présents;
- la continuité validée en séance quand le plan suivi n’existe pas encore comme doc source unique.

Elle ne remplace pas les closings, specs ou rapports détaillés par module.

## 2. But final

Construire une chaîne analytique trading cohérente séparant:
- collecte des données dérivées et marchés;
- calcul et règles de risque;
- analyse explicative et lecture des signaux;
- estimation probabiliste / biais / flags;
- exposition de sorties stables pour consommation par d’autres couches.

L’objectif n’est pas un script isolé, mais un pipeline analytique réutilisable avec contrats suffisamment stables pour alimenter d’autres surfaces opérateur ou moteurs d’aide à la décision.

## 3. Plan validé

1. Séparer clairement collecte, calcul risque, analyse et probabilité au lieu de mélanger ces rôles dans un seul point d’entrée.
2. Stabiliser les payloads machine-readables et les contrats d’interface avant d’élargir le périmètre fonctionnel.
3. Durcir les sémantiques par versions / invariants / tests avant ajout de nouveaux champs ou comportements.
4. Préserver les formats déjà acceptés lorsqu’ils servent d’interface pour les autres briques.
5. Exposer ensuite une lecture plus utile côté opérateur ou consommation aval, sans casser les contrats déjà verrouillés.

## 4. ETABLI

- La vue portefeuille déjà mergée a explicitement retenu une famille analytique trading composée de `risk_engine`, `derivatives_collector`, `derivatives_analyzer` et `probability_engine`, avec une cible commune de séparation collecte / analyse / probabilité / risque.
- `derivatives_collector` existe comme module durable avec:
  - application dédiée;
  - wrappers `cmd` et `sanity_check`;
  - logique adapters;
  - outillage de compat lifecycle.
- Une famille documentaire `COLLECTORS_*` existe déjà dans le repo pour cadrer doctrine, mapping, compat et convergence du volet collecte.
- `probability_engine` existe comme module durable avec application dédiée et wrappers `cmd` / `sanity_check`.
- La logique de continuité retenue sur cette chaîne a déjà privilégié:
  - la séparation des responsabilités;
  - le verrouillage progressif des contrats;
  - les ajouts prudents par version plutôt qu’une expansion non bornée.

## 5. NON ETABLI

- Il n’existe pas encore, dans un seul document compact déjà consolidé avant cette fiche, une vue programme unifiée expliquant bout-en-bout le rôle final de `risk_engine`, `derivatives_collector`, `derivatives_analyzer` et `probability_engine` ensemble.
- Tous les sous-modules de la chaîne n’ont pas été relus ligne par ligne dans cette passe documentaire; cette fiche reste une fiche de continuité, pas un audit code exhaustif.
- La chaîne complète n’est pas encore figée ici comme contrat bout-en-bout unique allant de la collecte brute à la sortie finale consommée par une surface opérateur déterminée.
- La présente fiche ne tranche pas, à elle seule, un nouveau GO d’extension fonctionnelle; elle fige d’abord la compréhension validée de la chaîne.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise chaîne analytique
Par défaut, la reprise logique suivante est:
`GO_TRADING_ANALYTICS_CHAIN_CONTRACT_FREEZE_01`

### Pourquoi
Parce que le manque documentaire le plus structurant n’est plus d’abord l’existence de briques séparées, mais la fixation d’une vue courte et stable de leurs interfaces de chaîne:
- entrée collecte;
- sorties intermédiaires;
- exposition analyse;
- exposition probabilité / biais / flags;
- frontière exacte du risque.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée de la chaîne analytique trading;
- ne modifie aucun runtime;
- n’ajoute aucun champ de payload;
- n’ouvre pas automatiquement un chantier d’implémentation;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `docs/ot/reports/OT_PROJECT_PORTFOLIO_OBJECTIVES_VALIDATED_PLANS_01.md`
- `modules/derivatives_collector/app/derivatives_collector.py`
- `modules/derivatives_collector/scripts/cmd.sh`
- `modules/derivatives_collector/scripts/sanity_check.sh`
- `modules/derivatives_collector/scripts/lifecycle_compat.sh`
- `modules/probability_engine/app/probability_engine.py`
- `modules/probability_engine/scripts/cmd.sh`
- `modules/probability_engine/scripts/sanity_check.sh`
- `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- `docs/COLLECTORS_DERIVATIVES_MAPPING_01.md`
- `docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md`
- `docs/COLLECTORS_LIFECYCLE_COMPAT_CLOSEOUT_01.md`

## 9. ETABLI

- la deuxième `PROJECT_CARD` issue du gel portefeuille est ouverte pour la chaîne analytique trading;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée;
- la lacune documentaire est recentrée sur la fixation des interfaces de chaîne plus que sur l’existence des briques.

## 10. TODO

- produire la fiche équivalente pour Bot Vision / ingestion desk;
- produire ensuite la fiche OpenClaw si l’on veut compléter les trois gros blocs les moins bien résumés.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_TRADING_ANALYTICS_CHAIN_01`

Point de reprise chantier logique:
`GO_TRADING_ANALYTICS_CHAIN_CONTRACT_FREEZE_01`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour la chaîne analytique trading, le prochain manque structurant n’est plus tant la séparation des briques que la fixation courte et stable de leurs interfaces de chaîne.
