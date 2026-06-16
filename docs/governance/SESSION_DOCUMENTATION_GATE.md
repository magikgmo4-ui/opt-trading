---
doc_id: OPT_TRADING_SESSION_DOCUMENTATION_GATE
doc_type: governance
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - documentation
  - session_gate
  - continuity
  - restart
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 3. References canoniques a consulter"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/INDEX.md
  - docs/master_pack/mission_starter_pack/00_mission_start_guide.md
  - docs/governance/HUMAN_CONTINUITY_TRANSMISSION.md
---

# SESSION_DOCUMENTATION_GATE

## Objet

Cette fiche fixe la règle de session minimale pour décider s’il faut produire ou mettre à jour une documentation durable.

Elle ne crée pas un nouveau système de templates.
Elle s’appuie sur le canon déjà en place dans le repo.

Hiérarchie minimale de lecture :
- état réel prouvé
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- annexes stables utiles au recroisement
- surfaces opératoires concernées

---

## 1. Réflexe de session

Avant de créer, déplacer, mettre à jour ou demander une documentation durable, poser la question :

**À documenter ?**

- Si **non** : ne pas créer de documentation durable.
- Si **oui** : utiliser cette fiche de référence.

Formule courte de continuité :

```text
À documenter ? Si oui, fiche.
```

---

## 2. Ce que la fiche doit cadrer

Si la réponse est **oui**, cadrer au minimum :

- besoin initial
- cible finale / objectif final
- plan validé
- état établi courant
- gap restant
- next GO

La continuité utile doit aussi préserver, si pertinent :

- machine owner / thread machine
- rôle actif IA/IDE
- rôle repo / produit

Ces couches doivent rester séparées.

---

## 3. Références canoniques à consulter

Cette fiche n’écrase pas le canon existant. Elle renvoie vers lui.

Références minimales :

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` : matrice maître souveraine de gouvernance documentaire
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` : annexe stable secondaire utile si un recroisement fin est nécessaire
- `docs/INDEX.md` : navigation documentaire canonique
- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` : point d’entrée de session
- `docs/index/REPRISE.md` : surface opératoire de reprise
- `docs/governance/HUMAN_CONTINUITY_TRANSMISSION.md` : principes humains de transmission

---

## 4. Règle de placement

Cette fiche ne fige pas de nouveau layout documentaire au-delà de ce qui est déjà validé.

Règles minimales :

- utiliser le canon documentaire déjà établi dans le repo
- ne pas créer de structure parallèle ad hoc pour contourner le canon
- garder le lien entre décision validée, chantier actif, reprise et next step

---

## 5. Quand documenter

Documenter par défaut si au moins un de ces cas est vrai :

- décision validée
- convention durable
- point de reprise important
- chantier multi-session
- chantier multi-machine
- closeout / validation réelle
- transfert ou reprise nécessitant une trace durable

Ne pas documenter par défaut si le contenu est purement éphémère, sans valeur de reprise ni de transmission.

---

## 6. Sortie attendue quand la réponse est oui

La sortie documentaire doit être :

- compacte
- opératoire
- structurée
- alignée sur le canon réel du repo
- explicite sur le besoin, la cible, le plan, l’état établi, le gap et le next GO

---

## 7. Propagation canonique de l’intention et de la cible finale

Quand un chantier structuré est ouvert, la documentation durable doit aussi figer explicitement :

- l’**intention** du chantier
- le **target final** / produit final voulu

Et ces deux éléments doivent être **reconduits explicitement** dans les GO suivants quand ils appartiennent à la même trajectoire.

### Règle
Ne pas laisser l’intention et la cible finale uniquement dans une conversation ou dans un seul opening initial.

Les faire suivre dans la documentation canonique pour garder une suite de GO :

- fluide
- non ambiguë
- transmissible
- et alignée sur l’objectif final retenu

### Formulation minimale attendue
Quand c’est pertinent, faire apparaître explicitement :

- `Intention`
- `Produits finaux voulus / objectifs du chantier`

Cette règle devient canonique et systématique pour les chantiers structurés où la trajectoire doit rester stable à travers plusieurs GO.

---

## 8. Maintenance obligatoire du tableau canonique des chantiers

Quand un **parent**, un **chantier** ou un **sous-chantier** est :

- créé
- renommé
- reclassé
- rerattaché
- archivé
- clos
- ou réouvert

le tableau canonique des chantiers doit être mis à jour dans le même lot documentaire.

Référence canonique à maintenir :
- `docs/index/GO_INDEX.md`

### Contrôle de complétude

Le tableau canonique ne peut être considéré cohérent que si :

- chaque entrée `### GO_...` de `docs/index/GO_INDEX.md` a au moins une ligne dans le tableau
- chaque dossier direct de `docs/chantiers/` a au moins une ligne correspondante
- chaque sous-chantier explicitement retenu est sourcé
- chaque champ `STATUT` et `DOSSIER_PRESENT` est cohérent avec l’état réel du repo

### Règle de non-oubli

Aucun chantier nouveau ne doit rester seulement dans :

- un dossier
- un cadrage
- un plan
- un closeout
- une reprise locale
- ou une fiche isolée

sans être reflété dans le tableau canonique.

---

## 9. Gate permanent avant PR

Avant toute PR, même petite, vérifier :

1. Quel est le `GO_ID` ?
2. Le GO existe-t-il dans `docs/chantiers/` ?
3. Le fichier `00_INITIAL_PROJECT_DOC.md` existe-t-il ou le GO existant est-il explicitement référencé ?
4. Le fichier `FILE_SCOPE.txt` couvre-t-il chaque fichier modifié ?
5. La PR touche-t-elle un seul GO ?
6. Les conditions d'ouverture et de fermeture sont-elles écrites ?
7. La validation réelle est-elle indiquée ?
8. Le point de reprise est-il clair si la target supérieure reste ouverte ?

Si une réponse est non, ne pas ouvrir ou merger la PR.

---

## 10. Statut

Fiche de référence de gouvernance.

À utiliser comme gate minimal de session :

```text
À documenter ? Si oui, fiche.
```

## RISKS

- À qualifier.
