---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01_UPDATE_MATRIX_RULES
doc_type: update_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01
status: draft_for_review
lifecycle_stage: child_update_rules
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - update-protocol
  - maintenance
  - matrix
  - rules
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/01_UPDATE_MATRIX_RULES.md
point_de_reprise: "Règles de mise à jour des 6 couches produit après chaque PR significative."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/00_CADRAGE.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
  - docs/product/guides/README.md
  - docs/product/UPDATE_PROTOCOL.md
---

# 01_UPDATE_MATRIX_RULES

## 1_OBJECTIF

Définir pour chaque couche de la pile Product Usage Atlas :
- **quand** la couche doit être mise à jour ;
- **qui** la déclenche (type de PR) ;
- **comment** la mettre à jour (procédure) ;
- **par qui** (rôle) ;
- **avec quoi** (entrées nécessaires).

## 2_LES_6_COUCHES

```text
1. PRODUCT_USAGE_MATRIX.md    → vue rapide : bucket, statut, guide
2. PRODUCT_USAGE_ATLAS.md     → vue détaillée : fiche complète par produit
3. FINAL_TARGET_GAPS.md       → gaps restants vers produit fini
4. PRODUCT_USAGE_GRAPH.mmd    → carte visuelle des dépendances
5. guides/*.md                → guides d'usage / reprise / implémentation
6. UPDATE_PROTOCOL.md         → le présent protocole (auto-référentiel)
```

## 3_REGLES_PAR_COUCHE

### 3.1 PRODUCT_USAGE_MATRIX.md

**Quand :** après toute PR qui change l'état d'un produit.

Trigger :

```text
- un produit est ajouté à l'Atlas
- un produit change de bucket (ex: DOC_ONLY → USABLE_LIMITED)
- un produit change de sous-type
- un guide est créé ou retiré
- un produit est rétrogradé en DO_NOT_PROMOTE
- un gap majeur est fermé (change l'usage réel)
```

Ne pas déclencher pour :

```text
- une PR purement documentaire sans changement d'état
- un fix de typo dans un guide
- un commit de merge sans PR associée
```

**Comment :**

```text
1. Lire le closeout + diff de la PR mergée.
2. Identifier les produits affectés.
3. Pour chaque produit :
   a. Recalculer le bucket (USABLE_NOW / USABLE_LIMITED / DOC_ONLY / SIMULATED_ONLY / FORBIDDEN_LIVE).
   b. Appliquer la précédence prudente (FORBIDDEN_LIVE > SIMULATED_ONLY > DOC_ONLY > USABLE_LIMITED > USABLE_NOW).
   c. Mettre à jour la ligne dans le tableau MATRIX.
   d. Conserver l'ancien bucket dans l'historique du chantier, pas dans MATRIX.
4. Vérifier que la somme des produits par bucket est cohérente.
5. Commiter avec message "docs: update product usage matrix after PR #NNN".
```

**Entrées nécessaires :**

```text
- URL ou numéro de la PR mergée
- closeout du chantier
- fichiers modifiés (diff --stat)
- avis de l'opérateur si le changement est structurel
```

### 3.2 PRODUCT_USAGE_ATLAS.md

**Quand :** après une PR qui change la fiche détaillée d'un produit (pas juste le bucket).

Trigger :

```text
- un produit est ajouté à l'Atlas (nouvelle fiche complète)
- canonical_sources change (nouveau module, suppression, refactoring)
- remaining_gaps change structurellement
- next_go change
- usage_mode change (DOC_ONLY → USABLE_LIMITED, etc.)
- do_not_use_notes ajoutées ou retirées
```

**Comment :**

```text
1. Mettre à jour la fiche produit dans PRODUCT_USAGE_ATLAS.md.
2. Champs obligatoires inchangés :
   - product_id, product_name, parent_branch, reason_to_exist
   - final_usage_target, current_state, usable_now
   - usage_mode, user_guide, canonical_sources
   - remaining_gaps, next_go, do_not_use_notes
3. Tout changement de bucket doit être tracé dans le chantier source.
4. Vérifier que canonical_sources pointe vers des fichiers existants (check repo).
5. Vérifier que next_go n'est pas vide ni obsolète.
```

**Entrées nécessaires :**

```text
- fiche produit actuelle dans Atlas
- closeout ou document source du changement
- preuve repo (fichiers existants, tests passés)
```

### 3.3 FINAL_TARGET_GAPS.md

**Quand :** après une PR qui ferme un gap ou en ouvre un nouveau.

Trigger :

```text
- un gap est fermé → retiré de la liste ou marqué CLOSED
- un nouveau gap est identifié → ajouté avec NEXT_GO associé
- un gap change de sévérité (bloquant → non bloquant, ou inverse)
- un produit est ajouté à l'Atlas → ses gaps sont ajoutés
```

**Comment :**

```text
1. Lister les gaps fermés par la PR (source : closeout).
2. Lister les nouveaux gaps ouverts (source : remaining_gaps du closeout).
3. Mettre à jour le tableau des gaps par produit.
4. Chaque gap doit avoir :
   - description
   - sévérité (BLOCKING / MAJOR / MINOR)
   - NEXT_GO associé
   - date d'identification
```

**Entrées nécessaires :**

```text
- closeout du chantier (remaining_gaps après merge)
- diff de la PR mergée
```

### 3.4 PRODUCT_USAGE_GRAPH.mmd

**Quand :** après une PR qui change la topologie (dépendances entre produits).

Trigger :

```text
- un nouveau produit est ajouté avec des dépendances
- une dépendance entre produits est créée ou rompue
- un produit est rétrogradé (impacte les dépendants)
- une consolidation de modules change la carte
```

Ne pas déclencher pour :

```text
- un changement de bucket sans impact topologique
- une mise à jour de guide
```

**Comment :**

```text
1. Mettre à jour le graphe Mermaid dans PRODUCT_USAGE_GRAPH.mmd.
2. Convention graphique :
   - USABLE_NOW → bord épais, vert
   - USABLE_LIMITED → bord normal, bleu
   - DOC_ONLY → pointillés, gris
   - SIMULATED_ONLY → pointillés, orange
   - FORBIDDEN_LIVE → barré, rouge
3. Les arêtes représentent les dépendances d'usage.
4. Vérifier que le graphe compile (mermaid-cli ou preview GitHub).
```

### 3.5 Guides (docs/product/guides/*)

**Quand :** après une PR qui change l'usage documenté d'un produit.

Trigger :

```text
- un nouveau guide est créé (produit ajouté à l'Atlas)
- l'usage autorisé change (ex: DOC_ONLY → USABLE_LIMITED, ajout de commandes)
- les prérequis changent (nouvelle dépendance, nouvelle config)
- le statut CONTINUITY_STATE change
- des limites sont levées
```

**Comment :**

```text
1. Appliquer le modèle de guide défini dans 03_USER_GUIDE_MODEL.md :
   - Ce que c'est
   - A quoi ça sert
   - Quand l'utiliser
   - Quand ne pas l'utiliser
   - Prérequis
   - Commandes / accès
   - Procédure simple
   - Vérification PASS
   - Limites
   - Dépannage
   - Source canonique
   - NEXT_GO
2. Ajouter les champs de continuité enrichis (PR #242) :
   - MASTER_TARGET
   - IMPLEMENTATION_PATH
   - CONTINUITY_STATE
   - REPRISE_POINT
   - PROMOTION_CONDITIONS
3. Mettre à jour guides/README.md.
```

**Entrées nécessaires :**

```text
- closeout + diff de la PR mergée
- preuve d'usage (logs, tests, captures)
```

### 3.6 UPDATE_PROTOCOL.md (auto-maintenance)

**Quand :** après une PR qui change la méthode elle-même (comme UPDATE_PROTOCOL_01).

Trigger :

```text
- un nouveau bucket est ajouté
- un sous-type est ajouté
- une règle de promotion est changée
- la checklist PR est modifiée
- le rôle d'OpenClaw ou des workers est redéfini
```

**Comment :**

```text
1. Mettre à jour UPDATE_PROTOCOL.md pour refléter les nouvelles règles.
2. Incrémenter le champ updated_at.
3. Ajouter un lien vers le chantier source.
4. Ne pas dupliquer : UPDATE_PROTOCOL.md = résumé exécutable, les chantiers = détail complet.
```

## 4_ORDRE_DE_MISE_A_JOUR

Après chaque PR significative, l'ordre canonique est :

```text
1. UPDATE_PROTOCOL.md       (si la méthode elle-même change)
2. PRODUCT_USAGE_MATRIX.md  (buckets, statuts)
3. PRODUCT_USAGE_ATLAS.md   (fiches détaillées)
4. FINAL_TARGET_GAPS.md     (gaps fermés/ouverts)
5. Guides concernés         (usages documentés)
6. guides/README.md         (index des guides)
7. PRODUCT_USAGE_GRAPH.mmd  (carte topologique)
```

## 5_COMMIT_CONVENTION

Toute mise à jour d'une couche produit après PR doit suivre le format :

```text
docs: update {COUCHE} after PR #{NNN} ({GO_ID})
```

Exemples :

```text
docs: update PRODUCT_USAGE_MATRIX after PR #243 (SOURCE_LOCK_01)
docs: update guides/README after PR #242 (USER_GUIDES_01)
docs: update PRODUCT_USAGE_GRAPH after PR #241 (APPLY_REPO_INVENTORY_01)
```

## 6_EXCEPTIONS

```text
E1. Une PR en cascade (parent + enfants mergés dans la même session)
    → une seule mise à jour groupée des couches peut couvrir toute la cascade.
    → le message de commit liste toutes les PRs concernées.

E2. Une PR de rollback
    → la mise à jour des couches doit annuler le changement précédent.
    → le message de commit précise "rollback after PR #NNN".

E3. Une PR sans closeout (merge direct)
    → la mise à jour des couches est quand même obligatoire.
    → le closeout peut être produit après merge si nécessaire.
```

## 17_RESUME_POINT

```text
6 couches à maintenir, 6 procédures de mise à jour, 1 ordre canonique.
Toute PR qui change l'état d'un produit doit déclencher la chaîne de mise à jour.
Les commits de mise à jour sont tracés par référence à la PR source.
```
