---
doc_id: OPT_TRADING_PROJECT_CARD_DESKPRO_01
doc_type: project_card
repo: opt-trading
project: opt-trading
module:
go_id: GO_PROJECT_CARDS_FREEZE_01
status: validated
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - project_card
  - desk_pro
  - continuity
  - multi_machine
search_tags:
  - surface:continuity
  - doc_role:carte
  - product:desk_pro
  - flow:operational_support
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 6. Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/status/desk_pro_stack_canonique.md
---

# PROJECT_CARD_DESKPRO_01

Date: 2026-04-13

## Role documentaire

- role_actuel: fiche compacte de reprise Desk Pro
- role_cible: fiche operatoire compacte non souveraine, lue sous la synthese produit Desk Pro
- souverainete: ne remplace ni la synthese produit canonique, ni les runbooks, ni les closeouts
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et la synthese Desk Pro avant d'utiliser cette fiche pour retrouver la suite locale la plus utile

## 1. Objet

Figer une fiche compacte de reprise pour Desk Pro, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche complète les runbooks, closings et notes de plan déjà présents. Elle ne les remplace pas.

## 2. But final

Faire de Desk Pro une surface opérateur multi-machine cohérente, gouvernée et relâchable, avec:
- des entrypoints clairs selon le rôle opérateur / admin-debug;
- une surface de wrappers maîtrisée;
- des runbooks release cohérents;
- une chaîne d’export et de consultation inter-machines explicite;
- une préparation bornée d’une future consommation ou ingestion côté `db-layer`.

## 3. Plan validé

1. Nettoyer la surface opérateur et les entrypoints réellement exposés.
2. Recaler doctrine, wrappers et documentation pour réduire les divergences entre ce qui est décrit et ce qui est installé.
3. Stabiliser la chaîne de release et ses preuves de rejouabilité.
4. Prouver le flux multi-machine via export vers `/shared` puis consultation/consommation sur les autres machines.
5. Préparer ensuite la couche de consommation enrichie et, si nécessaire plus tard, la future ingestion côté `db-layer`.

## 4. ETABLI

- Une note de plan distingue explicitement:
  - le GO global de sélection;
  - les missions candidates Desk Pro non-Trae;
  - les chantiers DEV `fantome` dérivés.
- La file des missions candidates a été figée:
  - `OT_DESKPRO_ADMIN_WRAPPERS_GOVERNANCE_01`
  - `OT_DESKPRO_RELEASE_OPS_DRILL_01`
  - `OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01`
  - `OT_DESKPRO_INSTALLERS_WRAPPERS_INVENTORY_01`
  - `OT_DESKPRO_RELEASE_REFERENCE_CONSOLIDATION_01`
  - `OT_DESKPRO_DB_LAYER_INGESTION_PREP_AUDIT_01`
- Les docs générales ont déjà été resynchronisées avec la hiérarchie d’entrypoints retenue.
- La consolidation des références release a été traitée.
- Le contrat source minimal pour une future ingestion `db-layer` a été documenté.
- La gouvernance a déjà explicitement distingué:
  - les wrappers globaux canoniques;
  - les wrappers machine-pack `student` / `db-layer` comme exception runtime hors registry canonique.

## 5. NON ETABLI

- Le flux bout-en-bout complet `admin-trading -> /shared -> student/db-layer` n’est pas figé ici comme preuve opérationnelle complète unique.
- La future ingestion `db-layer` n’est pas encore implémentée dans cette fiche; seul le cadrage source minimal est retenu.
- L’ensemble Desk Pro n’est pas encore résumé dans une unique doc programme plus large couvrant à la fois doctrine, release, export et consommation.
- Cette fiche ne remplace pas les preuves runtime machine par machine.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise Desk Pro
Par défaut, la reprise logique suivante reste:
`OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01`

### Pourquoi
Parce que:
- la doctrine et la gouvernance wrappers ont déjà été largement figées;
- la release a déjà eu une passe de clarification / drill;
- le prochain manque de preuve le plus structurant est la démonstration opérationnelle du flux inter-machines.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée du chantier Desk Pro;
- ne modifie aucun runtime;
- n’ouvre aucun drill automatiquement;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `docs/ot/reports/OT_DESKPRO_GO_CANONICAL_PLAN_01.md`
- `docs/ot/reports/OT_PROJECT_PORTFOLIO_OBJECTIVES_VALIDATED_PLANS_01.md`
- `docs/desk_pro_release_ops_runbook.md`
- `docs/desk_pro_release_ops_quick_reference.md`
- `docs/db_layer_desk_pro_runbook.md`
- `docs/ot/closings/OT_DESKPRO_RELEASE_OPS_DRILL_01_CLOSING.txt`
- `docs/ot/closings/OT_DESKPRO_RELEASE_REFERENCES_CONSOLIDATION_01_CLOSING.txt`
- `docs/ot/closings/OT_DESKPRO_DB_LAYER_INGESTION_SOURCE_CONTRACT_01_CLOSING.txt`

## 9. ETABLI

- la première `PROJECT_CARD` issue du gel portefeuille est ouverte pour Desk Pro;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée.

## 10. TODO

- produire la fiche équivalente pour la chaîne analytique trading;
- produire ensuite la fiche Bot Vision / ingestion desk.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_DESKPRO_01`

Point de reprise chantier logique:
`OT_DESKPRO_SHARED_EXPORT_CONSUMPTION_DRILL_01`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour Desk Pro, la prochaine preuve structurante n’est plus principalement doctrinale mais opérationnelle: démontrer le flux inter-machines export -> shared -> consommation.
