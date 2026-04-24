---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_RECLASS_PRIORITY
doc_type: chantier_priorisation
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - reclassement
  - priorisation
  - risque
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/92_plan_classement_optimal.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
---

# Priorisation des reclassements

## Objet
Traduire l'arbre de dependances et le plan de classement en priorites d'action, du plus sur au plus risqué.

## Lecture
- `SAFE` = doc-only ou hygiene faible risque, compatible avec les dependances verifiees
- `VERIFY` = necessite une verification ciblee avant tout move ou reclassement plus fort
- `FREEZE` = ne pas toucher structurellement a ce stade

## SAFE

### SAFE-01 — realigner la carte canonique top-level sur l'etat reel
- cible : `docs/architecture/REPO_SURFACES_MAP.md`
- action : corriger les surfaces qui ne correspondent plus a la racine reelle
- point explicite : `infra_context_sanitized/` est mentionne dans la carte mais absent du top-level observe au `2026-04-24`
- preuve attendue : comparaison entre la carte et `Get-ChildItem -Force -Directory`
- risque : faible, doc-only

### SAFE-02 — expliciter les exceptions racine legitimes
- cibles : `docs/governance/REPO_ROOT_POLICY.md`, eventuellement `README.md`
- action : figer clairement la racine minimale autorisee
- contenu minimal : `README.md`, `requirements.txt`, `.env.example`, `webhook_server.py`, `bitget_bridge.py`
- preuve attendue : coherence entre `REPO_ROOT_POLICY`, le plan de classement et le top-level reel
- risque : faible, doc-only

### SAFE-03 — geler la regle "pas de nouveau support a la racine"
- cibles : `REPO_ROOT_POLICY.md` et references chantier
- action : rappeler que toute nouvelle doc, pack legacy, export, preuve ou helper doit aller dans une surface specialisee
- preuve attendue : regle explicite et non ambiguë
- risque : faible, doc-only

### SAFE-04 — borner clairement les surfaces local-only
- cibles : `docs/architecture/REPO_SURFACES_MAP.md` et/ou `REPO_ROOT_POLICY.md`
- action : rappeler que `_archive/`, `tmp/`, caches, `.secrets/` ne sont ni prerequis de lecture ni sources de verite
- preuve attendue : doctrine documentaire alignee
- risque : faible, doc-only

## VERIFY

### VERIFY-01 — confirmer le statut final de `bitget_bridge.py`
- cible : `bitget_bridge.py`
- question : shim racine durable, ou simple compat legacy deplacable plus tard
- verification requise : references repo, usages operatoires reels, wrappers/eventuels appels externes
- risque : moyen a eleve si move physique premature

### VERIFY-02 — confirmer la place top-level de `packages/`
- cible : `packages/`
- question : surface durable repo-first ou simple support interne a un sous-systeme
- verification requise : consumers reels, rythme d'usage, besoin de visibilite top-level
- risque : moyen

### VERIFY-03 — confirmer la strategie top-level de `tests/`
- cible : `tests/`
- question : renforcer une vraie surface de test top-level, ou assumer une verification distribuee par modules/scripts
- verification requise : tests reels hors top-level, conventions de lancement, impacts sur la lecture canonique
- risque : moyen

### VERIFY-04 — durcir la frontiere `student/` / `data/` / `audit/`
- cibles : `student/`, `data/`, `audit/`
- question : que garde-t-on comme surface machine, comme sortie metier, et comme preuve
- verification requise : types d'artefacts reellement presents et logique d'usage
- risque : moyen

### VERIFY-05 — separer plus finement `scripts/` et `tools/` si necessaire
- cibles : `scripts/`, `tools/`
- question : wrappers structurants versus aides contextuelles
- verification requise : entrypoints canoniques, scripts historiques, scripts de verif, utilitaires ponctuels
- risque : moyen

### VERIFY-06 — taxonomie interne de `modules/`
- cible : `modules/`
- question : faut-il figer une lecture interne plus forte par familles metier / execution / registry / machine
- verification requise : besoin reel de pilotage, pas seulement desir de rangement
- risque : moyen si fait sans lot dedie

## FREEZE

### FREEZE-01 — ne pas fusionner `docs/`, `registry/`, `workflow_ai/`
- raison : trois couches distinctes et complementaires
- risque de move : confusion entre gouvernance, registre declaratif et methode

### FREEZE-02 — ne pas absorber `deploy_module_multi_machine/` dans `scripts/`
- raison : sous-systeme autonome, avec doc, logique et dependances propres
- risque de move : perte de lisibilite systeme

### FREEZE-03 — ne pas basculer `student/` dans `data/`
- raison : `student/` est une surface machine avec scripts, docs et exports
- risque de move : perte de frontiere entre machine et sous-produits

### FREEZE-04 — ne pas deplacer `tradingview/` dans `docs/`
- raison : bord d'integration technique, pas support documentaire
- risque de move : confusion entre contrat technique et documentation

### FREEZE-05 — ne pas promouvoir `_archive/`, `tmp/`, caches ou `.secrets/`
- raison : surfaces locales ou d'archive uniquement
- risque de move : pollution du canon et de la lecture repo-first

## Ordre recommande
1. `SAFE-01` a `SAFE-04`
2. `VERIFY-01` a `VERIFY-04`
3. `VERIFY-05` et `VERIFY-06` seulement si un lot enfant devient utile
4. garder les points `FREEZE` comme garde-fous constants

## Point de reprise
Traiter les points `SAFE` en premier. Les points `VERIFY` n'autorisent aucun move physique avant preuve ciblee.
