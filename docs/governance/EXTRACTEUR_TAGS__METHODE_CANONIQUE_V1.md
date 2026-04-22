---
doc_id: OPT_TRADING_EXTRACTEUR_TAGS_METHODE_CANONIQUE_V1
doc_type: governance
repo: opt-trading
project: opt-trading
module: session_extraction
go_id: GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - extracteur_tags
  - routing
  - documentation
  - memory
surface: governance
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/governance/DOC_LAYERS.md
  - docs/index/GO_INDEX.md
---

# EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1

## 1_CIBLE_MASTER

Documenter la méthode canonique : **extraction par tags**, puis **routage contrôlé** vers **mémoire projet** ou **documentation canonique** selon des règles explicites.

## 2_INITIAL_PROJECT_DOC

**Ref**  
`EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1`

**Type**  
Fiche de référence initiale figée.

**Règle canonique liée au nommage GO**  
Lorsque `2_INITIAL_PROJECT_DOC` décrit explicitement un produit ou une surface stable, ce token canonique devient la source à reprendre telle quelle, sans variante locale, pour `<PRODUCT_OR_SURFACE>` dans les GO dérivés.  
Si ce `PRODUCT_OR_SURFACE` n'est pas encore explicité dans `2_INITIAL_PROJECT_DOC`, il doit y être canonisé avant la création du GO, sans dériver une seconde source parallèle.

## 3_INITIAL_NEED

Valider et ancrer la bonne méthode pour :
- extraire les blocs utiles depuis une session ;
- les classer par tags ;
- décider s’ils vont en mémoire projet, en doc canonique, ou nulle part ;
- éviter la confusion entre mémoire, doc et brouillon de session.

## 4_MASTER_PROJECT_PLAN

### Direction
Mettre en place une méthode durable d’extraction de session basée sur des tags explicites et des destinations distinctes.

### Axes majeurs
1. Tagger
2. Extraire
3. Classifier
4. Router
5. Écrire de façon contrôlée
6. Préserver la séparation mémoire / doc / session

## 5_GO_PLAN

### Chantier dérivé
`GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01`

### Objet
Formaliser la méthode avant implémentation MCP / app / extracteur.

## 6_FINAL_TARGET

Obtenir une méthode canonique documentée avec :
- schéma de tags ;
- règles de routage ;
- invariants ;
- exclusions ;
- setup cible pour implémentation.

## 7_CANONICAL_STATE

### ETABLI
La bonne méthode est :

**Extraction par tags**  
→ **classification du bloc**  
→ **routage vers la bonne destination**  
→ **écriture contrôlée**

### ETABLI
Il faut distinguer strictement :
- mémoire projet
- documentation canonique
- contenu non persistant de session

### NEXT_GO
Formaliser la table de routage initiale et les tools cibles.

## 8_VALIDATED_PLAN

1. Définir les tags autorisés
2. Définir les destinations autorisées
3. Définir les règles tag → destination
4. Définir les cas exclus
5. Définir les write-actions autorisées
6. Définir le mode validation / dry-run / confirmation
7. Implémenter ensuite seulement

## 9_SELECTED_SOLUTION

### Solution retenue
Un système à trois étages :

#### A. Extraction
Lecture de blocs structurés marqués par tags ou sections canonisées.

#### B. Classification
Chaque bloc reçoit un statut de routage :
- mémoire
- documentation
- rejet / non persistant
- proposition à confirmer

#### C. Persistance contrôlée
Chaque destination possède son propre mécanisme d’écriture.

## 10_SELECTED_SETUP

### Structure retenue

#### 1. Entrée
Session ou export de session.

#### 2. Parseur
Détection de blocs taggés.

#### 3. Moteur de routage
Application d’une table de décision.

#### 4. Sorties distinctes
- mémoire projet
- documentation canonique
- export de session
- aucun enregistrement

#### 5. Write-actions séparées
Pas de write global unique.

## 11_KEY_DECISIONS

### DECISION
Ne pas fusionner mémoire projet et documentation canonique.

### DECISION
Ne pas persister les hypothèses, scratchs ou brouillons par défaut.

### DECISION
Utiliser des règles explicites tag → destination.

### DECISION
Séparer les actions :
- extraire
- classifier
- sauvegarder mémoire
- écrire doc
- exporter session

### DECISION
Privilégier un mode contrôlé avec proposition ou confirmation pour les écritures sensibles.

## 12_INVARIANTS

### INVARIANT
La mémoire projet n’est pas la documentation canonique.

### INVARIANT
La documentation canonique ne doit pas recevoir le flux brut de session.

### INVARIANT
Les hypothèses non validées ne deviennent pas du durable par défaut.

### INVARIANT
Une écriture durable doit toujours être traçable et dirigée vers une destination explicite.

### INVARIANT
Le routage doit être piloté par des règles stables, non par interprétation libre au cas par cas.

## 13_ESTABLISHED

### ESTABLISHED
Les bons candidats **mémoire projet** sont :
- préférences stables
- conventions
- décisions durables
- invariants
- setup retenu
- état stable réutilisable

### ESTABLISHED
Les bons candidats **documentation canonique** sont :
- plan maître
- plan validé
- solution retenue
- setup retenu
- état canonique
- reprise
- closeout
- cadrage
- architecture

### ESTABLISHED
Les blocs suivants ne doivent pas être persistés par défaut :
- `SCRATCH`
- `HYPOTHESIS`
- brouillons temporaires
- contenu ambigu
- bruit de session

## 14_HYPOTHESIS

### HYPOTHESIS
Le meilleur mode opératoire sera probablement :
- extraction automatique
- classification automatique
- écriture semi-automatique avec confirmation selon sensibilité

### HYPOTHESIS
Un mode `dry_run` avec diff proposé avant écriture doc sera utile dès V1.

## 15_REMAINING_GAP

Il reste à figer :
1. format exact des tags
2. table de routage initiale
3. mode de validation
4. forme du stockage mémoire
5. forme du patch doc
6. journal d’écriture

## 16_TODO

### TODO_01
Figer le schéma de tags autorisés.

### TODO_02
Figer la table tag → destination.

### TODO_03
Définir les tags interdits à la persistance.

### TODO_04
Définir les actions d’écriture minimales :
- `extract_tagged_blocks`
- `save_memory_brick`
- `append_canonical_doc`
- `export_session_summary`

### TODO_05
Définir le mode :
- auto
- dry-run
- confirmation requise

### TODO_06
Documenter un exemple complet de session → extraction → routage → sortie.

## 17_RESUME_POINT

### REPRISE
Méthode validée à ancrer :

**Extraction par tags**  
→ **classification**  
→ **routage mémoire vs documentation vs non persistant**  
→ **écriture contrôlée et traçable**

### REPRISE
Ne jamais confondre :
- mémoire projet = continuité utile
- documentation canonique = vérité structurée du projet
- session = espace de travail temporaire

## 18_TO_DOCUMENT

### TAGS
- `DOC_REF`
- `PLAN_MAITRE_PROJET`
- `SOLUTION_RETENUE`
- `SETUP_RETENU`
- `KEY_DECISIONS`
- `INVARIANTS`
- `ESTABLISHED`
- `HYPOTHESIS`
- `TODO`
- `REPRISE`

### Blocks à extraire
- `EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1`
- `EXTRACTEUR_TAGS__SEPARATION_MEMOIRE_DOC_SESSION`
- `EXTRACTEUR_TAGS__ROUTAGE_CONTROLE`
- `EXTRACTEUR_TAGS__INVARIANTS_PERSISTENCE`

## 19_TO_REMEMBER

### NO_MEMORY
Pas de bio memory à ajouter.  
Ceci relève de la **documentation canonique projet**.
