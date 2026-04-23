---
doc_id: OPT_TRADING_MATRICE_GOUVERNANTE_V2
doc_type: governance_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - governance
  - continuity
  - git
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Role documentaire"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/GO_CLOSED_INDEX.md
  - matrice_gouvernante_bundle_v1/matrice_gouvernante_bundle_v1/06_MATRICE_GOUVERNANTE_V2_SQUELETTE.md
---

# MATRICE_GOUVERNANTE_V2

## Objet

Fixer la matrice gouvernante V2 comme annexe stable secondaire de gouvernance pour `opt-trading`.

Elle reste une surface canonique importante du corpus stable.
Depuis la publication de `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, elle n'est plus la surface maitresse souveraine transverse.

---

## Role documentaire

- `role_actuel` : annexe stable de gouvernance
- `role_cible` : socle structurel secondaire relu sous la matrice maitre
- `souverainete` : non souveraine face a `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `lecture_de_reprise` : lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis revenir ici pour le detail structurel historiquement promu

---

## 1. Cible

Produire une surface gouvernante unique, transmissible sans memoire de session, qui ordonne :
- la continuite produit
- les flux parent / sous-GO
- le support Git
- l'ouverture / fermeture / propagation
- le placement / l'indexation minimale

Cette matrice gouverne la structure.
Elle ne remplace ni l'etat reel du repo, ni les index operatoires, ni les annexes derivees.

---

## 2. Hierarchie d'autorite

Ordre canonique :
1. etat reel local prouve
2. gouvernance canonique
3. continuite active
4. cartes / navigation / registry
5. chantiers locaux

Effets de lecture :
- une regle ne monte dans la matrice que si elle reste compatible avec les niveaux superieurs
- un support inferieur peut illustrer, prouver, ou contextualiser, sans contredire un niveau superieur
- `docs/index/GO_INDEX.md` est la verite de liste canonique
- `docs/index/REPRISE.md` n'est pas une seconde verite de liste
- `docs/index/BRANCH_STATE.md` gouverne la surface branches seulement

Regles de non-concurrence :
- aucune structure parallele ne concurrence `GO_INDEX.md` pour la liste
- aucune surface Git ne gouverne seule la structure documentaire
- aucun support derive ne remplace la couche produit

---

## 3. Continuite produit

Principe directeur :
- produit d'abord

La couche produit est situee au-dessus :
- du parent chantier
- du GO local
- de la branche

La matrice doit rendre visible :
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`
- `plan_macro_valide`
- `jalons_clos`
- `etat_global_courant`
- `gap_global_restant`
- `suite_logique`

Regles :
- un GO local se lit comme un moyen, jamais comme une finalite autonome
- un parent chantier se lit comme un flux structure au service d'une trajectoire produit
- un support Git se lit comme un moyen d'isolement ou de continuite, jamais comme l'objet gouvernant
- la fermeture d'un chantier doit propager son effet vers la continuite produit

La couche produit ne tranche pas a elle seule :
- le support Git exact
- l'existence d'un parent
- le besoin d'une branche enfant

---

## 4. Parent / sous-GO / support Git

### 4.1 Parent et GO simple

Un parent n'existe dans la matrice que s'il est prouve.

Regles :
- si un parent est explicitement etabli dans le repo, il gouverne le flux
- si aucun parent n'est prouve, le GO est traite comme GO simple
- aucun parent ne doit etre suppose pour completer artificiellement une structure

Effet documentaire :
- `GO_INDEX.md` porte la verite de liste des parents, GO simples et sous-entrees retenues
- `NEXT_GO_CANDIDATES.md` porte la surface next par parent actif

### 4.2 Sous-GO

Un sous-GO n'existe dans la matrice que s'il est prouve.

Regles :
- un sous-GO herite du flux du parent
- un sous-GO sert un objectif local borne
- un sous-GO ne remplace pas le parent
- la fermeture d'un sous-GO ne ferme pas implicitement le parent

### 4.3 Doctrine Git

La branche est le support Git du flux, pas la finalite documentaire.

Regles retenues :
- parent doc-only borne : `sot/mainline` par defaut
- parent d'implementation, multi-machine, ou a isolement structurant : branche dediee possible
- sous-GO : support Git du parent par defaut
- branche enfant : seulement en exception motivee

Cas recevables pour une branche enfant :
- isolement technique fort
- revue separee
- travail parallele reel
- stabilisation locale sans polluer le support du parent
- besoin temporaire lie a une machine ou a une surface distincte

Interdits :
- pas de doctrine `1 GO = 1 branche`
- pas de branche decorative
- pas de parent invente pour justifier une branche
- pas de support Git eleve au-dessus du flux parent

### 4.4 Role du GO local

Le GO local sert a :
- ouvrir un lot borne
- executer un besoin local
- produire une preuve locale
- fermer proprement un sous-ensemble de travail

Le GO local ne sert pas a :
- redefinir seul la trajectoire produit
- porter la verite de liste a la place de `GO_INDEX.md`
- imposer une doctrine Git generale

---

## 5. Ouverture / fermeture / propagation

### 5.1 Ouverture

Ouverture parent :
- prouver le besoin, la cible, le plan et l'intention produit
- etablir son statut dans `GO_INDEX.md`
- etablir le support Git du flux seulement s'il est prouve ou necessaire

Ouverture sous-GO :
- prouver le rattachement a un parent ou etablir un GO simple si aucun parent n'est prouve
- borner l'objectif local
- heriter du support Git du parent par defaut

### 5.2 Fermeture

Fermeture sous-GO :
- closeout local explicite
- maintien ou mise a jour du parent
- mise a jour des index concernes
- propagation vers la continuite produit si le sous-GO change l'etat produit
- decision explicite sur le sort du support Git local s'il existe

Fermeture parent :
- closeout parent explicite
- retrait ou reclassification dans les surfaces de continuite actives
- propagation vers la continuite produit
- decision explicite sur le sort de la branche du parent si une branche dediee existe

### 5.3 Propagation minimale

La fermeture canonique propage au minimum vers :
- le parent, si un parent existe
- `GO_INDEX.md`
- `NEXT_GO_CANDIDATES.md` si le prochain geste change
- la continuite produit

Selon le cas, elle peut aussi propager vers :
- `ACTIVE_STREAMS.md`
- `BRANCH_STATE.md`
- les annexes derivees

### 5.4 Symetrie

La matrice retient une symetrie stricte :
- ce qui est ouvert doit avoir un point de reprise lisible
- ce qui est ferme doit avoir une propagation lisible
- aucun chantier ne doit rester seulement dans un support local sans reflet dans la surface canonique adequate

---

## 6. Placement / indexation

| Type d'objet | Surface canonique | Indexation minimale | Statut |
|---|---|---|---|
| regle stable | `docs/governance/` | `docs/INDEX.md` | noyau ou annexe selon autorite |
| continuite produit | surface gouvernante produit | `docs/INDEX.md` et surface dediee si necessaire | noyau |
| parent / GO simple / sous-GO | `docs/chantiers/<GO_...>/` | `GO_INDEX.md` | noyau structurel |
| next par parent actif | `docs/index/NEXT_GO_CANDIDATES.md` | interne a la surface | noyau de continuite active |
| reprise operatoire | `docs/index/REPRISE.md` | aucune souverainete de liste | support seulement |
| flux actifs | `docs/index/ACTIVE_STREAMS.md` | interne a la surface | support |
| etat branches | `docs/index/BRANCH_STATE.md` | interne a la surface | support branches |
| carte humaine | `docs/architecture/` ou `docs/INDEX.md` | navigation | annexe |
| registre machine-readable | `registry/*` | `registry/meta_index.yaml` | derive / support |
| journal brut | `journal.md` | aucune indexation canonique active | hors noyau |
| journal derive | `journal/index/*` | aucune substitution a `docs/index/*` | support |
| journal archive | `journal/canon/*` | aucune substitution a `docs/index/*` | preuve / archive |

Regles de placement :
- une regle stable ne doit pas etre cachee dans un chantier
- un chantier ne doit pas remplacer un index
- un index ne doit pas absorber un closeout
- un registre derive ne doit pas remplacer la verite canonique
- `REPRISE.md` reste une surface operatoire seulement

Principes frontmatter / metadata / tags :
- le frontmatter canonique porte la verite structurale minimale
- `topic_keys` servent au recroisement stable
- `search_tags` et metadata enrichies restent derives apres stabilisation de la structure
- le registry de recherche est derive et non souverain

La matrice ne prend pas les tags comme base de regle.
Elle pose seulement le principe de derivation posterieure.

---

## 7. Invariants

- ne pas creer de structure parallele
- ne pas transformer une hypothese en regle
- ne pas supposer un parent non prouve
- ne pas remonter `REPRISE.md` dans le noyau canonique
- ne pas transformer `BRANCH_STATE.md` en doctrine generale
- ne pas utiliser housekeeping branches comme doctrine complete
- ne pas imposer `1 GO = 1 branche`
- ne pas faire preceder la structure par les tags / metadata
- ne pas laisser un support inferieur contredire une couche superieure sans reserve explicite

---

## 8. Points reportes et limites

### 8.1 Reserve AI team

Cas reporte :
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`

Statut retenu :
- l'objet reste reconnu comme entree d'index
- la contradiction locale reelle sur `DOSSIER_PRESENT` reste une reserve de synchronisation
- le contenu local du parent n'est pas promu dans le noyau tant qu'il n'est pas confirme localement

Effet :
- l'objet ne contamine pas la regle generale
- la reserve reste non bloquante

### 8.2 Limite `REPRISE.md`

Statut retenu :
- surface operatoire seulement
- non souveraine pour la liste
- utile pour le pilotage, non pour la canonisation de cardinalite

Effet :
- `REPRISE.md` peut etre cite comme support
- `REPRISE.md` ne peut pas contredire `GO_INDEX.md`

### 8.3 Limites de corpus

Sources externes absentes localement :
- ne sont pas reinjectees dans le noyau
- peuvent etre rappelees seulement comme limite de corpus

### 8.4 Annexes

Restent hors noyau souverain :
- details housekeeping branches
- details naming et regex
- details frontmatter / metadata / tags
- cartes exhaustives de placement

Ces sujets relevent des annexes et non de la matrice centrale.

---

## 9. Resume point

La matrice V2 retient :
- produit d'abord
- `GO_INDEX.md` comme verite de liste
- `NEXT_GO_CANDIDATES.md` comme surface next par parent actif
- parent et sous-GO seulement si prouves
- branche comme support Git du flux
- sous-GO sur support Git du parent par defaut
- branche enfant seulement en exception motivee
- fermeture avec propagation vers parent, index et continuite produit
- `REPRISE.md` comme support operatoire seulement

La matrice V2 n'integre pas comme noyau :
- les details de housekeeping branches
- les details naming
- les tags et metadata comme base de regle
- les contradictions locales bornees non encore resynchronisees
