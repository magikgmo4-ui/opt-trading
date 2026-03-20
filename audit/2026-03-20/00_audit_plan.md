# Plan chef de projet — Audit croisé `opt-trading`

## 1. Objet de l’audit
Établir une lecture croisée propre des branches utiles du repo `opt-trading`, produire un rapport normalisé par branche, puis converger vers une décision de pilotage claire sur :
- la branche canonique
- les branches à intégrer
- les branches à extraire partiellement
- les branches à archiver

Cet audit doit être **traçable dans Git** et **indépendant de la mémoire de session**.

---

## 2. Source de vérité de l’audit
La source de vérité de cet audit sera :

- **Repo** : `magikgmo4-ui/opt-trading`
- **Branche d’audit dédiée** : `audit/opt-trading-20260320a`
- **Base de départ** : `sot/mainline`
- **Méthode** : un rapport à la fois, validé avant le suivant

La conversation sert à piloter,  
la branche `audit/opt-trading-20260320a` sert à conserver la mémoire durable.

---

## 3. Doctrine de travail
Règles obligatoires :

1. **Une analyse à la fois**
2. **Un rapport à la fois**
3. **Même template pour les rapports comparables**
4. **Validation utilisateur avant de passer au suivant**
5. **Sauvegarde du rapport validé dans la branche d’audit**
6. **Pas de mélange entre plusieurs analyses dans un même fichier**
7. **Pas d’invention si une preuve Git manque**
8. **La décision PM vient après la lecture réelle, pas avant**

---

## 4. Livrables attendus
L’audit doit produire au minimum :

### A. Cadrage
- plan d’audit
- méthode
- périmètre
- ordre d’analyse

### B. Rapports individuels
Un fichier par branche auditée, avec template fixe.

### C. Synthèse croisée
- matrice de convergence
- conflits / dépendances / recouvrements
- statut PM final par branche

### D. Décision de pilotage
- quoi garder
- quoi merger
- quoi absorber partiellement
- quoi archiver
- quoi documenter pour reprise future

---

## 5. Template de référence
Le template validé pour les rapports individuels reste :

1. Identité  
2. Intention de la branche  
3. Surface modifiée  
4. Réalité technique observée  
5. État de maturité  
6. Risques  
7. Dépendances et recouvrements  
8. Valeur projet  
9. Verdict chef de projet  
10. Résumé exécutable  
+ notation finale

Sauf décision contraire plus tard, ce template reste le standard pour les rapports de branche.

---

## 6. Périmètre initial de l’audit
Branche canonique de référence :
- `sot/mainline`

Branches à auditer ensuite :
- `sot/build`
- `main`
- `fix/desk-ui-toolbox`
- `feat/engines-plugin`
- `feat/execution-engine`
- `feat/persistent-state`
- `feat/position-engine`
- `feat/position-guard`
- `feat/risk-engine`

Branches hors cœur mais à qualifier ensuite :
- `antigravity/main`
- `backup/main-before-filter`

---

## 7. Ordre de traitement recommandé
Ordre validé côté pilotage :

### Phase 1 — Ancrage canonique
1. `sot/mainline`

### Phase 2 — Anciennes bases / lignes de divergence
2. `sot/build`
3. `main`

### Phase 3 — Branches probablement absorbées ou dépassées
4. `fix/desk-ui-toolbox`

### Phase 4 — Branches feature à valeur potentiellement survivante
5. `feat/engines-plugin`
6. `feat/execution-engine`
7. `feat/persistent-state`
8. `feat/position-engine`
9. `feat/position-guard`
10. `feat/risk-engine`

### Phase 5 — Branches laboratoire / archive / périmètre séparé
11. `antigravity/main`
12. `backup/main-before-filter`

---

## 8. Méthode d’exécution détaillée
Pour chaque branche :

### Étape 1 — Lecture
- identité réelle de la branche
- comparaison avec la base retenue
- dernier commit clé
- 1 à 3 fichiers structurants si nécessaire
- lecture des PR liées si utile

### Étape 2 — Rapport dans la session
- rapport complet au template
- aucun autre chantier mélangé
- verdict PM provisoire

### Étape 3 — Validation
- tu valides ou ajustes
- on fige la version retenue

### Étape 4 — Sauvegarde Git
- enregistrement du rapport validé dans `audit/opt-trading-20260320a`

### Étape 5 — Passage au suivant
- uniquement après validation

---

## 9. Critères de décision PM
Chaque branche devra être classée dans une catégorie finale :

- **Canonique**
- **À intégrer**
- **À intégrer partiellement**
- **À documenter puis archiver**
- **À archiver**
- **À fermer**

Les critères de classement :

- valeur opératoire réelle
- valeur structurelle
- valeur documentaire
- niveau de maturité
- risque de confusion canonique
- dépendances
- recouvrement avec d’autres branches
- niveau de survivance utile

---

## 10. Risques à contrôler pendant l’audit
Risques principaux :

- partir d’un nom de branche trompeur
- prendre une PR comme vérité alors que le code dit autre chose
- mélanger branche active et branche historique
- perdre la mémoire entre deux étapes
- documenter trop tôt avant validation
- laisser plusieurs “sources de vérité” coexister

Mesure de contrôle :
- tout rapport validé est écrit dans la branche d’audit
- pas de saut d’étape
- pas de synthèse finale avant suffisamment de rapports individuels

---

## 11. Usage futur de Claude
Claude n’est **pas** la mémoire primaire de cet audit.

Rôle de Claude, plus tard :
- mise au propre documentaire
- génération de fichiers Windows/reprise
- harmonisation de style
- documentation de synthèse à partir des rapports déjà validés

Rôle de Git dans cette audit :
- mémoire principale
- historisation
- point de reprise stable

Donc :
- **d’abord** rapports validés dans `audit`
- **ensuite** prompt Claude si nécessaire

---

## 12. Livrables Git proposés
Dans la branche `audit/opt-trading-20260320a`, je recommande cette structure :

- `audit/2026-03-20/00_audit_plan.md`
- `audit/2026-03-20/01_sot_mainline.md`
- `audit/2026-03-20/02_sot_build.md`
- `audit/2026-03-20/03_main.md`
- etc.

Puis plus tard :
- `audit/2026-03-20/90_convergence_matrix.md`
- `audit/2026-03-20/99_pm_decision.md`

---

## 13. Point de départ opérationnel
Le point de départ retenu pour cette nouvelle passe est :

- branche d’audit : `audit/opt-trading-20260320a`
- base : `sot/mainline`
- premier rapport à enregistrer : **plan d’audit**
- deuxième fichier : **Rapport 01 — `sot/mainline`**
- ensuite : **Rapport 02 — `sot/build`**

---

## 14. Décision PM actuelle
Décision de pilotage à ce stade :

- on repart proprement
- on documente cet audit dans Git dès le début
- on suit une progression séquentielle stricte
- on ne dépend plus de la mémoire de session pour conserver l’état du chantier

---

## 15. Résumé exécutable
- repo cible : `opt-trading`
- branche d’audit : `audit/opt-trading-20260320a`
- méthode : un rapport à la fois
- validation : obligatoire entre chaque rapport
- mémoire durable : Git
- prochain fichier à créer après validation : `audit/2026-03-20/00_audit_plan.md`
