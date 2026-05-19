---
doc_id: OPT_TRADING_PROJECT_CARD_MODULE_CONTEXTUALS_SHELL_01
doc_type: project_card
repo: opt-trading
project: opt-trading
module: module_contextuals_shell
go_id: GO_PROJECT_CARDS_FREEZE_01
status: validated
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - project_card
  - module_contextuals_shell
  - shell
  - continuity
search_tags:
  - surface:continuity
  - doc_role:carte
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 6. Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - modules/module_contextuals_shell/README.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
---

# PROJECT_CARD_MODULE_CONTEXTUALS_SHELL_01

Date: 2026-04-14

## Role documentaire

- role_actuel: fiche compacte de reprise module / socle shell
- role_cible: fiche operatoire compacte non souveraine pour une brique de support
- souverainete: ne remplace ni la matrice, ni le README module, ni un audit d'adoption complet
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` avant d'utiliser cette fiche pour retrouver le prochain gel utile

## 1. Objet

Figer une fiche compacte de reprise pour `module_contextuals_shell`, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche agrège volontairement:
- les artefacts repo déjà présents;
- la continuité validée en séance quand le plan suivi n’existe pas encore comme doc source unique.

Elle ne remplace pas le README ni les docs techniques du module.

## 2. But final

Faire de `module_contextuals_shell` un socle partagé pour les futurs modules shell, afin de standardiser:
- la déclaration d’actions via fichiers contextuels;
- la lecture robuste de ces fichiers;
- l’affichage de menus dynamiques;
- le routage vers les scripts cibles.

L’objectif retenu n’est pas un module utilisateur final isolé, mais une brique de fondation pour réduire le coût d’intégration et homogénéiser la couche opératoire shell.

## 3. Plan validé

1. Créer un socle générique au lieu de recoder menu / dispatch dans chaque module shell.
2. Passer vers une logique déclarative d’actions via fichiers `.ctx`.
3. Fournir lecture, rendu et routage standardisés.
4. Permettre à un menu global de scanner les contextuals des modules et d’indexer leurs actions.
5. Réduire ensuite la friction d’adoption par les futurs modules shell.

## 4. ETABLI

- Le README du module l’identifie explicitement comme socle partagé pour la gestion des actions contextuelles des modules shell.
- La cible déclarée est `tous les futurs modules shell`.
- Le module standardise déjà:
  - fichiers `.ctx`;
  - lecture robuste;
  - menus dynamiques;
  - routage des actions.
- La structure du module couvre:
  - `lib/`;
  - `contextuals/`;
  - `examples/`;
  - `docs/`.
- Une surface opérable existe déjà via `cmd.sh` et `sanity.sh`.
- Le README explicite déjà une intégration future avec un menu global capable de scanner les `contextuals/` des modules.

## 5. NON ETABLI

- Il n’existait pas encore, avant cette fiche, une project card courte unique résumant finalité + plan validé + reprise du module.
- La feuille d’adoption effective par les autres modules shell reste moins figée que la cible architecturale elle-même.
- Cette fiche ne démontre pas, à elle seule, l’adoption généralisée du socle par l’ensemble des modules shell existants.
- Cette fiche ne remplace pas une validation multi-environnements complète.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise `module_contextuals_shell`
Par défaut, la reprise logique suivante est:
`GO_MODULE_CONTEXTUALS_SHELL_ADOPTION_FREEZE_01`

### Pourquoi
Parce que:
- le rôle architectural du socle est déjà clair;
- le manque restant porte surtout sur le gel court de son adoption par les modules aval;
- une passe documentaire d’adoption est plus utile qu’un élargissement artificiel du scope du socle.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée de `module_contextuals_shell`;
- ne modifie aucun runtime;
- n’ouvre pas automatiquement un nouveau patch;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `modules/module_contextuals_shell/README.md`
- `modules/module_contextuals_shell/cmd.sh`
- `modules/module_contextuals_shell/sanity.sh`
- `modules/module_contextuals_shell/lib/discovery.sh`
- `modules/module_contextuals_shell/examples/example.ctx`

## 9. ETABLI

- la sixième `PROJECT_CARD` issue du gel portefeuille est ouverte pour `module_contextuals_shell`;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée;
- la lacune documentaire est recentrée sur l’adoption effective du socle plus que sur sa définition architecturale.

## 10. TODO

- aucune autre fiche prioritaire immédiate imposée dans cette série courte.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_MODULE_CONTEXTUALS_SHELL_01`

Point de reprise chantier logique:
`GO_MODULE_CONTEXTUALS_SHELL_ADOPTION_FREEZE_01`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour `module_contextuals_shell`, le prochain manque structurant est surtout la fixation courte de son adoption par les modules futurs / aval.
