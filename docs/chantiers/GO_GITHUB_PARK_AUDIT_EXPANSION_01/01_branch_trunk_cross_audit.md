---
doc_id: OPT_TRADING_GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01
doc_type: chantier_report
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01
status: closed
lifecycle_stage: audit
topic_keys:
  - github
  - branches
  - trunks
  - audit
  - cross_read
surface: park
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02B.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02C.md
---

# GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01

## Objet

Croiser les trunks réellement inspectés via ZIP avec les branches visibles via GitHub, afin de distinguer :

- ce qui est déjà absorbé par le trunk
- ce qui reste une branche active utile
- ce qui ressemble à une branche de parking / historique / sauvegarde
- ce qui doit être traité ensuite dans un audit plus fin de familles de modules

---

## Besoin initial

Le parc avait déjà été lu à partir des trunks ZIP et consolidé côté rôles de repo.
Il manquait encore la couche de raccord entre :

- le contenu réellement inspecté
- les branches visibles
- les chantiers déjà absorbés ou encore ouverts

---

## Cible finale

Obtenir une lecture exploitable `trunk ↔ branches` repo par repo, sans prétendre encore faire la consolidation physique des branches ni l’audit complet des familles de modules.

---

## Méthode retenue

Le croisement a été fait à partir de :

1. trunks ZIP réellement inspectés
2. listes de branches visibles via GitHub
3. PR récentes accessibles via GitHub pour rattacher les branches à l’état du trunk

Cette passe ne prétend pas relire toutes les branches commit par commit.
Elle produit un audit de rattachement opératoire.

---

## État établi — par repo

### 1. `opt-trading`

#### Trunk retenu
- trunk inspecté : `sot/mainline`
- trunk dominant du parc

#### Lecture branches ↔ trunk
Les branches visibles se regroupent en grandes familles :

- `docs/*`, `doc/*` : branches documentaires courtes
- `feat/*` : branches de chantiers fonctionnels ou doc/ops bornés
- `integ/*` : branches d’intégration / alignement
- `save/*` : snapshots machine / sauvegarde
- `main` : branche secondaire visible mais non retenue comme continuité canonique

#### Ce qui est établi
- une grande partie des branches récentes documentées par PR ont déjà été **absorbées** dans `sot/mainline`
- le trunk porte déjà les thèmes suivants sous forme absorbée :
  - SimEx
  - OpenClaw docs repo-side
  - Desk Pro doctrine / release / wrappers / docs sync
  - journal GO matrix
  - session documentation gate
  - portfolio / product target docs

#### Branches encore utiles / ouvertes constatées
- `feat/project-card-deskpro-01` : branche encore ouverte, avec PR ouverte, prolonge le trunk documentaire Desk Pro sans le contredire

#### Branche redondante / supersédée constatée
- `feat/workflow-post-change-consolidation-03` : branche encore visible mais désormais **redondante côté continuité**, car la consolidation correspondante a déjà été portée directement sur `sot/mainline`

#### Branches non tranchées dans cette passe
Restent à classer plus finement dans une future passe :
- familles `mimo*`
- familles `memory-bricks-v2*`
- familles `trading-realtime-v1*`
- diverses branches `feat/*` anciennes sans rattachement PR récent lu dans cette passe
- branches `save/*` (à traiter comme snapshots, non comme continuité active)

#### Verdict croisé
- `opt-trading` : **trunk très absorbant ; beaucoup de branches = branches de chantier déjà intégrées ; quelques branches encore ouvertes ; reliquat de branches parking/historique à classifier plus finement**

---

### 2. `localcms`

#### Trunk retenu
- trunk inspecté : `main`

#### Branches visibles
- `main`
- `tools/localcms-dev-host`

#### Ce qui est établi
- le gros de la matière produit a déjà été absorbé dans `main`
- les PR lues montrent que :
  - la mémoire read-only a été mergée dans une feature antérieure
  - le gros merge `LocalCMS v1` a bien atterri sur `main`

#### Lecture de la branche restante
- `tools/localcms-dev-host` ressemble à une branche de tooling / hôte de dev, pas à un second trunk produit concurrent

#### Verdict croisé
- `localcms` : **trunk stable ; divergence faible ; branche restante de type tooling/environnement**

---

### 3. `openclaw`

#### Trunk retenu
- trunk inspecté : `main`

#### Branches visibles
- `main`
- `docs/go-openclaw-sync-02-v1`
- `docs/openclaw-next-go-sequence-v1`
- `docs/kanban-resync-04b`

#### Ce qui est établi
- les branches `docs/go-openclaw-sync-02-v1` et `docs/openclaw-next-go-sequence-v1` ont été absorbées dans `main` via PR mergées
- le trunk `main` joue bien son rôle de repo documentaire/gouvernance dédié

#### Point restant
- `docs/kanban-resync-04b` reste visible, sans preuve de merge lue dans cette passe
- elle doit être traitée comme branche documentaire à vérifier, pas comme second tronc du repo

#### Verdict croisé
- `openclaw` : **trunk documentaire propre ; la plupart des branches visibles sont des branches doc déjà absorbées ; une branche doc résiduelle reste à qualifier**

---

### 4. `hf_trading`

#### Trunk retenu
- trunk inspecté : `main`

#### Branches visibles
- `main` uniquement

#### Verdict croisé
- aucune divergence branches ↔ trunk
- repo simple et non problématique sur ce point

---

### 5. `Llm-wiki-minimal`

#### Trunk retenu
- trunk inspecté : `main`

#### Branches visibles
- `main` uniquement

#### Verdict croisé
- aucune divergence branches ↔ trunk
- lane simple, cohérente, retenue pour la pré-consolidation documentaire

---

### 6. `Llm-wiki`

#### Trunk retenu
- trunk inspecté : `main`

#### Branches visibles
- `main` uniquement

#### Lecture croisée
- aucun problème de branches, mais repo désormais hors parc actif utile
- classé `FREEZE_LEGACY_OBSOLETE`

---

## Synthèse croisée du parc actif utile

### Type A — trunk simple, sans divergence notable
- `hf_trading`
- `Llm-wiki-minimal`

### Type B — trunk stable avec faible divergence tooling/doc
- `localcms`
- `openclaw`

### Type C — trunk absorbant avec historique de nombreuses branches de chantier
- `opt-trading`

### Type D — hors parc actif utile
- `Llm-wiki`
- `Magikgmo`
- `algo_hf`

---

## Ce qui est établi à ce stade

1. Le principal besoin de croisement `branches ↔ trunks` concerne désormais surtout `opt-trading`.
2. `localcms`, `openclaw`, `hf_trading` et `Llm-wiki-minimal` ont une surface de divergence faible ou triviale.
3. `opt-trading` concentre l’essentiel du travail restant de lecture branchée.
4. Une partie des branches visibles d’`opt-trading` n’est plus du travail actif mais de l’historique de chantier absorbé.
5. `feat/workflow-post-change-consolidation-03` est à considérer comme redondante côté continuité tant que la branche n’est pas nettoyée ou fermée.
6. `feat/project-card-deskpro-01` reste un vrai chantier ouvert côté doc.

---

## Limites réelles

Cette passe ne fait pas :

- la revue commit par commit de toutes les branches `opt-trading`
- la lecture exhaustive de toutes les PR historiques
- la classification module par module des branches thématiques `mimo`, `trading-realtime`, `memory-bricks`, etc.

Ces points sont volontairement laissés au GO suivant.

---

## Next GO

### GO retenu
`GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01`

### Pourquoi
Le croisement `branches ↔ trunks` montre que le vrai nœud restant n’est plus la topologie des repos, mais la structure interne d’`opt-trading` :

- familles de modules
- variantes
- modules concurrents
- wrappers / miroirs / outputs
- archives et reliquats

---

## Verdict

**PASS — audit croisé branches ↔ trunks établi à un niveau opératoire suffisant pour descendre au GO suivant**
