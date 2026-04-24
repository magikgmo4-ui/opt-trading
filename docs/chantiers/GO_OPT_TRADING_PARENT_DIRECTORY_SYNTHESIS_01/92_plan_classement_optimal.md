---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_CLASSIFICATION_PLAN
doc_type: chantier_classification_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - classement
  - structure
  - repo
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/ARCHITECTURE.md
  - registry/README.md
  - workflow_ai/WORKFLOW.md
---

# Plan de classement optimal

## Objectif
Definir un classement cible stable du repo, aligne sur les dependances verifiees, sans lancer de refactor physique large qui casserait les references existantes.

## Principe directeur
Le classement optimal n'est pas "tout regrouper". Le bon critere est :
- upstream canonique distinct
- runtime durable distinct
- etat et sous-produits distincts
- local, archive et cache explicitement subordonnes

## Regles de placement
1. aucune nouvelle documentation de support ne remonte a la racine
2. aucun cache, temporaire, export machine ou preuve ponctuelle ne remonte dans `docs/`
3. aucune source fonctionnelle durable ne va dans `scripts/` ou `tools/`
4. `registry/` reste declaratif; il ne prouve pas le live
5. `workflow_ai/` reste methodologique; il ne remplace pas `docs/`
6. `state/` et `data/` restent downstream; ils ne doivent pas piloter les decisions canoniques

## Classement cible

### 1. Racine minimale
Contenu legitime :
- `README.md`
- `requirements.txt`
- `.env.example`
- `webhook_server.py`
- `bitget_bridge.py` tant qu'un retrait n'est pas prouve sans casse

Regle :
- la racine ne garde que le bootstrap humain, les prerequisites repo et les entrypoints runtime historiques vraiment justifies
- tout nouveau support doit etre reclassé sous une surface specialisee

### 2. Canon humain souverain
Surface :
- `docs/`

Sous-centres :
- `docs/governance/`
- `docs/index/`
- `docs/architecture/`
- `docs/master_pack/`
- `docs/chantiers/`

Regle :
- tout ce qui tranche la lecture, la methode de continuite, les decisions de structure ou les points de reprise va ici

### 3. Canon declaratif machine-readable
Surface :
- `registry/`

Regle :
- y placer seulement les inventaires structurels versionnes, pas les preuves runtime ni les explications longues

### 4. Doctrine d'execution
Surface :
- `workflow_ai/`

Regle :
- y placer gates, templates, prompts institutionnels et methode d'execution
- ne pas y dupliquer la gouvernance repo deja fixee dans `docs/`

### 5. Runtime durable
Surfaces :
- `modules/`
- `shared/`
- `adapters/`
- `schemas/`
- `perf/`
- `packages/`

Regle :
- toute logique executable durable, librairie partagee, contrat runtime et persistance applicative va ici

Sous-regles :
- `modules/` = coeur fonctionnel
- `shared/` = briques transverses legeres
- `adapters/` = ponts explicites entre modeles / protocoles
- `schemas/` = contrats machine lisibles
- `perf/` = sous-systeme applicatif autonome avec sa persistance
- `packages/` = code mutualisable empaquetable, pas documentation

### 6. Ops, wrappers et deploiement
Surfaces :
- `scripts/`
- `tools/`
- `deploy_module_multi_machine/`

Regle :
- `scripts/` contient l'execution operatoire, verification, installation et wrappers
- `tools/` contient les utilitaires ponctuels ou bridges operateur/developpeur
- `deploy_module_multi_machine/` reste un sous-systeme de deploiement distinct, car il depend a la fois du registry, des modules sources et du contexte multi-machine

### 7. Integration, etat, produits et preuves
Surfaces :
- `tradingview/`
- `state/`
- `data/`
- `student/`
- `contracts/`
- `audit/`
- `tests/`

Regle :
- `tradingview/` reste au bord d'entree / compatibilite protocolaire
- `state/` garde les checkpoints et configurations runtime legeres
- `data/` garde les sorties et artefacts metier
- `student/` reste une surface machine distincte, pas un simple sous-dossier de donnees
- `contracts/` garde les contrats specialises hors `schemas/` quand ils sont documentaires/metier
- `audit/` garde les preuves ponctuelles et packs d'audit
- `tests/` garde les tests repo-first si une vraie surface de test top-level se renforce

### 8. Archive et local-only
Surfaces :
- `_archive/`
- `tmp/`
- `__pycache__/`
- `.ruff_cache/`
- `.uv-cache/`
- `.uv-python/`
- `.secrets/`

Regle :
- aucune de ces surfaces ne doit etre citee comme source de verite ou prerequis de lecture

## Plan d'action recommande

### Phase 1. Stabilisation documentaire
- retenir officiellement ce classement comme reference de lecture
- garder `docs/architecture/REPO_SURFACES_MAP.md` et le present chantier alignes
- expliciter dans les docs les exceptions racine (`webhook_server.py`, `bitget_bridge.py`)

### Phase 2. Hygiene sans casse
- toute nouvelle doc support -> `docs/`
- toute nouvelle logique durable -> `modules/`, `shared/`, `adapters/`, `schemas/`, `perf/` ou `packages/`
- tout nouveau wrapper ou script d'exploitation -> `scripts/`
- tout nouvel outil ponctuel -> `tools/`
- toute nouvelle preuve ou export -> `audit/`, `data/` ou `student/` selon le cas

### Phase 3. Enfants cibles seulement si besoin
- enfant `modules/` si une taxonomie interne metier doit etre figee
- enfant `scripts/` si on veut separer wrappers canoniques et aides contextuelles
- enfant `data/` et `student/` si la frontiere entre sorties metier, exports machine et preuves doit etre durcie

## Reclassements non recommandes a ce stade
- ne pas fusionner `docs/`, `workflow_ai/` et `registry/` : ils sont complementaires mais non equivalants
- ne pas rentrer `deploy_module_multi_machine/` dans `scripts/` : il a une densite systeme et documentaire propre
- ne pas basculer `student/` dans `data/` : c'est une surface machine, pas un simple bucket
- ne pas absorber `audit/` dans `docs/` : une preuve ponctuelle n'est pas une source canonique
- ne pas deplacer `tradingview/` dans `docs/` : la compatibilite d'entree reste une surface technique

## Arbitrages restants
- `bitget_bridge.py` : garder en racine tant qu'un retrait ou move n'est pas prouve sans rupture d'usage
- `tests/` : confirmer plus tard si la surface doit monter en puissance au top-level ou rester diffusee
- `packages/` : surveiller si le dossier reste bien limite au code mutualisable

## Point de reprise
Avant tout nouveau reclassement physique, verifier d'abord si la cible appartient a la bonne classe dans ce plan. Si oui, le move est justifie; sinon, preferer une clarification documentaire.
