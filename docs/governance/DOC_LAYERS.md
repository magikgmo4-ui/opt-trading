---
doc_id: OPT_TRADING_DOC_LAYERS
doc_type: workflow_rule
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - doc_layers
  - governance
  - continuity
  - memory_bricks
search_tags:
  - surface:governance
  - doc_role:regle_stable
  - closeout:reference
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 8. Pipeline local cible"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/REPO_ROLE.md
---

# DOC_LAYERS — opt-trading

## Objet

Ce document fixe les couches documentaires utilisées dans `opt-trading` dans le cadre de la méthode uniforme de continuité.

Il sert à distinguer les fonctions documentaires et à éviter :
- les doublons de source de vérité
- les mélanges entre doc longue, chantier, continuité et compaction
- les dérivations implicites non tracées

Hiérarchie de lecture :
- l'etat reel prouve prime
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne les couches
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` reste une annexe stable secondaire
- ce document explicite l'application locale de ces couches dans `opt-trading`

---

## 1. Vue d’ensemble

Les couches documentaires retenues sont :

- gouvernance
- chantier
- continuité
- compaction
- couche humaine à préciser séparément

Chaque couche a une fonction propre.

---

## 2. Couche gouvernance

### But
Définir les règles stables du repo.

### Contenu type
- rôle du repo
- conventions locales
- règles de dérivation
- règles de structure des documents

### Artefacts typiques
- `REPO_ROLE.md`
- `DOC_LAYERS.md`
- `MEMORY_BRICKS_MAPPING.md`

---

## 3. Couche chantier

### But
Porter un lot de travail borné.

### Structure canonique
- `00_cadrage.md`
- `01_plan.md`
- `02_journal_technique.md`
- `03_decisions.md`
- `90_closeout.md`

### Fonction
- cadrer
- exécuter
- valider
- clore
- reprendre

### Convention locale de nommage futur des GO

Règle locale à retenir pour les futurs GO :

`GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`

Décisions locales :
- `<PRODUCT_OR_SURFACE>` doit provenir d'un produit, d'une famille ou d'une surface deja stabilise(e) par le canon produit ou la carte de surfaces
- `2_INITIAL_PROJECT_DOC` peut servir de source operatoire secondaire si ce token y est deja aligne avec ce canon, mais ne suffit plus comme source souveraine unique
- tous les tokens du GO doivent rester stables, uppercase et séparés par `_`
- `<ROLE>` est un rôle structurel issu d'un vocabulaire canonique contrôlé ; `PARENT` et `CHILD` sont des rôles structurels et ne sont autorisés que si la structure parent / sous-chantier est réelle
- en l'état, le vocabulaire contrôlé explicite déjà canonisé pour les rôles structurels est `PARENT` / `CHILD`; aucune étiquette décorative n'est autorisée à la place
- `<OBJECT>` doit provenir d'un vocabulaire canonique contrôlé ; à défaut de lexique global séparé déjà canonisé, il faut reprendre un token objet déjà stabilisé par la source canonique gouvernante du lot et ne pas inventer de taxonomie excessive
- `<NN>` est obligatoire, placé en suffixe final, comporte au minimum deux chiffres, et sert à éviter les collisions, distinguer les séries ou itérations, permettre une réouverture propre et stabiliser les références documentaires
- aucune campagne rétroactive massive n'est autorisée sans GO dédié

Exemples validés :
- `GO_OPT_DESKPRO_PARENT_AUDIT_01`
- `GO_OPT_DESKPRO_CHILD_ALIGNMENT_01`
- `GO_OPT_TMUX_PARENT_CADRAGE_01`
- `GO_OPT_TMUX_CHILD_RUNTIME_CONTRACT_01`

### Méthode de clôture / canonisation
Lorsqu'un lot est canonisé comme fermé, son nom canonique clos peut être normalisé sous la forme `..._CLOS`.

Cette normalisation sert à :
- distinguer explicitement un lot clos d'un simple cadrage ou d'un lot encore ouvert
- garder une continuité plus lisible entre dossier chantier clos et index fermés

Règle locale :
- la normalisation `..._CLOS` est autorisée au moment de la canonisation fermée
- elle n'impose pas de campagne globale rétroactive sur les anciens GO clos
- elle doit rester bornée aux cas explicitement réalignés

---

## 4. Couche continuité

### But
Rendre visible l’état courant et les suites naturelles.

### Artefacts typiques
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/opportunities/OPPORTUNITY_LOG.md`

### Fonction
- suivi des GO connus
- suivi des flux actifs
- reprise rapide
- visibilité des prochains GO candidats
- conservation des opportunités non encore ouvertes

### Règles locales de lecture pour `docs/index/GO_INDEX.md`
- le `Tableau canonique des chantiers` porte la liste canonique
- la section `Entrées` enrichit un GO déjà canonisé ; elle n’ajoute pas un GO hors tableau
- une surface documentaire non chantier peut être référencée comme support ou source, sans devenir un chantier
- un repère dérivé transverse peut exister comme aide de lecture, mais reste non canonique tant qu’il ne remplace ni la liste ni la priorité ni la reprise

---

## 5. Couche compaction

### But
Fournir une forme compacte, structurée et navigable.

### Artefact principal
- `memory_bricks`

### Règle
La compaction dérive de documents stabilisés.
Elle ne remplace ni les closeouts ni la doc de chantier.

---

## 6. Couche humaine

### Statut actuel
Cette couche est reconnue comme nécessaire, mais son rôle exact n’est pas fixé dans ce document.

### Règle actuelle
La matière humaine et contextuelle doit être relue et stabilisée avant d’alimenter les couches canoniques.

Ce document ne tranche pas encore :
- le lieu exact final de cette matière
- son niveau de duplication autorisé
- son mapping détaillé vers les autres couches

---

## 7. Règles anti-mélange

### 7.1 La gouvernance ne remplace pas le chantier
Un document de gouvernance n’est pas un dossier chantier.

### 7.2 Le chantier ne remplace pas la continuité transverse
Un dossier chantier ne remplace ni un index, ni un `REPRISE.md`, ni un `NEXT_GO_CANDIDATES.md`.

### 7.3 La compaction ne remplace pas le détail
`memory_bricks` ne remplace pas la documentation longue.

### 7.4 La continuité ne remplace pas le closeout
Les index et fichiers de reprise pointent vers les closeouts, ils ne les absorbent pas.

---

## 8. Pipeline local cible

Le pipeline local cible est :

contexte utile / matière stabilisée
-> chantier borné
-> closeout / reprise / next
-> compaction `memory_bricks`

La continuité locale doit rester cohérente avec ce pipeline.

---

## 9. Statut

Statut :
- document de référence locale
- à maintenir cohérent avec la méthode uniforme globale
