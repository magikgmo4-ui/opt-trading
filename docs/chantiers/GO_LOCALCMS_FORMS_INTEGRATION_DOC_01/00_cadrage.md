---
doc_id: GO_LOCALCMS_FORMS_INTEGRATION_DOC_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: localcms
module: forms
go_id: GO_LOCALCMS_FORMS_INTEGRATION_DOC_01
status: cadrage
lifecycle_stage: cadrage
topic_keys:
  - localcms
  - forms
  - integration
  - documentation
  - consumer_ui
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md
  - docs/index/GO_INDEX.md
---

# GO_LOCALCMS_FORMS_INTEGRATION_DOC_01

## Classification
**module durable — cadrage documentation / intégration compatible**

## Rôle recommandé
**Architecte produit + intégrateur UI**

---

## Besoin initial
Prévoir dans `localcms` une future capacité `forms` pour modifier de façon plus souple des contenus globaux ciblés, sans casser ni dupliquer les briques déjà présentes.

---

## Cible finale
Avoir un cadrage doc-only où :

- `localcms` reste **consumer UI**
- `opt-trading` reste **canon / producer**
- `forms` devient une **couche d’édition contrôlée**
- l’édition visée couvre plus tard :
  - documentation générale
  - projet
  - infra
  - config
  - fichiers sélectionnés
  - axes globaux / points structurants
- rien de ce qui existe déjà dans `localcms` ne doit être recréé

---

## État établi retenu

- `localcms` est considéré comme **déjà mergé**
- la base réelle à considérer est **`main`**
- il ne faut pas recréer ce qui couvre déjà :
  - Shared Explorer
  - CMS Installer
  - Memory View / Memory Bricks
- le prochain lot `forms` doit être traité comme **intégration compatible à l’existant**, pas comme nouveau socle parallèle

---

## Intention
Prévoir dans `localcms` une future capacité `forms` pour modifier de façon souple des contenus globaux ciblés, sans casser ni dupliquer les briques déjà présentes.

---

## Périmètre V1 documentaire

- documentation générale
- projet
- infra
- config
- fichiers sélectionnés
- axes globaux / points structurants

---

## Contraintes

- ne pas recréer l’existant
- ne pas introduire une seconde UI concurrente
- rester compatible avec les surfaces déjà mergées dans `localcms`
- conserver `opt-trading` comme source canonique des cibles métier / doc quand applicable
- privilégier une édition bornée, ciblée, réversible

---

## Direction de design

- intégrer `forms` comme **extension** de `localcms`
- prévoir un usage transversal plutôt qu’un module isolé
- séparer explicitement :
  - navigation / exploration
  - inspection
  - installation
  - édition contrôlée via forms

---

## Décision de cadrage
On ne lance **pas** de code maintenant.

La suite correcte est :
1. figer le cadrage documentaire
2. référencer ce cadrage dans l’index
3. plus tard seulement, relire finement l’existant réel de `localcms main`
4. ensuite cadrer les points d’accroche UI/backend réels

---

## ETABLI
- `localcms` est le bon emplacement pour une future UI `forms`
- `localcms` doit être traité comme base déjà mergée
- `forms` doit être intégré à l’existant, pas recréé à côté
- `opt-trading` reste repo canonique pour la documentation et les cibles métier quand applicable

## TODO
- documenter que `localcms main` est la base réelle déjà mergée
- documenter `forms` comme intégration future compatible
- ne lancer aucun scaffold tant que l’existant n’est pas relu finement

## REPRISE
- `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01`

## MEM_CANDIDATE
- `localcms` déjà mergé intégralement
- futur `forms` = intégration compatible à l’existant, pas recréation de briques déjà présentes
