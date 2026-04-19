---
doc_id: OPT_TRADING_GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01
doc_type: governance
repo: opt-trading
project: opt-trading
module:
go_id: GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01
status: reference
lifecycle_stage: governance
topic_keys:
  - git
  - branches
  - housekeeping
  - convergence
  - skill
surface: governance
source_kind: canonical
updated_at: 2026-04-17
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md
  - docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md
---

# GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01

## Objet

Cette fiche fige la méthode canonique de ménage des branches Git pour `opt-trading`.

Elle sert à :
- classer les branches en `DELETE_NOW`, `KEEP`, `REVIEW`
- empêcher les suppressions aveugles
- rattacher le ménage Git à l’état réel du repo et à la doc canonique
- préparer, plus tard si utile, une extraction en Skill sans dépendre d’une session

---

## Base canonique

- repo canonique : `opt-trading`
- branche canonique de continuité : `sot/mainline`
- base de comparaison opératoire : `origin/sot/mainline`
- l’état réel du repo prime sur la mémoire et les hypothèses
- la doc canonique du repo prime sur la logique reconstruite en session

---

## Précondition de méthode

Le ménage des branches commence toujours par un audit, jamais par une suppression immédiate.

Ordre minimal :
1. fetch + prune
2. liste des branches mergées dans `origin/sot/mainline`
3. recroisement doc canonique / statut chantier / utilité de reprise
4. classement `DELETE_NOW / KEEP / REVIEW`
5. suppression seulement du lot `DELETE_NOW`
6. journalisation des suppressions réelles

---

## Entrées minimales

- liste des branches locales et distantes
- résultat `--merged origin/sot/mainline`
- éventuels commits uniques hors canon
- références canoniques utiles :
  - `docs/index/GO_INDEX.md`
  - `docs/index/REPRISE.md`
  - dossier chantier concerné
  - closeout si présent

---

## Règle de suppression

Une branche n’est supprimable que si les 3 conditions suivantes sont vraies :

1. elle est déjà absorbée dans `origin/sot/mainline`
2. elle n’est plus un chantier actif, un GO ouvert, ni un point de reprise
3. elle n’a plus de valeur documentaire, historique opératoire, ni de trace FAIL utile

Si un doute subsiste, la branche sort en `REVIEW`, jamais en `DELETE_NOW`.

---

## Sorties canoniques

### DELETE_NOW
Branche déjà absorbée, non active, non utile à la reprise, et sans valeur documentaire résiduelle.

### KEEP
Branche explicitement conservée car :
- active
- non terminée
- liée à une PR ouverte
- encore utile comme reprise
- encore utile comme preuve ou historique opératoire

### REVIEW
Branche techniquement mergée mais qui exige une revue humaine avant suppression.

---

## Familles à revue manuelle obligatoire

Ne jamais supprimer automatiquement sans revue explicite :

- `audit/*`
- `inventory/*`
- `integ/*`
- `save/*`
- branches nommées autour d’un `GO_*`
- toute branche encore citée dans `GO_INDEX`, `REPRISE` ou un dossier chantier vivant

---

## Traitement des FAIL

Une branche FAIL peut être supprimée seulement si :
- le FAIL est déjà ancré dans la doc canonique
- aucune reprise n’est attendue sur cette branche
- aucun commit utile n’existe encore hors `origin/sot/mainline`

Sinon : `KEEP` ou `REVIEW`.

---

## Procédure opératoire minimale

### 1. Audit Git
- `git fetch origin --prune`
- lister les branches distantes mergées dans `origin/sot/mainline`
- exclure les branches protégées et le tronc canonique

### 2. Contrôle chantier
Pour chaque candidate :
- vérifier l’existence d’un écart réel hors canon
- vérifier son statut dans la doc canonique
- vérifier son utilité de reprise ou de preuve

### 3. Décision
Produire obligatoirement, branche par branche :
- nom
- statut Git réel
- statut chantier
- décision (`DELETE_NOW` / `KEEP` / `REVIEW`)
- justification compacte

### 4. Suppression
Supprimer seulement le lot `DELETE_NOW` validé.

### 5. Journalisation
Tracer les suppressions réelles dans le support adapté au chantier ou au journal utile, sans créer de canon parallèle.

---

## Boundary doc / Skill

Ordre canonique retenu :

1. doc canonique
2. méthode validée
3. extraction éventuelle en Skill

Une Skill future peut :
- collecter les branches
- proposer la classification
- préparer des commandes Git
- produire une synthèse prête à valider

Une Skill future ne doit pas :
- redéfinir la règle hors repo
- inventer des critères non documentés
- supprimer des branches sensibles sans passer par la revue manuelle prévue ici

---

## Format de sortie attendu

| branche | merge canonique | statut chantier | décision | justification |
| --- | --- | --- | --- | --- |
| `nom` | oui/non | active/pass/open/fail/reference/inconnu | `DELETE_NOW` / `KEEP` / `REVIEW` | raison compacte |

---

## Next step type

Quand la méthode est déjà figée, la session suivante ne doit plus redéfinir la règle.

Le travail suivant porte seulement sur :
- l’audit réel du repo
- le classement des branches réelles
- l’exécution contrôlée du lot `DELETE_NOW`
- ou l’extraction en Skill si ce besoin devient stable et récurrent
