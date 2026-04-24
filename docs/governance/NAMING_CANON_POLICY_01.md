---
doc_id: OPT_TRADING_NAMING_CANON_POLICY_01
doc_type: governance_policy
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_NAMING_CANON_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - naming
  - canon
  - normalization
  - governance
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Regle sur <PRODUCT_OR_SURFACE>"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md
---

# NAMING_CANON_POLICY_01

## Objet
Fixer une politique transverse de nommage pour l'avenir, sans concurrencer le canon GO deja publie dans le repo et sans renommer immediatement l'existant.

## Priorite canonique
L'etat reel prouve prime, puis `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
Le canon GO du repo prime sur cette politique.
`docs/governance/MATRICE_GOUVERNANTE_V2.md` peut aider au recroisement, mais reste une annexe stable secondaire.

Canon GO deja publie :

`GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`

Cette politique par surface ne doit jamais redefinir cette regle.

## Principe
L'uniformite ne signifie pas une seule forme pour tout.
L'uniformite retenue ici est une regle stable par surface, strictement subordonnee au canon GO du repo.

## Surfaces et formats retenus

### 1. IDs de gouvernance
Utiliser `UPPER_SNAKE_CASE` pour les `doc_id` et identifiants documentaires hors GO.

Exemples :
- `OPT_TRADING_NAMING_CANON_POLICY_01`
- `SESSION_DOCUMENTATION_GATE`

### 2. Dossiers de modules
Utiliser `lower_snake_case`.

Exemples :
- `naming_normalizer`
- `validated_prompt_factory`
- `ops_menu_hub`

### 3. Scripts et fichiers applicatifs
Utiliser `lower_snake_case`.

Exemples :
- `sanity_check.sh`
- `audit_naming.sh`
- `scanner.py`

### 4. Fichiers ordonnes de chantier
Utiliser `NN_lower_snake_case.ext`.

Exemples :
- `00_cadrage.md`
- `01_plan.md`
- `02_journal_technique.md`
- `03_decisions.md`
- `90_closeout.md`

### 5. Fichier parent de chantier
Utiliser `01_cadrage_parent.md`.

### 6. Fichiers de gouvernance
Utiliser `UPPER_SNAKE_CASE.md` ou `UPPER_SNAKE_CASE_01.md`.

Exemples :
- `REPO_ROOT_POLICY.md`
- `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`

### 7. Branches Git
Utiliser `family/lower-kebab-case`.

Familles autorisees par defaut :
- `feat/`
- `fix/`
- `audit/`
- `inventory/`
- `integ/`
- `doc/`
- `backup/`
- `save/`
- `chore/`

## Granularite GO retenue pour l'outillage
La verification structurelle GO du module et des futurs audits repose sur la granularite suivante :

- `<SCOPE>` = 1 token uppercase
- `<PRODUCT_OR_SURFACE>` = 1 a n tokens uppercase
- `<ROLE>` = token structurel controle
- `<OBJECT>` = 1 a n tokens uppercase
- `<NN>` = suffixe numerique obligatoire sur 2 chiffres minimum

En pratique, les roles controles retenus a ce stade sont :
- `PARENT`
- `CHILD`

Cette granularite sert a verifier la forme structurelle.
Elle ne remplace pas la validation semantique :
- la source canonique de `<PRODUCT_OR_SURFACE>` est un produit, une famille ou une surface deja stabilise(e) par le canon produit ou la carte de surfaces
- `2_INITIAL_PROJECT_DOC` peut rester une source operatoire secondaire si ce token y est deja aligne avec ce canon
- la validite metier de `<OBJECT>` reste gouvernee par le canon documentaire du repo

## Regles de transition
- aucun renommage massif immediat
- audit repo-first
- exceptions explicites
- legacy tolere tant qu'il est inventorie
- application reelle seulement dans un GO dedie

## Invariants
- l'etat reel du repo prime
- la documentation canonique prime sur la reconstruction de session
- le canon GO du repo prime sur la politique par surface
- `GO_INDEX` ne doit etre prepare qu'avec des GO deja realignes
- le module `naming_normalizer` commence et reste ici en mode audit-only

## Regle sur `<PRODUCT_OR_SURFACE>`
Ce document ne canonise aucun nouveau token `<PRODUCT_OR_SURFACE>`.

Si un nouveau token devient necessaire dans un exemple ou une doc, il doit etre marque explicitement comme :

`a canoniser dans le canon produit ou la carte de surfaces avant toute application repo ; 2_INITIAL_PROJECT_DOC peut ensuite etre aligne si utile`

## Anti-cibles
- imposer un renommage global en une passe
- casser l'historique ou la reprise
- melanger canon futur et correction retroactive non qualifiee
- creer un second canon parallele au repo
- traiter un nouveau `<PRODUCT_OR_SURFACE>` comme deja valide par defaut

## REPRISE
- parent : `GO_OPT_TRADING_PARENT_NAMING_CANON_01`
- premier audit : `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01`
- module durable : `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01`
