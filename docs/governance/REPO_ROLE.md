---
doc_id: OPT_TRADING_REPO_ROLE
doc_type: repo_role
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - repo_role
  - governance
  - execution
  - memory_bricks
surface: repo
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 1. Role principal"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/DOC_LAYERS.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/index/REPRISE.md
  - docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
---

# REPO_ROLE — opt-trading

## Objet

Ce document fixe le rôle réel de `opt-trading` dans la méthode uniforme de continuité.

Il sert à éviter :
- les confusions de responsabilité entre repos
- les dérives documentaires
- les conflits de source de vérité
- les réouvertures de chantier mal cadrées

Hiérarchie d'autorité locale :
- l'état réel prouvé du repo prime
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne le rôle du repo dans la lecture produit / parent / GO / Git
- ce document explicite seulement le rôle local de `opt-trading` dans ce cadre

---

## 1. Rôle principal

`opt-trading` est le **repo canonique principal** du périmètre.

Il est la référence dominante pour :

- l’exécution réelle
- la structure des modules durables
- les wrappers opératoires
- les closeouts techniques liés à l’exécution
- les points de reprise liés à l’état réel du repo
- la compaction structurée via `memory_bricks`

---

## 2. Responsabilités dominantes

### 2.1 Exécution réelle
`opt-trading` porte le code, les scripts et les artefacts directement liés à l’exécution réelle des composants du périmètre.

Cela inclut notamment :
- modules durables
- scripts opératoires
- wrappers de type `cmd.sh`, `menu.sh`, `sanity_check.sh`
- artefacts de validation locale liés aux modules
- closeouts techniques liés au repo

### 2.2 Canon structurel des modules
`opt-trading` porte le modèle de structure des modules durables.

Ce rôle implique que les conventions de structure observées ou validées ici servent de référence pour les chantiers similaires quand cela est pertinent.

### 2.3 Compaction structurée
`opt-trading` est le repo porteur canonique de `memory_bricks`.

À ce titre :
- il porte la source operative de la compaction structurée
- il définit le point d’ancrage principal des formes compactes de reprise
- il ne doit pas être contredit par une seconde source compacte concurrente dans un autre repo

### 2.4 Continuité locale
`opt-trading` doit porter sa propre continuité locale :
- index de GO du repo si utile
- reprise locale
- next candidates locaux
- opportunity log local
- dossiers chantier au format canonique retenu

---

## 3. Ce que `opt-trading` n’est pas

`opt-trading` n’est pas, à lui seul :

- le repo maître de gouvernance transverse
- le repo consumer principal de lecture/UI
- le sas documentaire de pré-consolidation
- la seule couche documentaire du système entier

Ces fonctions existent ailleurs dans le périmètre.

---

## 4. Relations avec les autres repos

### 4.1 Relation avec `openclaw`
`openclaw` porte la gouvernance transverse :
- workflow
- statuts
- séquence GO
- garde-fous

`opt-trading` ne doit pas absorber silencieusement cette fonction transverse.

### 4.2 Relation avec `localcms`
`localcms` est un repo produit / consumer humain.

Il peut consommer des formes compactes ou structurées provenant de `opt-trading`, notamment autour de `memory_bricks`, mais il ne devient pas la source canonique de l’exécution ni de la compaction maîtresse.

### 4.3 Relation avec `llm_wiki_minimal`
`llm_wiki_minimal` agit comme couche de pré-consolidation.

Il peut condenser ou préparer des candidats de promotion issus du périmètre, mais il ne remplace pas les sources canoniques de `opt-trading`.

---

## 5. Sources dominantes portées par `opt-trading`

Dans la méthode uniforme, `opt-trading` est la source dominante pour :

- l’exécution réelle
- la structure des modules durables
- la compaction structurée via `memory_bricks`
- les closeouts techniques de ses propres chantiers
- les points de reprise liés à l’état réel du repo

---

## 6. Règles locales

### 6.1 Réalité avant mémoire
L’état réel du repo, de la branche et des artefacts prime sur la mémoire reconstruite et sur les hypothèses.

### 6.2 Git prioritaire pour le durable
Tout patch ou module durable doit être traité en priorité via Git.

Les bundles de transfert ne remplacent pas le chemin Git canonique pour la continuité durable.

### 6.3 Chantiers bornés
Les chantiers structurés dans `opt-trading` doivent suivre le format canonique retenu :
- cadrage
- plan
- journal technique
- décisions
- closeout

### 6.4 Dérivation explicite vers `memory_bricks`
Les formes compactes ne doivent pas être écrites comme une seconde narration libre.

Elles doivent dériver de documents stabilisés.

---

## 7. Conséquences pratiques

Quand un chantier concerne `opt-trading`, le repo doit porter au minimum :

- le dossier chantier correspondant si le travail est structuré
- la continuité locale utile
- le closeout technique
- le point de reprise
- les éléments nécessaires à une dérivation propre vers `memory_bricks` si pertinent

---

## 8. Limites

Ce document ne fixe pas encore :
- le rôle exact final de `journal.md`
- le mapping détaillé champ par champ vers `memory_bricks`
- les templates détaillés de chaque type documentaire local
- la liste exhaustive d’objets autorisés à la racine (portée dans `REPO_ROOT_POLICY.md`)

Ces éléments sont traités dans des documents dédiés.

---

## 9. Statut

Statut :
- document de référence locale
- à maintenir cohérent avec la méthode uniforme globale
