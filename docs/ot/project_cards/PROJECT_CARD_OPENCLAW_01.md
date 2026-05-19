---
doc_id: OPT_TRADING_PROJECT_CARD_OPENCLAW_01
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
  - openclaw
  - continuity
  - cockpit
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
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
---

# PROJECT_CARD_OPENCLAW_01

Date: 2026-04-14

## Role documentaire

- role_actuel: fiche compacte de reprise OpenClaw
- role_cible: fiche operatoire compacte non souveraine sur une surface locale de support
- souverainete: ne remplace ni la continuite produit globale, ni les frontieres repo, ni les preuves runtime fines
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et `PRODUCT_CONTINUITY_HIERARCHY_01` avant d'utiliser cette fiche pour retrouver le prochain cadrage local utile

## 1. Objet

Figer une fiche compacte de reprise pour OpenClaw, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche agrège volontairement:
- les artefacts repo déjà présents;
- la continuité validée en séance quand le plan suivi n’existe pas encore comme doc source unique.

Elle ne remplace pas les docs module par module ni les notes d’évidence déjà existantes.

## 2. But final

Fixer OpenClaw, dans `opt-trading`, comme un cockpit opérateur local sur `db-layer`, centré sur:
- l’installation;
- la configuration;
- la gateway locale;
- le diagnostic;
- l’export de preuves;
- la policy provider/model.

L’objectif retenu n’est pas une plateforme multi-machine généralisée ni un serving exposé, mais une chaîne opérateur locale bornée et diagnostiquable.

## 3. Plan validé

1. Documenter le périmètre réel OpenClaw au lieu d’extrapoler un produit plus large.
2. Outiller proprement le poste opérateur local sur `db-layer`.
3. Stabiliser la chaîne install -> config -> gateway -> doctor -> evidence -> policy.
4. Garder explicites les frontières de non-périmètre.
5. N’ouvrir un chantier plus large que sur besoin opératoire réel et vérifiable.

## 4. ETABLI

- Une doc dédiée a déjà fixé le projet cible réel OpenClaw dans `opt-trading`.
- Le projet cible réel retenu est un cockpit opérateur local sur `db-layer`.
- La chaîne documentée est: install -> config -> gateway -> configure -> doctor -> evidence -> policy.
- Les usages utiles prouvés couvrent:
  - `menu_openclaw` comme hub de reprise;
  - lecture policy provider/model;
  - validation de config;
  - diagnostic runtime;
  - pilotage de gateway locale via `tmux`;
  - export de preuves documentaires.
- Les frontières de non-périmètre sont déjà explicites:
  - pas de serving exposé;
  - pas de cloud GPU actif;
  - pas de bridge généralisé au-delà du cas borné;
  - pas de runtime multi-machine hors `db-layer`;
  - pas de mutation automatique de config live;
  - pas de migration runtime déjà décidée vers le repo dédié `openclaw`.

## 5. NON ETABLI

- Il n’existait pas encore, avant cette fiche, une project card courte unique résumant finalité + plan validé + reprise OpenClaw.
- Une feuille de route compacte de niveaux de maturité futurs reste encore moins figée que le périmètre actuel lui-même.
- Cette fiche ne démontre pas un nouveau bridge généralisé ni une orchestration automatique multi-modules.
- Cette fiche ne remplace pas un audit runtime machine complet sur `db-layer`.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise OpenClaw
Par défaut, la reprise logique suivante reste:
`GO_OPENCLAW_STATE_DIR_READ_09`

### Pourquoi
Parce que:
- le périmètre réel a déjà été borné;
- le prochain travail utile reste un raffinement documentaire / diagnostique prudent, sans réouvrir artificiellement un produit plus large;
- la position repo actuelle recommande de conserver la borne documentaire tant qu’un besoin opératoire réel ne justifie pas un case suivant.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée d’OpenClaw dans `opt-trading`;
- ne modifie aucun runtime;
- n’ouvre pas automatiquement un nouveau bridge case;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md`
- `modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md`
- `modules/menu_openclaw/docs/README.md`
- `modules/menu_openclaw/docs/RUNBOOK.txt`

## 9. ETABLI

- la quatrième `PROJECT_CARD` issue du gel portefeuille est ouverte pour OpenClaw;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée;
- la lacune documentaire est recentrée sur la feuille de route de maturité plus que sur la définition du périmètre réel.

## 10. TODO

- produire la fiche équivalente pour `validated_prompt_factory`;
- produire ensuite la fiche `module_contextuals_shell`.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_OPENCLAW_01`

Point de reprise chantier logique:
`GO_OPENCLAW_STATE_DIR_READ_09`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour OpenClaw, la force actuelle du repo est la bonne borne du périmètre réel; la lacune restante est surtout la feuille de route compacte de maturité, pas la définition du projet cible.
