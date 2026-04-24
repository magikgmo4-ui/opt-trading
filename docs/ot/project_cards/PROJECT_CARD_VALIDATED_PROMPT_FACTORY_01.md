---
doc_id: OPT_TRADING_PROJECT_CARD_VALIDATED_PROMPT_FACTORY_01
doc_type: project_card
repo: opt-trading
project: opt-trading
module: validated_prompt_factory
go_id: GO_PROJECT_CARDS_FREEZE_01
status: validated
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - project_card
  - validated_prompt_factory
  - continuity
  - prompts
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
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - modules/validated_prompt_factory/README.md
---

# PROJECT_CARD_VALIDATED_PROMPT_FACTORY_01

Date: 2026-04-14

## Role documentaire

- role_actuel: fiche compacte de reprise pour `validated_prompt_factory`
- role_cible: fiche operatoire compacte non souveraine sur une brique de support IA
- souverainete: ne remplace ni la matrice, ni les audits/closings du module, ni une trajectoire produit transverse
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et la continuite produit utile avant d'utiliser cette fiche pour retrouver le prochain lot d'usage

## 1. Objet

Figer une fiche compacte de reprise pour `validated_prompt_factory`, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche agrège volontairement:
- les artefacts repo déjà présents;
- la continuité validée en séance quand le plan suivi n’existe pas encore comme doc source unique.

Elle ne remplace pas les audits, reports, closings ni rapports d’adoption déjà présents.

## 2. But final

Faire de `validated_prompt_factory` une brique durable qui transforme une matière déjà validée en prompt final exploitable, dans le bon mode d’usage, avec une surface de commande opérable et des garde-fous documentés.

L’objectif retenu n’est pas seulement un générateur de texte, mais une étape de transformation contrôlée entre synthèse validée et prompt final réutilisable.

## 3. Plan validé

1. Partir d’une matière déjà validée plutôt que de générer à partir de zéro.
2. La convertir en prompt final exploitable pour plusieurs modes d’usage.
3. Exposer une surface opérable via wrappers / sanity / commandes de module.
4. Durcir ensuite usage réel, cohérence documentaire et adoption.
5. Traiter les écarts d’environnement ou de structure sans casser le rôle central du module.

## 4. ETABLI

- Le repo contient déjà un audit, des reports et plusieurs closings sur `validated_prompt_factory`.
- Le module est bien présent comme brique durable avec `sanity.sh`.
- Les documents existants couvrent:
  - audit du module;
  - report principal;
  - closing initial;
  - hardening;
  - real use;
  - adoption.
- Un report a déjà retenu que le module est validé structurellement, avec une doc corrigée malgré un contexte d’exécution Windows imparfait.
- La continuité retenue pour cette brique la place comme transformateur de synthèse validée vers prompt final en mode approprié.

## 5. NON ETABLI

- Il n’existait pas encore, avant cette fiche, une project card courte unique résumant finalité + plan validé + reprise du module.
- La place exacte du module dans la chaîne complète humaine/machine restait surtout reconstituée via reports et continuité, plus que figée dans une fiche unique.
- Cette fiche ne remplace pas une validation runtime complète sur tous les environnements shell/Windows/Linux.
- Cette fiche ne tranche pas de nouvelle extension fonctionnelle; elle gèle d’abord la compréhension validée du module.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise `validated_prompt_factory`
Par défaut, la reprise logique suivante est:
`GO_VALIDATED_PROMPT_FACTORY_ADOPTION_FREEZE_01`

### Pourquoi
Parce que:
- la brique est déjà suffisamment cadrée dans son rôle;
- le besoin documentaire restant porte davantage sur son positionnement d’usage et son adoption que sur sa simple existence structurelle;
- une passe de gel d’adoption est plus utile qu’une ouverture artificielle d’un nouveau scope produit.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée de `validated_prompt_factory`;
- ne modifie aucun runtime;
- n’ouvre pas automatiquement un nouveau patch;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `docs/ot/trae/OT_MODULE_01_VALIDATED_PROMPT_FACTORY_AUDIT.md`
- `docs/ot/reports/OT_MODULE_01_VALIDATED_PROMPT_FACTORY_REPORT.md`
- `docs/ot/closings/OT_MODULE_01_VALIDATED_PROMPT_FACTORY_CLOSING.txt`
- `docs/ot/closings/OT_MODULE_02_VALIDATED_PROMPT_FACTORY_HARDENING_CLOSING.txt`
- `docs/ot/closings/OT_MODULE_01_VALIDATED_PROMPT_FACTORY_REAL_USE_CLOSING.txt`
- `docs/ot/closings/OT_MODULE_03_VALIDATED_PROMPT_FACTORY_ADOPTION_CLOSING.txt`
- `modules/validated_prompt_factory/sanity.sh`

## 9. ETABLI

- la cinquième `PROJECT_CARD` issue du gel portefeuille est ouverte pour `validated_prompt_factory`;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée;
- la lacune documentaire est recentrée sur le positionnement d’usage et l’adoption plus que sur la structure même du module.

## 10. TODO

- produire la fiche `module_contextuals_shell`.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_VALIDATED_PROMPT_FACTORY_01`

Point de reprise chantier logique:
`GO_VALIDATED_PROMPT_FACTORY_ADOPTION_FREEZE_01`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour `validated_prompt_factory`, le prochain manque structurant est davantage le gel court de l’adoption et du positionnement d’usage que la structure du module elle-même.
