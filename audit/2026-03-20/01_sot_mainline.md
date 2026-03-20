# RAPPORT DE BRANCHE — `magikgmo4-ui/opt-trading` / `sot/mainline`

## 1. Identité
- **Repo** : `magikgmo4-ui/opt-trading`
- **Branche auditée** : `sot/mainline`
- **Réf canonique de comparaison** : `sot/mainline`
- **Base de comparaison retenue** : `main` pour la divergence historique ; `sot/build` comme ancien socle opératoire
- **Dernier commit clé** : `a2f75c0ed23200cd0a56533884483066a44e19cb`
- **Message du dernier commit clé** : `git_fleet_guard: add read-only fleet git audit module`
- **Auteur / période récente** : `Ghost`, `2026-03-20T01:26:06Z`
- **Statut Git/PR connu** : branche active du repo ; aucune PR de pilotage retenue ici comme référence primaire
- **PR liées** : non retenues à ce stade
- **Niveau de confiance initial** : élevé

## 2. Intention de la branche
- **Objectif supposé d’après le nom** : ligne principale “source of truth”
- **Objectif visible d’après commits / fichiers** : branche d’orchestration active, mêlant docs canoniques, kanban, runbooks, continuité de mission et modules durables
- **Objectif réel retenu** : **branche canonique opérationnelle** du projet
- **Périmètre fonctionnel** : mixte
- **Question à laquelle cette branche répond** : “Quel est l’état réel, opératoire et documenté du repo aujourd’hui ?”
- **Ce que cette branche n’est pas** : ni une feature isolée, ni une simple branche de docs, ni un miroir passif de `main`

## 3. Surface modifiée
- **Zones principales touchées** : `docs/`, `docs/ot/`, `docs/master_pack/`, `modules/`, plus les repères code documentés dans l’index (`webhook_server.py`, `perf/perf_app.py`, `adapters/`, `shared/`)
- **Fichiers/dossiers structurants** :
  - `docs/INDEX.md`
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - ajout récent du module `git_fleet_guard` via le dernier commit
- **Type de changement** : consolidation, gouvernance, module durable, documentation opératoire
- **Amplitude estimée** : forte
- **Nature dominante** : mixte, avec forte dominante documentation/opérations

## 4. Réalité technique observée
- L’index documentaire place explicitement au centre de la branche une roadmap annotée, un kanban “source of truth”, un point d’entrée unique d’ouverture de session, des checklists de mission longue, l’architecture, l’API, les runbooks et les schémas de continuité.
- Le kanban affirme explicitement être la **source de vérité kanban** du repo pour les statuts, closings et points de reprise, avec règle opposable de clôture propre.
- Le dernier commit ajoute `git_fleet_guard`, module durable d’audit Git multi-machine en lecture seule, avec garanties anti-actions destructives et rapports JSON/Markdown, ce qui confirme une branche encore active et orientée exploitation/gouvernance.
- **Ce qui devient canonique ou tente de le devenir** :
  - le kanban `source_of_truth`
  - le starter pack d’ouverture
  - les runbooks et la doctrine Trae
  - les modules durables avec wrappers et preuves
- **Ce qui reste legacy / compat / doublon** : non prouvé précisément dans cette passe, mais la densité documentaire et la coexistence de plusieurs couches (`docs/`, `master_pack`, `ot/trae`, modules) signalent un risque réel de recouvrement
- **Hypothèses implicites détectées** :
  - la documentation est opposable
  - la clôture exige doc canonique + kanban + point de reprise
  - `sot/mainline` sert de référence pratique au-dessus de `main`
- **Signaux de fragilité** :
  - densité documentaire élevée
  - couches de gouvernance nombreuses
  - risque de confusion si la maintenance baisse

## 5. État de maturité
- **Niveau** : branche canonique active / consolidation durable
- **Degré d’achèvement estimé** : élevé comme ligne de travail, mais non figé
- **Validation visible** : forte
- **Preuves disponibles** :
  - index documentaire structuré
  - kanban source of truth et règle de clôture opposable
  - ajout récent d’un module durable d’audit Git multi-machine

## 6. Risques
- **Risque principal** : confusion canonique par suraccumulation documentaire
- **Risques secondaires** :
  - mélange code/runtime/doctrine dans la même ligne
  - difficulté à séparer ce qui est vivant, clos, legacy, pré-V1
  - possible écart entre snapshot repo et runtime réel
- **Impact si on merge tel quel** : faible, car c’est déjà la meilleure candidate canonique
- **Impact si on ignore la branche** : critique
- **Impact si on archive trop vite** : destructeur pour la continuité
- **Dette documentaire** : moyenne à forte
- **Dette structurelle** : moyenne
- **Risque de confusion canonique** : moyen

## 7. Dépendances et recouvrements
- **Dépend de** : l’historique de `main`, puis de la consolidation propre à `sot/mainline`
- **Recouvre** :
  - état opératoire du repo
  - kanban, closings, reprise, doctrine Trae, starter pack, runbooks
- **Est recouverte par** : aucune branche plus crédible à ce stade
- **Conflits probables avec** :
  - `main` comme référence historique
  - `sot/build` comme ancien socle
  - certaines `feat/*` si elles portent encore de la valeur non absorbée
- **Peut être mergée seule ?** : elle sert déjà de pivot de convergence
- **Cherry-pick partiel nécessaire ?** : non pour la branche elle-même
- **Extraction documentaire préalable ?** : non, mais rationalisation future utile

## 8. Valeur projet
- **Valeur opératoire** : très forte
- **Valeur structurelle** : très forte
- **Valeur documentaire** : très forte
- **Valeur temporaire seulement ?** : non
- **Ce qu’on perdrait si on l’abandonne** : la meilleure source de vérité actuelle du repo
- **Ce qu’on gagnerait si on la converge** : un pivot stable pour auditer toutes les autres branches

## 9. Verdict chef de projet
- **Décision provisoire** : **conserver comme branche canonique principale**
- **Priorité** : P0
- **Action suivante recommandée** : auditer `sot/build` contre elle
- **Précondition avant action** : aucune
- **Ordre de traitement recommandé** : 1

## 10. Résumé exécutable
- **En une phrase** : `sot/mainline` est la branche canonique opérationnelle actuelle de `opt-trading`.
- **Décision** : la garder comme pivot d’audit
- **Pourquoi** : elle porte la source de vérité documentaire/kanban et reçoit encore des ajouts durables comme `git_fleet_guard`
- **Prochain pas concret** : produire le Rapport 02 — `sot/build`

## Notation
- **Clarté d’intention** : 5/5
- **Valeur réelle** : 5/5
- **Risque de confusion** : 3/5
- **Qualité de convergence potentielle** : 5/5
- **Maturité** : 5/5
- **Statut PM final** : **survivante / canonique**
